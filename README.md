# ResumeIQ – AI-Based Resume Analyzer and Job Matching System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-fitz-blue.svg)](https://pymupdf.readthedocs.io/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Generator-orange.svg)](https://www.reportlab.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A transparent, deterministic, and privacy-preserving resume analysis tool tailored for college students, graduates, and hiring candidates. Upload a text-based PDF resume, supply a target job description, and immediately receive an actionable breakdown of matched skills, missing requirements, structural improvements, and a downloadable PDF audit report.

---

## 📌 Project Overview

**ResumeIQ** addresses the common disconnect between academic resumes and corporate technical job descriptions. Rather than functioning as a black-box machine learning system or sending private candidate resumes to external third-party APIs, ResumeIQ uses a clean, explainable, rule-based keyword matching pipeline.

### 🛡️ Core Honesty & Transparency Rule
Everywhere in this application, the evaluation metric is strictly labeled **Skill Coverage Score**:
> *"This percentage shows how many of the job's required skills were found in your resume using keyword matching. It is not a real ATS score or a hiring prediction."*

---

## 🚀 Key Features

1. **Deterministic PDF Text Extraction:**
   - Powered by **PyMuPDF (`pymupdf` / `fitz`)**.
   - Robust error handling for corrupt documents, empty files, and scanned image-only PDFs.
2. **Master Skills Taxonomy (200+ Skills):**
   - Curated into 7 categories: Programming Languages, Web Development, Databases, Data Science & ML, Cloud & DevOps, Developer Tools, and Soft Skills.
   - Comprehensive alias mapping (e.g., `js` -> `JavaScript`, `k8s` -> `Kubernetes`, `ci/cd` -> `CI/CD`).
3. **Boundary-Safe Matching Engine:**
   - Compiled regular expressions with negative lookarounds `(?<![a-zA-Z0-9_])alias(?![a-zA-Z0-9_])`.
   - Prevents substring false positives (`Java` inside `JavaScript`) and safely parses symbols like `C++`, `C#`, and `.NET`.
4. **Interactive SaaS Results Dashboard:**
   - Color-coded circular SVG match gauge (<40% Red, 40-70% Orange, >70% Green).
   - Matched skills badges (Green), Missing skills badges (Red), and Extra skills (Slate).
   - Category coverage horizontal bar chart generated dynamically via Matplotlib.
5. **Rule-Based Improvement Suggestions:**
   - Evaluates missing skills grouped by category, dedicated projects section, quantified metrics (numbers and percentages), contact info (email, phone, LinkedIn/GitHub), education, experience, and length guidelines.
6. **Downloadable Branded PDF Reports:**
   - High-quality, multi-page PDF generation via **ReportLab Platypus**.
   - Custom dynamic `NumberedCanvas` for running footers (`Page X of Y`).
7. **Local History Persistence:**
   - Save, inspect, delete, and clear past evaluations via `data/history.json`.
   - Automatic crash recovery and corrupt file backup.

---

## 📂 Project Structure

```text
resumeiq/
├── app.py                  # Streamlit entry point, page routing, top navigation bar
├── pages_ui/
│   ├── home.py             # Landing page with hero section, SVG illustration, feature cards
│   ├── analyze.py          # Form page with input validation, sample loader, extraction triggers
│   ├── results.py          # Results dashboard with circular gauge, badges, chart, PDF download
│   ├── history.py          # Audit history page with view/delete/clear controls
│   ├── how_it_works.py     # Pipeline explanation and limitations of keyword matching
│   └── about.py            # Project purpose, tech stack, and editable viva configuration
├── modules/
│   ├── pdf_extractor.py    # PyMuPDF text extraction, normalization, and error checks
│   ├── skills_db.py        # Master dictionary of 200+ skills with aliases and categories
│   ├── skill_matcher.py    # Boundary-safe regex skill extractor, matcher, and scoring
│   ├── suggestions.py      # Rule-based recommendations engine
│   ├── report_generator.py # Professional multi-page ReportLab PDF report builder
│   └── history_manager.py  # Safe JSON persistence with crash recovery
├── styles/
│   └── style.css           # Custom CSS for modern SaaS aesthetic (typography, gradients, cards)
├── data/
│   └── history.json        # Persistent JSON history storage (auto-created)
├── reports/                # Generated PDF analysis reports (auto-created)
├── sample_data/
│   ├── sample_job_description.txt    # Realistic Full-Stack Python job description
│   ├── sample_resume.pdf             # Realistic student resume generated with ReportLab
│   ├── scanned_or_empty_sample.pdf   # Test PDF with 0 selectable text
│   ├── corrupt_sample.pdf            # Test corrupt non-PDF file
│   └── create_sample_resumes.py      # Utility script to generate test PDFs
├── tests/
│   └── test_backend.py     # Comprehensive automated test suite for all modules
├── requirements.txt        # Pinned dependency requirements
└── README.md               # Complete project documentation
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your computer.

### 2. Clone or Navigate to the Workspace
```bash
cd C:\Users\Admin\.gemini\antigravity\scratch\resumeiq
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Running the Application

Launch the Streamlit web application with:

```bash
streamlit run app.py
```

Open your web browser and navigate to `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the backend unit test suite to verify all modules, regex safety, scoring math, and PDF generation:

```bash
python -m unittest tests/test_backend.py
```

---

## 📊 How the Scoring Engine Works

The Skill Coverage Score is calculated deterministically:

$$\text{Skill Coverage Score} = \left( \frac{\text{Number of Matched Skills}}{\text{Total Required Skills in Job Posting}} \right) \times 100$$

### Example:
- **Target Job Requires 10 Skills:** Python, Django, REST API, PostgreSQL, Docker, Git, AWS, Kubernetes, Linux, Redis.
- **Candidate Resume Contains 8 Skills:** Python, Django, REST API, PostgreSQL, Docker, Git, Linux, Redis.
- **Matched Skills:** 8
- **Missing Skills:** 2 (AWS, Kubernetes)
- **Score:** $(8 / 10) \times 100 = 80\%$ (Color: Emerald Green, Verdict: *Strong Keyword Alignment*).

If the job posting contains no recognizable skills, the system displays an informative notice and sets score to 0%.

---

## ⚠️ Limitations of Keyword Matching

1. **Keyword Presence vs. Real Mastery:**
   - A candidate mentioning "Python" once in coursework receives the same keyword match as someone with 4 years of production experience.
2. **Context Blindness:**
   - A line saying "Planned to learn Kubernetes next semester" will trigger a keyword match for Kubernetes.
3. **Proprietary Commercial ATS Divergence:**
   - Commercial applicant tracking systems (e.g. Workday, Greenhouse) utilize proprietary ranking criteria. ResumeIQ is an educational, rule-based auditor, **not an official ATS emulator**.

---

## 🔮 Future Enhancements

- **Synonym Expansion:** Add support for regional variations in degree titles and terminology.
- **Section Parsing:** Parse and weight skills found within project bullet points higher than general lists.
- **Export Formats:** Add export to Markdown or JSON in addition to ReportLab PDF.
