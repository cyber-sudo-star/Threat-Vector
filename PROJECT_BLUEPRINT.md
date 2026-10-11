# AI-Based Adaptive Social Engineering Threat Detection & Awareness System
**Project Blueprint & Architectural Specification**  
**Team Name:** Threat Vector  
**Candidate:** Ms. Dhriti Gupta  
**Domain:** Artificial Intelligence, Cybersecurity, Cognitive Risk Analysis  

---

## 1. Executive Summary

Traditional cybersecurity awareness programs rely on generic, one-size-fits-all training modules that employees or students passively consume. This approach produces low retention and fails to address individual psychological vulnerabilities (such as susceptibility to urgency, deference to authority, or blind trust in digital links).

The **Threat Vector** system is an AI-driven, interactive platform that:
1. Simulates realistic social engineering scenarios (phishing emails, SMS alerts, IT helpdesk chat pretexts).
2. Quantifies a user's decision-making behavior to identify distinct cognitive vulnerabilities.
3. Uses machine learning to calculate risk scores and evaluate scenario characteristics.
4. Provides immediate **Explainable AI (XAI)** feedback pointing out exact red flags.
5. Dynamically adapts subsequent training modules to specifically remediate the user's identified weak areas.

---

## 2. System Architecture

```
+-------------------------------------------------------------------------+
|                         PRESENTATION LAYER                              |
|   - Interactive Simulation View (Email / SMS / Chat Mockups)             |
|   - Explainable Feedback Card (Red-Flag Highlights & Guidance)          |
|   - Adaptive Analytics Dashboard (Risk Gauge, Vulnerability Radar Chart)|
+-------------------------------------------------------------------------+
                                    |  HTTP / JSON
                                    v
+-------------------------------------------------------------------------+
|                      APPLICATION LAYER (Python Flask)                   |
|   - Scenario Router & Session Manager                                   |
|   - Assessment Controller (Captures response & dwell time)              |
|   - Profile & Analytics Controller                                      |
+-------------------------------------------------------------------------+
                    |                               |
                    v                               v
+-------------------------------+   +-------------------------------------+
|      AI & ANALYTICS ENGINE    |   |           DATA STORAGE LAYER        |
|  (Scikit-Learn + Heuristics)  |   |               (SQLite)              |
| - Threat Feature Extractor    |   | - Users & Credentials               |
| - Multi-Factor Risk Scorer    |   | - Scenarios & Metadata              |
| - Explainability (XAI) Module |   | - User Attempts & Timestamps        |
| - Adaptive Scenario Recommender|  | - Cognitive Vulnerability Profiles  |
+-------------------------------+   +-------------------------------------+
```

---

## 3. Cognitive Attack Vectors (Categories)

The system classifies all scenarios under 5 primary social-engineering persuasion vectors based on Cialdini's principles of influence:

1. **Urgency / Time Pressure (`URGENCY`)**  
   *Psychological Trigger:* Panic, fear of missing a deadline, rapid action without reflection.  
   *Example:* "Your access expires in 15 minutes. Verify immediately."

2. **Authority / Impersonation (`AUTHORITY`)**  
   *Psychological Trigger:* Deference to bosses, IT departments, police, or university deans.  
   *Example:* "Official Notice from the Dean's Office regarding disciplinary review."

3. **Malicious Links & Typosquatting (`FAKELINKS`)**  
   *Psychological Trigger:* Habitual clicking, disguised hyperlinks, lookalike domains (`goo-gle.co`, `paypa1.com`).  
   *Example:* "Track your courier parcel at `dhl-express-portal.xyz/track`."

4. **Greed / Incentive Traps (`INCENTIVE`)**  
   *Psychological Trigger:* Desire for easy reward, vouchers, scholarships, or free prizes.  
   *Example:* "Congratulations! You have received a $500 campus bookstore voucher."

5. **Fear & Coercion (`COERCION`)**  
   *Psychological Trigger:* Dread of account suspension, legal trouble, or financial penalty.  
   *Example:* "Suspicious login detected from overseas. Your card has been temporarily locked."

---

## 4. How the AI / Adaptive Engine Works

### Step 1: Feature Extraction
When a scenario is evaluated or created, features are extracted:
- **Lexical markers:** Presence of urgency words (`immediately`, `expire`, `urgent`, `suspend`).
- **Domain credibility score:** Checks for mismatched sender vs displayed brand, unfamiliar TLDs (`.xyz`, `.top`, `.tk`).
- **Call-to-Action intensity:** Number of action links, requests for credentials or OTPs.

### Step 2: User Vulnerability Modeling
For every user $u$ and category $c$, the vulnerability score $V(u, c)$ is computed:
$$V(u, c) = \frac{\text{Failed Attempts in Category } c}{\text{Total Attempts in Category } c} \times 100\%$$

### Step 3: Overall Composite Risk Score ($R_u$)
Combines error rate, high-severity category failures, and decision speed:
$$R_u = \sum_{c} w_c \cdot V(u, c)$$
Where $w_c$ is the severity weight of each category.
- **Low Risk (0 - 30):** High cybersecurity vigilance.
- **Moderate Risk (31 - 70):** Susceptible to targeted triggers.
- **High Risk (71 - 100):** Immediate targeted awareness training required.

### Step 4: Adaptive Training Loop
Instead of serving random questions, the **Adaptive Selector**:
1. Checks the user's top 1-2 weakest vulnerability categories.
2. Selects training scenarios that challenge those specific vectors.
3. Provides micro-lessons before re-evaluating to verify retention.

---

## 5. College Evaluation & Viva Defense Talking Points

1. **"What is novel or AI-based about this project vs a simple online quiz?"**  
   *Answer:* A simple quiz gives everyone the same questions and a fixed percentage score. Our system builds a dynamic **Cognitive Risk Profile** for each user, extracts threat features from scenarios, computes vulnerability across attack vectors, and uses an **adaptive recommender algorithm** to dynamically tailor training to individual human weaknesses.

2. **"How do you implement Explainable AI (XAI)?"**  
   *Answer:* When a user fails a scenario, the system does not just say "Wrong". It displays an **Explainability Decomposition**: highlighting the spoofed domain, the psychological urgency pretext, and the missing security hallmarks.

3. **"Why SQLite and Flask?"**  
   *Answer:* Lightweight, self-contained, and perfectly suited for rapid deployment, zero-configuration local evaluation, and seamless demonstration during project review.
