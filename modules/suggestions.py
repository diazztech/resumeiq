"""
suggestions.py
--------------
Rule-based recommendation engine for ResumeIQ.

Analyzes resume content, structure, contact links, metrics, and missing skills
to provide targeted, prioritized recommendations for college students and job seekers.
"""

import re
from typing import Dict, Any, List
from modules.skills_db import SKILLS_DB


def generate_suggestions(
    resume_text: str,
    match_result: Dict[str, Any],
    word_count: int
) -> List[Dict[str, str]]:
    """
    Evaluates rule-based checks on the resume text and comparison results,
    returning a prioritized list of actionable recommendations.

    Args:
        resume_text: Raw or cleaned text of the resume.
        match_result: The output dictionary from skill_matcher.compare_skills.
        word_count: Total word count in the extracted resume.

    Returns:
        List of dicts: [
            {
                "priority": "High" | "Medium" | "Low" | "Info",
                "category": str,
                "title": str,
                "description": str
            }, ...
        ]
    """
    suggestions: List[Dict[str, str]] = []
    text_lower = resume_text.lower()

    missing_skills = match_result.get("missing", [])
    matched_skills = match_result.get("matched", [])
    match_score = match_result.get("match_score", 0)

    # -------------------------------------------------------------------------
    # RULE 1: Missing Skills Grouped by Category (High Priority)
    # -------------------------------------------------------------------------
    if missing_skills:
        # Group missing skills by category for clarity
        grouped_missing: Dict[str, List[str]] = {}
        for skill in missing_skills:
            cat = SKILLS_DB.get(skill, {}).get("category", "General")
            grouped_missing.setdefault(cat, []).append(skill)

        group_summaries = [
            f"{cat}: {', '.join(skills[:4])}{'...' if len(skills) > 4 else ''}"
            for cat, skills in grouped_missing.items()
        ]
        summary_str = " | ".join(group_summaries[:3])

        suggestions.append({
            "priority": "High",
            "category": "Skills Gap",
            "title": f"Address Missing Key Skills ({len(missing_skills)} Missing)",
            "description": (
                f"The job asks for {len(missing_skills)} skills not detected in your resume, "
                f"including: {summary_str}. If you have academic, project, or coursework "
                "experience with any of these technologies, add them to your resume."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 2: Projects Section Check
    # -------------------------------------------------------------------------
    has_projects = bool(re.search(
        r'\b(projects|project work|academic projects|key projects|personal projects|capstone)\b',
        text_lower
    ))
    if not has_projects:
        suggestions.append({
            "priority": "High",
            "category": "Structure",
            "title": "Add a Dedicated 'Projects' Section",
            "description": (
                "No clear projects section was found. Technical recruiters heavily prioritize "
                "hands-on projects. Add 2–3 notable academic, capstone, or personal projects with "
                "tools used, your role, and GitHub repository links."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 3: Skills Section Check
    # -------------------------------------------------------------------------
    has_skills_section = bool(re.search(
        r'\b(skills|technical skills|key competencies|technologies|core competencies|tech stack)\b',
        text_lower
    ))
    if not has_skills_section:
        suggestions.append({
            "priority": "High",
            "category": "Structure",
            "title": "Include a Structured 'Technical Skills' Section",
            "description": (
                "Your resume does not appear to have an explicit 'Technical Skills' heading. "
                "Group your competencies cleanly into categories (e.g. Languages, Frameworks, "
                "Databases, Cloud & Tools) so human readers can quickly verify your toolkit."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 4: Quantified Achievements & Metrics Check
    # -------------------------------------------------------------------------
    metrics_matches = re.findall(
        r'(\b\d+[\d,.]*\s*(?:%|percent|users|x|k|ms|s|hours|stars|\+)\b|\b(?:reduced|increased|improved|boosted|optimized)\b)',
        text_lower
    )
    if len(metrics_matches) < 2:
        suggestions.append({
            "priority": "Medium",
            "category": "Content Quality",
            "title": "Quantify Your Impact With Numbers & Percentages",
            "description": (
                "Your bullet points contain few or no measurable metrics. Use numbers to convey "
                "scale and outcomes (e.g. 'Optimized SQL queries by 30%', 'Served 500+ active users', "
                "or 'Led a team of 4 students to build a full-stack portal')."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 5: Contact Information Checks (Email, Phone, Profiles)
    # -------------------------------------------------------------------------
    has_email = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', resume_text))
    has_phone = bool(re.search(
        r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3,5}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}',
        resume_text
    ))
    has_profile = bool(re.search(r'(github\.com|linkedin\.com|gitlab\.com|portfolio|behance)', text_lower))

    if not has_email:
        suggestions.append({
            "priority": "High",
            "category": "Contact Information",
            "title": "Add a Professional Email Address",
            "description": "No email address was identified. Place an active, professional email in your contact header."
        })

    if not has_phone:
        suggestions.append({
            "priority": "Medium",
            "category": "Contact Information",
            "title": "Add a Contact Phone Number",
            "description": "Ensure your phone number is easily visible at the top of your resume."
        })

    if not has_profile:
        suggestions.append({
            "priority": "Medium",
            "category": "Contact Information",
            "title": "Link Your GitHub and LinkedIn Profiles",
            "description": (
                "No GitHub or LinkedIn links were detected. Adding clickable links to your live "
                "code repositories and LinkedIn profile significantly enhances technical credibility."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 6: Education & Experience Checks
    # -------------------------------------------------------------------------
    has_education = bool(re.search(
        r'\b(education|academic background|degree|b\.tech|bachelor|master|b\.e|m\.tech|b\.sc|university|college|cgpa|gpa)\b',
        text_lower
    ))
    if not has_education:
        suggestions.append({
            "priority": "High",
            "category": "Structure",
            "title": "Add an 'Education' Section",
            "description": (
                "Could not find an Education section. Include your degree, university name, "
                "graduation year, and relevant GPA or marks."
            )
        })

    has_experience = bool(re.search(
        r'\b(experience|work experience|employment|internship|internships|work history|professional background)\b',
        text_lower
    ))
    if not has_experience:
        suggestions.append({
            "priority": "Medium",
            "category": "Structure",
            "title": "Highlight Internships or Practical Experience",
            "description": (
                "No experience or internship section was detected. If you do not have corporate "
                "experience, list technical internships, freelance assignments, club leadership, "
                "or open-source contributions."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 7: Resume Length & Volume Check
    # -------------------------------------------------------------------------
    if word_count < 150:
        suggestions.append({
            "priority": "High",
            "category": "Length & Formatting",
            "title": "Resume Content Appears Too Brief",
            "description": (
                f"Your resume contains only ~{word_count} words. An effective 1-page college "
                "resume typically contains 350 to 600 words to adequately describe coursework, "
                "projects, skills, and accomplishments."
            )
        })
    elif word_count > 900:
        suggestions.append({
            "priority": "Medium",
            "category": "Length & Formatting",
            "title": "Consider Condensing to a 1-Page Format",
            "description": (
                f"Your resume contains ~{word_count} words, which often spills into multiple pages. "
                "For entry-level and college roles, recruiters prefer a crisp, single-page resume."
            )
        })

    # -------------------------------------------------------------------------
    # RULE 8: Honest Keyword Mirroring Tip
    # -------------------------------------------------------------------------
    suggestions.append({
        "priority": "Low",
        "category": "Keyword Optimization",
        "title": "Mirror Job Terminology Accurately & Honestly",
        "description": (
            "When updating your resume, use standard terminology matching the job description "
            "(e.g., if the posting asks for 'RESTful APIs', make sure you mention 'REST APIs' "
            "rather than ambiguous descriptions). Never claim skills you cannot defend in a viva or interview."
        )
    })

    # Sort suggestions by priority order: High -> Medium -> Low -> Info
    priority_order = {"High": 1, "Medium": 2, "Low": 3, "Info": 4}
    suggestions.sort(key=lambda s: priority_order.get(s["priority"], 5))

    return suggestions
