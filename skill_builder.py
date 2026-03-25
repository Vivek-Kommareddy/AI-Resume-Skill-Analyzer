from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict, List, Set


class ResumeSkillBuilder:
    """A lightweight resume-to-job-description skill gap analyzer.

    The project is intentionally simple so it is easy to run, read, and extend.
    It avoids external ML dependencies and uses clean Python-only text matching.
    """

    def __init__(self) -> None:
        self.skill_catalog: Dict[str, List[str]] = {
            "Programming Languages": [
                "python", "java", "javascript", "typescript", "sql", "c", "c++", "c#", "go", "ruby"
            ],
            "Web & API": [
                "html", "css", "react", "angular", "node.js", "nodejs", "express", "rest api",
                "graphql", "fastapi", "flask", "django", "spring", "spring boot", "microservices"
            ],
            "Cloud & DevOps": [
                "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "git",
                "github actions", "ci/cd", "linux"
            ],
            "Data & AI": [
                "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "machine learning",
                "deep learning", "nlp", "llm", "data analysis", "data visualization", "power bi"
            ],
            "Databases": [
                "mysql", "postgresql", "mongodb", "oracle", "redis", "snowflake", "dynamodb"
            ],
            "Professional Skills": [
                "agile", "scrum", "leadership", "communication", "problem solving", "mentoring",
                "stakeholder management", "team collaboration"
            ],
        }

    def _normalize(self, text: str) -> str:
        """Normalize text for easier matching.

        The regex keeps letters, numbers, whitespace, and a few symbols commonly
        found in technical terms. The hyphen is placed at the end of the class
        to avoid the bad character range regex error.
        """
        text = text.lower()
        text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _generate_variants(self, skill: str) -> Set[str]:
        skill = skill.lower().strip()
        variants = {skill}

        replacements = {
            "node.js": ["node js", "nodejs"],
            "scikit-learn": ["sklearn", "scikit learn"],
            "c#": ["c sharp"],
            "c++": ["cpp"],
            "rest api": ["rest apis", "restful api", "restful apis"],
            "ci/cd": ["cicd", "ci cd"],
            "machine learning": ["ml"],
            "deep learning": ["dl"],
            "artificial intelligence": ["ai"],
            "llm": ["large language model", "large language models"],
            "github actions": ["github action"],
            "microservices": ["microservice"],
        }

        for key, values in replacements.items():
            if skill == key:
                variants.update(values)

        variants.add(skill.replace("-", " "))
        return {self._normalize(v) for v in variants if v.strip()}

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        normalized = self._normalize(text)
        detected: Dict[str, List[str]] = {}

        for category, skills in self.skill_catalog.items():
            matches: List[str] = []
            for skill in skills:
                variants = self._generate_variants(skill)
                for variant in variants:
                    pattern = rf"(?<!\w){re.escape(variant)}(?!\w)"
                    if re.search(pattern, normalized):
                        matches.append(skill)
                        break
            if matches:
                detected[category] = sorted(set(matches))

        return detected

    def flatten_skills(self, categorized_skills: Dict[str, List[str]]) -> Set[str]:
        flat: Set[str] = set()
        for skills in categorized_skills.values():
            flat.update(skills)
        return flat

    def calculate_match_score(self, resume_skills: Set[str], jd_skills: Set[str]) -> int:
        if not jd_skills:
            return 0
        overlap = len(resume_skills & jd_skills)
        return round((overlap / len(jd_skills)) * 100)

    def grouped_missing_skills(self, resume_text: str, jd_text: str) -> Dict[str, List[str]]:
        resume_detected = self.extract_skills(resume_text)
        jd_detected = self.extract_skills(jd_text)
        resume_flat = self.flatten_skills(resume_detected)

        grouped: Dict[str, List[str]] = {}
        for category, skills in jd_detected.items():
            missing = sorted([skill for skill in skills if skill not in resume_flat])
            if missing:
                grouped[category] = missing
        return grouped

    def suggest_summary(self, matched_skills: Set[str], missing_skills: Set[str]) -> str:
        matched_list = sorted(matched_skills)[:8]
        missing_list = sorted(missing_skills)[:4]

        summary = (
            "Results-driven software professional with hands-on experience in "
            f"{', '.join(matched_list) if matched_list else 'modern application development'}"
            ". Skilled at building reliable solutions, collaborating across teams, and aligning technical delivery "
            "with business needs."
        )

        if missing_list:
            summary += (
                " Currently strengthening capabilities in "
                f"{', '.join(missing_list)} to better align with target roles."
            )

        return summary

    def keyword_density(self, text: str) -> List[Dict[str, int]]:
        normalized = self._normalize(text)
        tokens = normalized.split()
        counts = Counter(tokens)
        rows: List[Dict[str, int]] = []
        for word, count in counts.most_common(15):
            if len(word) > 2 and not word.isdigit():
                rows.append({"keyword": word, "count": count})
        return rows

    def analyze(self, resume_text: str, jd_text: str) -> Dict[str, object]:
        resume_skills_by_category = self.extract_skills(resume_text)
        jd_skills_by_category = self.extract_skills(jd_text)

        resume_skills = self.flatten_skills(resume_skills_by_category)
        jd_skills = self.flatten_skills(jd_skills_by_category)

        matched_skills = sorted(resume_skills & jd_skills)
        missing_skills = sorted(jd_skills - resume_skills)
        extra_skills = sorted(resume_skills - jd_skills)

        return {
            "match_score": self.calculate_match_score(resume_skills, jd_skills),
            "resume_skills_by_category": resume_skills_by_category,
            "jd_skills_by_category": jd_skills_by_category,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills,
            "grouped_missing_skills": self.grouped_missing_skills(resume_text, jd_text),
            "suggested_summary": self.suggest_summary(set(matched_skills), set(missing_skills)),
            "resume_keyword_density": self.keyword_density(resume_text),
            "jd_keyword_density": self.keyword_density(jd_text),
        }
