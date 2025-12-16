#  Job Application Email Counter

A lightweight Python tool that scans your Gmail inbox(es) and counts:

- Total job-application–related emails  
- Approximate number of unique job threads (one thread ≈ one application)  
- Across **multiple Gmail accounts** (e.g., personal, university, work)

---

## 🚀 Features

- 🔍 Search for job application confirmation emails using advanced Gmail queries  
- 📆 Supports **date ranges**:
  - `days_back=365` (default)  
  - or `start_date="YYYY/MM/DD"`  
- 👥 Handles **multiple Gmail accounts**, each with its own OAuth token  
- 🔒 Fully secure: all credentials & tokens are excluded from Git  
- 📝 Clean logging with per-account and combined summaries  

---

# 🛠️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/job-app-counter.git
cd job-app-counter
```

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```