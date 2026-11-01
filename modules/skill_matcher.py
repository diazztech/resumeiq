"""
skill_matcher.py
----------------
Core matching engine for ResumeIQ.

Extracts skills from raw text using boundary-safe regex, compares candidate resume
skills against job description requirements, and calculates the Skill Coverage Score
along with category-level breakdowns.
"""

import re
from typing import Dict, Any, List, Set
from modules.skills_db import SKILLS_DB, get_all_categories


def build_skill_regex_pattern(alias: str) -> re.Pattern:
    """
    Builds a compiled regular expression for a skill alias using lookarounds
    to ensure boundary safety even when symbols like '+', '#', or '.' are present.

    Prevents false positives like:
    - 'java' matching inside 'javascript'
    - 'r' matching arbitrary letters
    - 'c' matching inside other words
    """
    escaped_alias = re.escape(alias)
    # Using negative lookbehind and negative lookahead for alphanumeric characters
    pattern_str = rf"(?<![a-zA-Z0-9_]){escaped_alias}(?![a-zA-Z0-9_])"
    return re.compile(pattern_str, re.IGNORECASE)


# Pre-compile patterns once for optimal runtime performance
COMPILED_SKILL_PATTERNS: List[Dict[str, Any]] = []

for canonical_name, data in SKILLS_DB.items():
    category = data["category"]
    for alias in data["aliases"]:
        COMPILED_SKILL_PATTERNS.append({
            "canonical_name": canonical_name,
            "category": category,
            "alias": alias,
            "pattern": build_skill_regex_pattern(alias)
        })


def extract_skills(text: str) -> Dict[str, Dict[str, str]]:
    """
    Scans a given text (resume or job description) and extracts all matching skills.

    Args:
        text: String containing the document content.

    Returns:
        A dictionary mapping Canonical Skill Name -> {"category": str, "matched_alias": str}
    """
    if not text:
        return {}

    found_skills: Dict[str, Dict[str, str]] = {}

    for item in COMPILED_SKILL_PATTERNS:
        canonical_name = item["canonical_name"]
        if canonical_name in found_skills:
            # Already detected this canonical skill via an earlier alias
            continue

        if item["pattern"].search(text):
            found_skills[canonical_name] = {
                "category": item["category"],
                "matched_alias": item["alias"]
            }

    return found_skills


def compare_skills(
    resume_skills: Dict[str, Dict[str, str]],
    job_skills: Dict[str, Dict[str, str]]
) -> Dict[str, Any]:
    """
    Compares extracted resume skills against extracted job description skills.

    Args:
        resume_skills: Dict of skills found in the resume.
        job_skills: Dict of skills found in the job description.

    Returns:
        A comprehensive analysis dictionary containing:
            - matched: List of skills found in both
            - missing: List of skills present in job but missing from resume
            - extra: List of skills present in resume that job didn't explicitly request
            - total_job_skills: Integer count
            - total_resume_skills: Integer count
            - match_score: Whole-number percentage (0-100)
            - has_job_skills: Boolean flag
            - category_breakdown: Breakdown of matched vs total skills per category
    """
    resume_set: Set[str] = set(resume_skills.keys())
    job_set: Set[str] = set(job_skills.keys())

    matched_set = resume_set.intersection(job_set)
    missing_set = job_set - resume_set
    extra_set = resume_set - job_set

    total_job_skills = len(job_set)
    total_matched = len(matched_set)

    # Calculate Skill Coverage Score:
    # Score = (matched job skills / total job skills) * 100
    if total_job_skills > 0:
        match_score = round((total_matched / total_job_skills) * 100)
    else:
        # Gracefully handle the zero-skills case when job description has no keywords
        match_score = 0

    # Sort skill lists alphabetically for tidy presentation
    matched_list = sorted(list(matched_set))
    missing_list = sorted(list(missing_set))
    extra_list = sorted(list(extra_set))

    # Category Breakdown Calculation
    all_cats = get_all_categories()
    category_breakdown: Dict[str, Dict[str, Any]] = {}

    for cat in all_cats:
        # Collect job skills in this category
        cat_job_skills = [s for s in job_set if SKILLS_DB[s]["category"] == cat]
        cat_matched_skills = [s for s in matched_set if SKILLS_DB[s]["category"] == cat]
        cat_missing_skills = [s for s in missing_set if SKILLS_DB[s]["category"] == cat]
        cat_extra_skills = [s for s in extra_set if SKILLS_DB[s]["category"] == cat]

        job_count = len(cat_job_skills)
        match_count = len(cat_matched_skills)
        cat_score = round((match_count / job_count) * 100) if job_count > 0 else 0

        # Only store or display categories that have relevant skills (in job or resume)
        if job_count > 0 or len(cat_extra_skills) > 0:
            category_breakdown[cat] = {
                "job_skills": sorted(cat_job_skills),
                "matched_skills": sorted(cat_matched_skills),
                "missing_skills": sorted(cat_missing_skills),
                "extra_skills": sorted(cat_extra_skills),
                "job_count": job_count,
                "match_count": match_count,
                "coverage_pct": cat_score
            }

    return {
        "matched": matched_list,
        "missing": missing_list,
        "extra": extra_list,
        "total_job_skills": total_job_skills,
        "total_resume_skills": len(resume_set),
        "match_score": match_score,
        "has_job_skills": total_job_skills > 0,
        "category_breakdown": category_breakdown,
        "matched_details": {s: resume_skills[s] for s in matched_list},
        "missing_details": {s: job_skills[s] for s in missing_list},
        "extra_details": {s: resume_skills[s] for s in extra_list}
    }
