# AI Resume Skill Builder

A lightweight NLP-based application that analyzes a resume against a job description, identifies skill gaps, and provides actionable suggestions to improve job alignment.

---

## Overview

This project is designed to help users understand how well their resume matches a given job description. It performs basic Natural Language Processing (NLP) to extract skills, compare them, and highlight missing areas.

The goal is to simulate a simplified version of how resume screening tools evaluate candidate profiles.

---

## What This Project Does

- Takes **resume text** and a **job description**
- Extracts relevant technical skills from both inputs
- Compares the two sets of skills
- Calculates a **match score**
- Identifies:
  - matched skills
  - missing skills
- Provides **simple improvement suggestions**

---

## AI / NLP Approach Used

This project uses **basic Natural Language Processing techniques** instead of heavy ML models.

### Techniques implemented:

- **Text Normalization**
  - Lowercasing
  - Cleaning using regex
  - Removing unwanted characters

- **Keyword-Based Skill Extraction**
  - Predefined list of skills (Python, Java, AWS, etc.)
  - Matching skills using text search

- **Set-Based Comparison**
  - Finds intersection (matched skills)
  - Finds difference (missing skills)

- **Rule-Based Scoring**
  - Match Score = (matched skills / total JD skills) × 100

- **Heuristic Suggestions**
  - Generates recommendations based on missing skills

---

## Why This Is Considered AI

This project applies **NLP techniques on unstructured text data** (resume and job description), which is a fundamental part of AI systems used in:

- Resume screening tools
- Applicant Tracking Systems (ATS)
- Job recommendation platforms

It focuses on **practical, interpretable AI logic**, rather than complex deep learning models.

---

## Project Structure

```
resume_skill_builder/
│── app.py
│── skill_builder.py
│── requirements.txt
│── README.md
```

---

## Tech Stack

- Python
- Streamlit
- Regular Expressions (re)
- Basic NLP techniques

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/vivek-kommareddy/resume-skill-builder.git
cd resume-skill-builder
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## Example Output

- Match Score: 65%
- Matched Skills: Python, SQL
- Missing Skills: Docker, Kubernetes, AWS

Suggestions:
- Add missing skills in project descriptions
- Highlight backend and cloud experience
- Align resume keywords with job description

---

## Limitations

- Does not use machine learning models
- Relies on predefined skill lists
- No semantic understanding of context
- Text input only (no PDF/DOCX parsing)

---

## Future Improvements

- Add TF-IDF or embeddings for better matching
- Support PDF/DOCX resume upload
- Improve skill extraction using NLP libraries
- Add role-specific recommendations

---

## Resume Description

Built a Python-based NLP application using Streamlit to analyze resumes against job descriptions, extract skills, identify gaps, and generate improvement suggestions using rule-based text processing techniques.

---

## License

For educational and portfolio use.
