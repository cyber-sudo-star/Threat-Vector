import os
import sys
import json
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, render_template, request, redirect, url_for, g, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db, close_db, init_db, ensure_tables
from ml_engine.risk_scorer import calculate_user_risk_profile
from ml_engine.explainability import generate_explainable_feedback
from ml_engine.adaptive_selector import get_next_adaptive_scenario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'threat-vector-secure-key-2026'

app.teardown_appcontext(close_db)

DEFAULT_USERNAME = 'dhriti'

def get_current_user_id():
    """Returns currently logged-in user ID, or defaults to dhriti if not explicitly logged out."""
    if 'user_id' in session:
        return session['user_id']
    
    db = get_db()
    user = db.execute("SELECT id, username, full_name FROM users WHERE username = ?", (DEFAULT_USERNAME,)).fetchone()
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        return user['id']
    return 1

def fetch_user_profile_data(user_id):
    db = get_db()
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,)).fetchone()
    if not profile:
        return {
            "composite_risk_score": 50.0,
            "primary_weakness": "Baseline (Not yet evaluated)",
            "category_stats": {},
            "total_tests": 0,
            "accuracy_pct": 0.0,
            "risk_level": "Unrated"
        }

    stats = json.loads(profile['category_stats']) if profile['category_stats'] else {}
    score = profile['composite_risk_score']
    if score < 30.0:
        risk_level = "Low Risk (Vigilant 🛡️)"
    elif score < 65.0:
        risk_level = "Moderate Risk (Cautious ⚠️)"
    else:
        risk_level = "High Risk (Vulnerable 🚨)"

    return {
        "composite_risk_score": score,
        "primary_weakness": profile['primary_weakness'],
        "category_stats": stats,
        "total_tests": profile['total_tests'],
        "accuracy_pct": profile['accuracy_pct'],
        "risk_level": risk_level
    }

def fetch_user_attempts(user_id):
    db = get_db()
    rows = db.execute("""
        SELECT a.id, a.scenario_id, a.user_choice, a.is_correct, a.response_time_sec,
               strftime('%Y-%m-%d %H:%M', a.timestamp) as timestamp,
               s.title, s.category_code, s.is_threat
        FROM user_attempts a
        JOIN scenarios s ON a.scenario_id = s.id
        WHERE a.user_id = ?
        ORDER BY a.id DESC
    """, (user_id,)).fetchall()

    attempts = []
    for r in rows:
        attempts.append({
            "id": r["id"],
            "scenario_id": r["scenario_id"],
            "user_choice": bool(r["user_choice"]),
            "is_correct": bool(r["is_correct"]),
            "response_time_sec": r["response_time_sec"],
            "timestamp": r["timestamp"],
            "title": r["title"],
            "category_code": r["category_code"],
            "is_threat": bool(r["is_threat"])
        })
    return attempts

def fetch_all_scenarios():
    db = get_db()
    rows = db.execute("SELECT * FROM scenarios").fetchall()
    scenarios = []
    for r in rows:
        scenarios.append({
            "id": r["id"],
            "category_code": r["category_code"],
            "channel": r["channel"],
            "title": r["title"],
            "sender": r["sender"],
            "sender_name": r["sender_name"],
            "subject": r["subject"],
            "body": r["body"],
            "is_threat": bool(r["is_threat"]),
            "difficulty": r["difficulty"],
            "red_flags": json.loads(r["red_flags"]) if r["red_flags"] else [],
            "explanation": r["explanation"],
            "micro_lesson": r["micro_lesson"]
        })
    return scenarios

# ----------------- AUTHENTICATION ROUTES ----------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template('login.html')

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE LOWER(username) = ?", (username,)).fetchone()

        if user:
            # Check password hash (or allow if legacy empty hash)
            pwd_hash = user['password_hash'] if 'password_hash' in user.keys() else ''
            if not pwd_hash or check_password_hash(pwd_hash, password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user['full_name']
                flash(f"Welcome back, {user['full_name']}!", "success")
                return redirect(url_for('index'))

        flash("Invalid username or password. Please try again.", "danger")
        return render_template('login.html')

    return render_template('login.html')

@app.route('/demo-login', methods=['POST'])
def demo_login():
    """Quick 1-click login for demonstration purposes."""
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = 'dhriti'").fetchone()
    if not user:
        # Create demo user if missing
        cur = db.execute("INSERT INTO users (username, full_name, password_hash) VALUES (?, ?, ?)",
                         ('dhriti', 'Ms. Dhriti Gupta', generate_password_hash('password123')))
        db.commit()
        user_id = cur.lastrowid
        session['user_id'] = user_id
        session['username'] = 'dhriti'
        session['full_name'] = 'Ms. Dhriti Gupta'
    else:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']

    flash("Signed in as Demo User (Ms. Dhriti Gupta).", "success")
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not username or not password:
            flash("All fields are required.", "danger")
            return render_template('signup.html')

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "danger")
            return render_template('signup.html')

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template('signup.html')

        if password != confirm_password:
            flash("Passwords do not match. Please re-enter.", "danger")
            return render_template('signup.html')

        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE LOWER(username) = ?", (username,)).fetchone()
        if existing:
            flash("This username is already taken. Please choose another.", "danger")
            return render_template('signup.html')

        pwd_hash = generate_password_hash(password)
        cur = db.execute(
            "INSERT INTO users (username, full_name, password_hash) VALUES (?, ?, ?)",
            (username, full_name, pwd_hash)
        )
        new_user_id = cur.lastrowid

        # Initialize blank profile for new user
        db.execute("""
            INSERT INTO user_profiles (user_id, composite_risk_score, primary_weakness, category_stats, total_tests, accuracy_pct)
            VALUES (?, 50.0, 'Baseline (Not yet evaluated)', '{}', 0, 0.0)
        """, (new_user_id,))
        db.commit()

        # Log in newly created user
        session['user_id'] = new_user_id
        session['username'] = username
        session['full_name'] = full_name

        flash(f"Account successfully created! Welcome, {full_name}!", "success")
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out successfully.", "success")
    return redirect(url_for('login'))

# ----------------- UNIFIED SINGLE-PAGE ROUTE ----------------- #

@app.route('/')
def index():
    user_id = get_current_user_id()
    all_scenarios = fetch_all_scenarios()
    attempts = fetch_user_attempts(user_id)
    profile = fetch_user_profile_data(user_id)

    chosen_scenario, rationale = get_next_adaptive_scenario(all_scenarios, attempts, profile)
    if not chosen_scenario and all_scenarios:
        chosen_scenario = all_scenarios[0]
        rationale = "Initial Diagnostic: Evaluating baseline vigilance."

    return render_template(
        'index.html',
        profile=profile,
        scenario=chosen_scenario,
        adaptive_rationale=rationale,
        attempts=attempts,
        all_scenarios=all_scenarios
    )

# ----------------- JSON API FOR DYNAMIC SINGLE-PAGE UPDATES ----------------- #

@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.get_json(silent=True) or request.form
    user_id = get_current_user_id()
    scenario_id = int(data.get('scenario_id'))
    choice_str = data.get('user_choice', 'safe')
    user_choice = True if choice_str == 'threat' else False

    try:
        response_time = float(data.get('response_time', 5.0))
    except ValueError:
        response_time = 5.0

    db = get_db()
    r = db.execute("SELECT * FROM scenarios WHERE id = ?", (scenario_id,)).fetchone()
    if not r:
        return jsonify({"error": "Scenario not found"}), 404

    scenario = {
        "id": r["id"],
        "category_code": r["category_code"],
        "channel": r["channel"],
        "title": r["title"],
        "sender": r["sender"],
        "sender_name": r["sender_name"],
        "subject": r["subject"],
        "body": r["body"],
        "is_threat": bool(r["is_threat"]),
        "difficulty": r["difficulty"],
        "red_flags": json.loads(r["red_flags"]) if r["red_flags"] else [],
        "explanation": r["explanation"],
        "micro_lesson": r["micro_lesson"]
    }

    is_correct = (user_choice == scenario["is_threat"])

    # 1. Record Attempt for the specific active user
    cur = db.execute("""
        INSERT INTO user_attempts (user_id, scenario_id, user_choice, is_correct, response_time_sec)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, scenario_id, 1 if user_choice else 0, 1 if is_correct else 0, response_time))
    db.commit()

    # 2. Recalculate Cognitive Risk Profile for this specific user
    all_attempts = fetch_user_attempts(user_id)
    new_profile = calculate_user_risk_profile(all_attempts)

    # 3. Update Profile Table
    db.execute("""
        UPDATE user_profiles
        SET composite_risk_score = ?,
            primary_weakness = ?,
            category_stats = ?,
            total_tests = ?,
            accuracy_pct = ?,
            last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (
        new_profile["composite_risk_score"],
        new_profile["primary_weakness"],
        json.dumps(new_profile["category_stats"]),
        new_profile["total_tests"],
        new_profile["accuracy_pct"],
        user_id
    ))
    db.commit()

    # 4. Generate Explainable AI Feedback
    feedback = generate_explainable_feedback(scenario, user_choice, is_correct, response_time)

    # 5. Determine Next Adaptive Scenario
    all_scenarios = fetch_all_scenarios()
    next_scenario, next_rationale = get_next_adaptive_scenario(all_scenarios, all_attempts, new_profile)

    return jsonify({
        "success": True,
        "feedback": feedback,
        "profile": new_profile,
        "next_scenario": next_scenario,
        "next_rationale": next_rationale,
        "attempts": all_attempts
    })

@app.route('/api/scenario/<int:scenario_id>', methods=['GET'])
def api_get_scenario(scenario_id):
    all_scenarios = fetch_all_scenarios()
    matched = next((s for s in all_scenarios if s["id"] == scenario_id), None)
    if not matched:
        return jsonify({"error": "Scenario not found"}), 404
    return jsonify({
        "scenario": matched,
        "rationale": f"Targeted inspection of Scenario #{scenario_id} ({matched['category_code']})"
    })

@app.route('/api/category/<string:cat_code>', methods=['GET'])
def api_get_by_category(cat_code):
    all_scenarios = fetch_all_scenarios()
    cat_scenarios = [s for s in all_scenarios if s["category_code"] == cat_code.upper()]
    if not cat_scenarios:
        return jsonify({"error": "No scenarios in category"}), 404
    chosen = cat_scenarios[0]
    return jsonify({
        "scenario": chosen,
        "rationale": f"Focused Practice Drill on '{cat_code.upper()}' vectors."
    })

@app.route('/api/reset', methods=['POST'])
def api_reset():
    user_id = get_current_user_id()
    db = get_db()
    db.execute("DELETE FROM user_attempts WHERE user_id = ?", (user_id,))
    db.execute("""
        UPDATE user_profiles
        SET composite_risk_score = 50.0,
            primary_weakness = 'Baseline (Not yet evaluated)',
            category_stats = '{}',
            total_tests = 0,
            accuracy_pct = 0.0,
            last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (user_id,))
    db.commit()

    all_scenarios = fetch_all_scenarios()
    new_profile = {
        "composite_risk_score": 50.0,
        "primary_weakness": "Baseline (Not yet evaluated)",
        "category_stats": {},
        "total_tests": 0,
        "accuracy_pct": 0.0,
        "risk_level": "Unrated"
    }
    return jsonify({
        "success": True,
        "profile": new_profile,
        "next_scenario": all_scenarios[0] if all_scenarios else None,
        "next_rationale": "Initial Diagnostic: Establishing your baseline cybersecurity vigilance profile."
    })

# ----------------- LEGACY COMPATIBILITY REDIRECTS ----------------- #

@app.route('/simulate')
@app.route('/profile')
@app.route('/training')
def legacy_redirect():
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_data():
    api_reset()
    return redirect(url_for('index'))

if __name__ == '__main__':
    ensure_tables()
    port = int(os.environ.get('PORT', 5000))
    print(f"Threat Vector AI Server running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
