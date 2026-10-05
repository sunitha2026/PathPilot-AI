from flask import Flask, render_template, request, jsonify

from app.utils import (
    extract_resume_text,
    detect_skills,
    calculate_resume_score,
    get_career_matches,
    get_strengths,
    get_missing_skills,
    get_recommendations,
    ask_pathpilot_ai
)

from app.jobs import search_jobs


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return jsonify({
            "error": "No resume uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    try:

        # Extract resume text
        resume_text = extract_resume_text(file)

        if not resume_text.strip():
            return jsonify({
                "error": "Could not extract text from the resume"
            }), 400

        # Detect skills
        skills = detect_skills(resume_text)

        # Calculate resume score
        resume_score = calculate_resume_score(resume_text)

        # Calculate career matches
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

        # Search jobs for top career
        jobs = []

        if career_matches:

            top_career = career_matches[0]["career"]

            jobs = search_jobs(
                top_career,
                "India"
            )

        # Show result page
        return render_template(
            "result.html",
            filename=file.filename,
            skills=skills,
            resume_text=resume_text[:3000],
            resume_score=resume_score,
            career_matches=career_matches,
            strengths=strengths,
            missing_skills=missing_skills,
            recommendations=recommendations,
            jobs=jobs
        )

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# PATHPILOT AI CHATBOT
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

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


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )