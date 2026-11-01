"""
test_full_app_flow.py
---------------------
End-to-end integration and verification script for ResumeIQ.
Tests:
1. Module imports and page rendering modules
2. Real analysis pipeline with sample resume and sample job description
3. Exact score calculation and manual mathematical verification
4. Scanned PDF error detection
5. Corrupt PDF error detection
6. Empty PDF error detection
7. PDF report generation and verifying the output PDF opens with PyMuPDF
8. History manager save, list, get, delete, and clear operations
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding if needed
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pymupdf as fitz
from modules.pdf_extractor import (
    extract_text_from_pdf,
    EmptyPDFError,
    CorruptPDFError,
    ScannedPDFError
)
from modules.skill_matcher import extract_skills, compare_skills
from modules.suggestions import generate_suggestions
from modules.report_generator import generate_pdf_report
from modules.history_manager import (
    save_analysis,
    list_history,
    get_history_by_id,
    delete_history_by_id,
    clear_history
)


def test_end_to_end():
    print("=================================================================")
    print("Starting ResumeIQ End-to-End System Tests...")
    print("=================================================================")

    # 1. Clean history to start fresh
    clear_history()
    assert len(list_history()) == 0, "History should be empty after clear"
    print("[PASS] History clean state verified.")

    # 2. Test Scanned / Empty PDF Detection
    scanned_path = PROJECT_ROOT / "sample_data" / "scanned_or_empty_sample.pdf"
    try:
        extract_text_from_pdf(str(scanned_path))
        assert False, "Should have raised ScannedPDFError"
    except ScannedPDFError as e:
        print(f"[PASS] Scanned PDF successfully detected and caught: {type(e).__name__}")

    # 3. Test Corrupt PDF Detection
    corrupt_path = PROJECT_ROOT / "sample_data" / "corrupt_sample.pdf"
    try:
        extract_text_from_pdf(str(corrupt_path))
        assert False, "Should have raised CorruptPDFError"
    except CorruptPDFError as e:
        print(f"[PASS] Corrupt PDF successfully detected and caught: {type(e).__name__}")

    # 4. Test Zero-byte Empty PDF Detection
    try:
        extract_text_from_pdf(b"")
        assert False, "Should have raised EmptyPDFError"
    except EmptyPDFError as e:
        print(f"[PASS] Zero-byte PDF successfully detected and caught: {type(e).__name__}")

    # 5. Test Realistic Resume Text Extraction
    resume_path = PROJECT_ROOT / "sample_data" / "sample_resume.pdf"
    assert resume_path.exists(), "sample_resume.pdf must exist"

    pdf_info = extract_text_from_pdf(str(resume_path))
    resume_text = pdf_info["text"]
    word_count = pdf_info["word_count"]
    page_count = pdf_info["page_count"]

    assert len(resume_text) > 100, "Extracted resume text must not be empty"
    assert word_count > 50, f"Expected > 50 words, got {word_count}"
    assert page_count >= 1, "Page count must be >= 1"
    print(f"[PASS] Text extracted: {word_count} words across {page_count} page(s).")

    # 6. Test Job Description & Skill Matching
    jd_path = PROJECT_ROOT / "sample_data" / "sample_job_description.txt"
    with open(jd_path, "r", encoding="utf-8") as f:
        job_description_text = f.read()

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description_text)

    print(f"  * Distinct skills in Resume: {len(resume_skills)}")
    print(f"  * Distinct skills in Job Description: {len(job_skills)}")

    match_result = compare_skills(resume_skills, job_skills)
    matched = match_result["matched"]
    missing = match_result["missing"]
    extra = match_result["extra"]
    total_job_skills = match_result["total_job_skills"]
    calculated_score = match_result["match_score"]

    # 7. Verify Mathematical Score by Hand
    # Mathematical formula: round((len(matched) / total_job_skills) * 100)
    expected_score = round((len(matched) / total_job_skills) * 100)
    assert calculated_score == expected_score, f"Math mismatch: got {calculated_score}, expected {expected_score}"
    assert len(matched) + len(missing) == total_job_skills, "Matched + Missing must equal total job skills"
    print(f"[PASS] Score Math Verified: {len(matched)} matched / {total_job_skills} total = {calculated_score}%")
    print(f"  * Matched ({len(matched)}): {', '.join(matched)}")
    print(f"  * Missing ({len(missing)}): {', '.join(missing)}")

    # 8. Test Suggestions Engine
    suggestions = generate_suggestions(resume_text, match_result, word_count)
    assert len(suggestions) > 0, "Suggestions should be generated"
    print(f"[PASS] Generated {len(suggestions)} rule-based suggestions.")
    for sug in suggestions[:3]:
        print(f"    - [{sug['priority']}] {sug['title']}")

    # 9. Test PDF Report Generation
    test_report_name = PROJECT_ROOT / "reports" / "test_verification_report.pdf"
    if test_report_name.exists():
        test_report_name.unlink()

    generated_report = generate_pdf_report(
        candidate_name="Aarav Sharma",
        resume_filename="sample_resume.pdf",
        match_result=match_result,
        suggestions=suggestions,
        output_filename=str(test_report_name)
    )
    assert os.path.exists(generated_report), "Generated PDF report file must exist"
    assert os.path.getsize(generated_report) > 5000, "PDF report file size must be substantial"

    # Open generated PDF with PyMuPDF to verify integrity and text
    rep_doc = fitz.open(generated_report)
    rep_page_count = len(rep_doc)
    assert rep_page_count >= 1, "Report must have at least 1 page"
    rep_text = "".join([page.get_text() for page in rep_doc])
    rep_doc.close()

    assert "ResumeIQ Analysis Report" in rep_text, "Title must be present in PDF"
    assert "Aarav Sharma" in rep_text, "Candidate name must be present in PDF"
    assert "Skill Coverage Score" in rep_text, "Skill Coverage Score label must be present in PDF"
    assert "It is not a real ATS score or a hiring prediction" in rep_text, "Honesty disclaimer must be in PDF"
    print(f"[PASS] PDF Report generated and verified with PyMuPDF ({rep_page_count} pages, text validated).")

    # 10. Test History Persistence Operations
    entry_id = save_analysis(
        candidate_name="Aarav Sharma",
        filename="sample_resume.pdf",
        match_result=match_result,
        suggestions=suggestions,
        word_count=word_count,
        page_count=page_count,
        report_filename=generated_report
    )
    assert entry_id is not None, "Entry ID must be returned"

    hist = list_history()
    assert len(hist) == 1, "Should have 1 entry in history"
    assert hist[0]["id"] == entry_id
    assert hist[0]["name"] == "Aarav Sharma"
    assert hist[0]["score"] == calculated_score
    print("[PASS] History record saved and listed successfully.")

    record = get_history_by_id(entry_id)
    assert record is not None
    assert record["name"] == "Aarav Sharma"
    print("[PASS] History record retrieved by ID successfully.")

    # Delete test
    del_ok = delete_history_by_id(entry_id)
    assert del_ok is True
    assert len(list_history()) == 0
    print("[PASS] History record deleted successfully.")

    # Re-save one sample entry so the History page has a realistic item to view
    saved_id = save_analysis(
        candidate_name="Aarav Sharma",
        filename="sample_resume.pdf",
        match_result=match_result,
        suggestions=suggestions,
        word_count=word_count,
        page_count=page_count,
        report_filename=generated_report
    )
    assert len(list_history()) == 1
    print(f"[PASS] Seeded sample entry for viva demonstration (ID: {saved_id}).")

    # 11. Verify syntax of all python source files
    py_files = list(PROJECT_ROOT.glob("**/*.py"))
    for py_file in py_files:
        with open(py_file, "r", encoding="utf-8") as pf:
            compile(pf.read(), str(py_file), "exec")
    print(f"[PASS] Syntax compiled cleanly for all {len(py_files)} Python files.")

    print("=================================================================")
    print("ALL END-TO-END INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=================================================================")


if __name__ == "__main__":
    test_end_to_end()
