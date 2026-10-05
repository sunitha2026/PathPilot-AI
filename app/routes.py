from flask import request, jsonify, render_template

from .utils import (
    extract_resume_text,
    detect_skills,
    calculate_resume_score,
    get_career_matches,
    get_strengths,
    get_missing_skills,
    get_recommendations,
    ask_pathpilot_ai
)

from .jobs import search_jobs


def analyze_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:

        # Extract resume text
        resume_text = extract_resume_text(file)

        # Detect skills
        skills = detect_skills(resume_text)

        # Calculate resume score
        resume_score = calculate_resume_score(resume_text)

        # Find career matches
        career_matches = get_career_matches(skills)

        # Find strengths
        strengths = get_strengths(skills)

        # Find missing skills
        missing_skills = get_missing_skills(
            skills,
            career_matches
        )

        # Generate recommendations
        recommendations = get_recommendations(
            missing_skills,
            career_matches
        )

        # Find the user's top career
        jobs = []

        if career_matches:

            top_career = career_matches[0]["career"]

            # Search India jobs based on top career
            jobs = search_jobs(
                top_career,
                "India"
            )

        return render_template(
            "result.html",
            resume_text=resume_text,
            filename=file.filename,
            skills=skills,
            resume_score=resume_score,
            career_matches=career_matches,
            strengths=strengths,
            missing_skills=missing_skills,
            recommendations=recommendations,
            jobs=jobs
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# PATHPILOT AI CHATBOT
# ==========================================

def chat_with_pathpilot():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    question = data.get("question", "").strip()

    context = data.get("context", "").strip()

    if not question:
        return jsonify({
            "error": "Please enter a question"
        }), 400

    try:

        answer = ask_pathpilot_ai(
            question,
            context
        )

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500