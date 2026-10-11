# Threat Vector — AI-Based Adaptive Social Engineering Threat Detection and Awareness System

**Student / Lead:** Ms. Dhriti Gupta  
**Team Name:** Threat Vector  
**Technologies:** Python 3.14, Flask, SQLite, Scikit-Learn, HTML5, CSS3, JavaScript (Chart.js), Gunicorn

---

## 🌟 Project Overview

Traditional cybersecurity training gives everyone the same generic guidelines. **Threat Vector** is an intelligent awareness platform featuring a **formal corporate light theme**:
1. **User Authentication & Multi-User Profiles**: Secure Login (`/login`) & Registration (`/signup`) where each user has their own personal risk scoring, history, and weakness vectors.
2. **Multi-Channel Social Engineering Simulations**: Realistic corporate emails, courier SMS alerts, and IT helpdesk chat pretexts.
3. **Cognitive Vulnerability Quantification**: Tracks decision accuracy and reaction speed across 5 psychological attack vectors:
   - ⚡ **Urgency & Time Pressure**
   - 👔 **Authority Impersonation**
   - 🔗 **Typosquatting & Fake Links**
   - 🎁 **Incentive & Greed Traps**
   - ⚠️ **Coercion & Legal Threats**
4. **Machine Learning (Scikit-Learn)**: Evaluates lexical features, domain threat indicators, and predicts threat likelihood with Random Forest classification.
5. **Explainable AI (XAI) Feedback**: Transparent breakdown of psychological triggers, domain flaws, and defensive protocols.
6. **Adaptive Training Loops**: Dynamically prioritizes drills targeting the active user's specific weaknesses.

---

## 🚀 How to Run Locally

### Option 1: 1-Click Batch Launcher (Easiest)
Simply double-click **`start_threat_vector.bat`** in your project folder. It launches the server and opens your browser automatically!

### Option 2: Command Line
```bash
python app.py
```
Then open: **[http://localhost:5000](http://localhost:5000)**

---

## 🌐 How to Get a Real Public Web Link (Free Hosting)

### Method 1: Instant 10-Second Public Link (No Signup Needed)
To instantly open the project on your phone, tablet, or send a live link to your teacher right now:
1. Double-click **`get_free_public_link.bat`** in your project folder.
2. It generates a free, live **`https://xxxx.a.pinggy.link`** public URL.
3. Anyone in the world can open that URL on any device!

---

### Method 2: Permanent Free Cloud Hosting on Render.com
To host it permanently online with a custom URL (e.g., `https://threat-vector.onrender.com`):
1. **Push your code to GitHub**:
   - Create a free GitHub repository at [github.com/new](https://github.com/new).
   - Upload this folder to GitHub.
2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign up for a free account.
   - Click **"New +"** ➔ **"Web Service"**.
   - Select your GitHub repository.
   - Render will detect the included `render.yaml` and `Procfile` automatically.
   - Build Command: `pip install -r requirements.txt && python data/seed_db.py`
   - Start Command: `gunicorn app:app`
   - Click **"Create Web Service"**.
3. **Your Public Link**:
   Render will deploy your site and give you a permanent live public URL (e.g. `https://threat-vector-app.onrender.com`) that is online 24/7!

---

### Method 3: PythonAnywhere (Alternative Free Host)
1. Sign up for a free account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Go to the **"Web"** tab ➔ Click **"Add a new web app"** ➔ Select **Flask** (Python 3.10+).
3. Upload your project files or clone from GitHub.
4. Your website is immediately live at: `https://<your-username>.pythonanywhere.com`!

---

## 📁 Project Architecture

```text
MDC project/
│
├── app.py                      # Main Flask application, authentication, & JSON API
├── Procfile                    # Cloud deployment process specification (gunicorn)
├── render.yaml                 # 1-Click configuration for Render.com free hosting
├── requirements.txt            # Python dependencies (Flask, scikit-learn, gunicorn)
├── README.md                   # Quickstart instructions
├── PROJECT_BLUEPRINT.md        # Comprehensive blueprint for viva / report
├── threat_vector.db            # SQLite relational database
├── Threat_Vector_Dashboard.html# Standalone 100% offline fallback model
│
├── 📂 data/
│   ├── scenarios.json          # Seed scenarios (Email, SMS, Chat attacks)
│   └── seed_db.py              # Script to reset / seed database
│
├── 📂 database/
│   ├── db.py                   # SQLite connection helpers & table verification
│   ├── schema.sql              # Database schema tables
│   └── migrate_db.py           # Auto-migration script for password hashes
│
├── 📂 ml_engine/
│   ├── feature_extractor.py    # NLP & lexical heuristic feature extractor
│   ├── risk_scorer.py          # Scikit-Learn Random Forest model & Risk Profiler
│   ├── explainability.py       # Explainable AI (XAI) report generator
│   └── adaptive_selector.py    # Weakness-targeted scenario recommender
│
├── 📂 static/
│   ├── css/style.css           # Clean corporate/academic light theme
│   └── js/
│       └── unified_app.js      # Dynamic Single-Page client script
│
└── 📂 templates/
    ├── base.html               # Shared navbar, user session badge, & footer
    ├── login.html              # Clean corporate Sign In page
    ├── signup.html             # Clean corporate Account Registration page
    └── index.html              # Unified Single-Page Platform
```
