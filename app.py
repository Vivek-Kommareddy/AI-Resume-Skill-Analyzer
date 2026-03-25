from __future__ import annotations

import streamlit as st

from skill_builder import ResumeSkillBuilder


st.set_page_config(page_title="Resume Skill Builder", page_icon="📄", layout="wide")

builder = ResumeSkillBuilder()

st.title("📄 Resume Skill Builder")
st.write(
    "Compare a resume against a job description, identify matching skills, and find the most visible gaps."
)

with st.sidebar:
    st.header("How to use")
    st.markdown(
        """
        1. Paste your resume text.
        2. Paste a job description.
        3. Click **Analyze Resume**.
        4. Review the score, skill match, and summary.
        """
    )

sample_resume = """Senior Software Engineer with experience in Python, Java, React, SQL, AWS, Docker, Git, REST API, Pandas, scikit-learn, Agile, and mentoring cross-functional teams."""
sample_jd = """We are hiring a Software Engineer with experience in Python, React, AWS, Docker, CI/CD, REST API, microservices, PostgreSQL, Agile, communication, and machine learning."""

col1, col2 = st.columns(2)

with col1:
    resume_text = st.text_area("Paste Resume Text", value=sample_resume, height=320)

with col2:
    jd_text = st.text_area("Paste Job Description", value=sample_jd, height=320)

if st.button("Analyze Resume", type="primary"):
    if not resume_text.strip() or not jd_text.strip():
        st.error("Please provide both resume text and job description text.")
    else:
        result = builder.analyze(resume_text, jd_text)

        st.subheader("Match Score")
        st.progress(min(result["match_score"], 100))
        st.metric("Overall Skill Match", f"{result['match_score']}%")

        a, b, c = st.columns(3)
        a.metric("Matched Skills", len(result["matched_skills"]))
        b.metric("Missing Skills", len(result["missing_skills"]))
        c.metric("Extra Resume Skills", len(result["extra_skills"]))

        tab1, tab2, tab3, tab4 = st.tabs([
            "Skill Overview",
            "Grouped Gaps",
            "Suggested Summary",
            "Keyword Density",
        ])

        with tab1:
            left, right = st.columns(2)
            with left:
                st.markdown("### Matched Skills")
                if result["matched_skills"]:
                    st.write(", ".join(result["matched_skills"]))
                else:
                    st.info("No overlapping skills were detected.")

                st.markdown("### Extra Resume Skills")
                if result["extra_skills"]:
                    st.write(", ".join(result["extra_skills"]))
                else:
                    st.info("No additional skills detected beyond the job description.")

            with right:
                st.markdown("### Missing Skills")
                if result["missing_skills"]:
                    st.write(", ".join(result["missing_skills"]))
                else:
                    st.success("No obvious skill gaps found from the tracked catalog.")

        with tab2:
            st.markdown("### Missing Skills by Category")
            grouped = result["grouped_missing_skills"]
            if grouped:
                for category, skills in grouped.items():
                    st.markdown(f"**{category}**")
                    st.write(", ".join(skills))
            else:
                st.success("No grouped gaps found.")

        with tab3:
            st.markdown("### Suggested Professional Summary")
            st.code(result["suggested_summary"], language="text")

        with tab4:
            left, right = st.columns(2)
            with left:
                st.markdown("### Resume Keywords")
                if result["resume_keyword_density"]:
                    st.dataframe(result["resume_keyword_density"], use_container_width=True)
                else:
                    st.info("No keyword data available.")
            with right:
                st.markdown("### Job Description Keywords")
                if result["jd_keyword_density"]:
                    st.dataframe(result["jd_keyword_density"], use_container_width=True)
                else:
                    st.info("No keyword data available.")
