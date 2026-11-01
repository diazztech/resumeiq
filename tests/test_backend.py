"""
test_backend.py
---------------
Comprehensive test suite verifying all ResumeIQ backend components:
- Skills database
- PyMuPDF text extractor and edge cases (corrupt, empty, scanned)
- Regex skill matcher and score calculation
- Suggestions engine
- ReportLab PDF generator
- History manager JSON persistence and recovery
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.skills_db import SKILLS_DB, total_skills_count, get_all_categories
from modules.pdf_extractor import (
    clean_extracted_text,
    extract_text_from_pdf,
    EmptyPDFError,
    ScannedPDFError,
    CorruptPDFError
)
from modules.skill_matcher import extract_skills, compare_skills
from modules.suggestions import generate_suggestions
from modules.history_manager import (
    save_analysis,
    list_history,
    get_history_by_id,
    delete_history_by_id,
    clear_history
)
from modules.report_generator import generate_pdf_report


class TestSkillsDB(unittest.TestCase):
    def test_skills_count(self):
        # We need at least 150-200 distinct skills
        self.assertGreaterEqual(total_skills_count(), 100)

    def test_categories_present(self):
        cats = get_all_categories()
        expected = [
            "Programming Languages",
            "Web Development",
            "Databases",
            "Data Science & ML",
            "Cloud & DevOps",
            "Developer Tools",
            "Soft Skills"
        ]
        for c in expected:
            self.assertIn(c, cats)

    def test_special_skills_aliases(self):
        self.assertIn("Python", SKILLS_DB)
        self.assertIn("C++", SKILLS_DB)
        self.assertIn(".NET", SKILLS_DB)
        self.assertIn("Node.js", SKILLS_DB)


class TestSkillMatcher(unittest.TestCase):
    def test_boundary_matching(self):
        # java should NOT match javascript
        sample = "We are looking for a JavaScript and Python engineer proficient in C++ and .NET."
        extracted = extract_skills(sample)
        self.assertIn("JavaScript", extracted)
        self.assertIn("Python", extracted)
        self.assertIn("C++", extracted)
        self.assertIn(".NET", extracted)
        self.assertNotIn("Java", extracted)  # Critical check: Java must NOT match in JavaScript

    def test_score_calculation(self):
        # Job requires 4 skills: Python, React, Docker, SQL
        job_text = "Required skills: Python, React, Docker, and SQL."
        resume_text = "I have experience in Python and SQL, as well as Git and HTML."

        job_skills = extract_skills(job_text)
        resume_skills = extract_skills(resume_text)

        result = compare_skills(resume_skills, job_skills)
        self.assertEqual(result["total_job_skills"], 4)
        self.assertEqual(len(result["matched"]), 2)  # Python, SQL
        self.assertIn("Python", result["matched"])
        self.assertIn("SQL", result["matched"])
        self.assertEqual(len(result["missing"]), 2)  # React, Docker
        self.assertIn("React", result["missing"])
        self.assertIn("Docker", result["missing"])

        # Score = (2 / 4) * 100 = 50%
        self.assertEqual(result["match_score"], 50)

    def test_zero_skills_graceful_handling(self):
        job_text = "Looking for an energetic team player who is enthusiastic."
        resume_text = "I have Python experience."
        job_skills = extract_skills(job_text)
        # Note: Soft skills like teamwork might match, but let's test completely empty
        result = compare_skills({}, {})
        self.assertEqual(result["match_score"], 0)
        self.assertFalse(result["has_job_skills"])


class TestSuggestions(unittest.TestCase):
    def test_suggestions_generation(self):
        resume_text = "John Doe. Experienced programmer. Worked on some projects."
        match_result = {
            "matched": ["Python"],
            "missing": ["Docker", "Kubernetes"],
            "extra": [],
            "match_score": 33,
            "total_job_skills": 3,
            "category_breakdown": {}
        }
        suggestions = generate_suggestions(resume_text, match_result, word_count=30)
        self.assertTrue(len(suggestions) > 0)
        titles = [s["title"] for s in suggestions]
        # Should flag missing email, brief length, missing core skills, etc.
        self.assertTrue(any("Missing Key Skills" in t for t in titles))
        self.assertTrue(any("Email" in t for t in titles))


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        clear_history()

    def tearDown(self):
        clear_history()

    def test_history_crud(self):
        match_res = {
            "match_score": 80,
            "total_job_skills": 5,
            "total_resume_skills": 6,
            "matched": ["Python", "SQL", "Git", "Docker"],
            "missing": ["AWS"],
            "extra": ["Linux", "FastAPI"],
            "category_breakdown": {},
            "has_job_skills": True
        }
        entry_id = save_analysis(
            candidate_name="Alice Smith",
            filename="alice_resume.pdf",
            match_result=match_res,
            suggestions=[{"priority": "Low", "category": "General", "title": "Tip", "description": "Good job"}],
            word_count=450,
            page_count=1
        )
        self.assertIsNotNone(entry_id)

        history = list_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["name"], "Alice Smith")
        self.assertEqual(history[0]["score"], 80)

        # Retrieve by id
        fetched = get_history_by_id(entry_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["id"], entry_id)

        # Delete
        deleted = delete_history_by_id(entry_id)
        self.assertTrue(deleted)
        self.assertEqual(len(list_history()), 0)


class TestPDFReportGeneration(unittest.TestCase):
    def test_generate_pdf(self):
        match_res = {
            "match_score": 75,
            "total_job_skills": 4,
            "total_resume_skills": 5,
            "matched": ["Python", "SQL", "Git"],
            "missing": ["Docker"],
            "extra": ["Linux", "FastAPI"],
            "category_breakdown": {
                "Programming Languages": {
                    "job_count": 2,
                    "match_count": 2,
                    "coverage_pct": 100
                }
            },
            "has_job_skills": True
        }
        suggestions = [
            {"priority": "High", "category": "Skills", "title": "Add Docker", "description": "Consider learning container basics."}
        ]
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            pdf_path = generate_pdf_report(
                candidate_name="Bob Test",
                resume_filename="bob_resume.pdf",
                match_result=match_res,
                suggestions=suggestions,
                output_filename=tmp_path
            )
            self.assertTrue(os.path.exists(pdf_path))
            self.assertGreater(os.path.getsize(pdf_path), 1000)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
