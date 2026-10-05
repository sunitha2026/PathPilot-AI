import fitz
from docx import Document
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# ==========================================
# RESUME TEXT EXTRACTION
# ==========================================

def extract_text_from_pdf(file):
    text = ""

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_text_from_docx(file):
    text = ""

    document = Document(file)

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_resume_text(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        return ""


# ==========================================
# SKILL DETECTION
# ==========================================

def detect_skills(text):

    skills_list = [
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "html",
        "css",
        "sql",
        "git",
        "github",
        "machine learning",
        "power bi",
        "excel",
        "flask",
        "django",
        "data analysis"
    ]

    text_lower = text.lower()

    detected_skills = []

    for skill in skills_list:

        if skill in text_lower:
            detected_skills.append(skill)

    return detected_skills


# ==========================================
# RESUME SCORE
# ==========================================

def calculate_resume_score(text):

    score = 0

    text_lower = text.lower()

    # Contact information
    if "@" in text:
        score += 10

    if any(char.isdigit() for char in text):
        score += 5

    # Important resume sections
    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    for section in sections:

        if section in text_lower:
            score += 10

    # Technical skills
    technical_skills = [
        "python",
        "java",
        "javascript",
        "sql",
        "html",
        "css",
        "git",
        "github",
        "machine learning",
        "power bi"
    ]

    detected_count = 0

    for skill in technical_skills:

        if skill in text_lower:
            detected_count += 1

    score += min(
        detected_count * 3,
        15
    )

    # Keep score between 0 and 100
    score = min(
        score,
        100
    )

    return score


# ==========================================
# CAREER MATCHING
# ==========================================

def get_career_matches(skills):

    career_requirements = {

        "Python Developer": [
            "python",
            "git",
            "github",
            "flask",
            "sql"
        ],

        "Data Analyst": [
            "python",
            "sql",
            "excel",
            "power bi",
            "data analysis"
        ],

        "Machine Learning Engineer": [
            "python",
            "machine learning",
            "sql",
            "git"
        ],

        "Web Developer": [
            "html",
            "css",
            "javascript",
            "python",
            "flask"
        ],

        "Data Scientist": [
            "python",
            "sql",
            "machine learning",
            "data analysis"
        ]
    }

    matches = []

    user_skills = set(
        skill.lower()
        for skill in skills
    )

    for career, required_skills in career_requirements.items():

        matched = 0

        for skill in required_skills:

            if skill in user_skills:
                matched += 1

        percentage = round(
            (matched / len(required_skills)) * 100
        )

        matches.append({
            "career": career,
            "match": percentage
        })

    matches.sort(
        key=lambda item: item["match"],
        reverse=True
    )

    return matches


# ==========================================
# STRENGTHS
# ==========================================

def get_strengths(skills):

    strengths = []

    skill_groups = {

        "Programming": [
            "python",
            "java",
            "c",
            "c++",
            "javascript"
        ],

        "Web Development": [
            "html",
            "css",
            "javascript",
            "flask",
            "django"
        ],

        "Data & Analytics": [
            "sql",
            "excel",
            "power bi",
            "data analysis"
        ],

        "Machine Learning": [
            "machine learning",
            "python"
        ],

        "Development Tools": [
            "git",
            "github"
        ]
    }

    user_skills = set(
        skill.lower()
        for skill in skills
    )

    for strength, related_skills in skill_groups.items():

        if any(
            skill in user_skills
            for skill in related_skills
        ):
            strengths.append(strength)

    return strengths


# ==========================================
# MISSING SKILLS
# ==========================================

def get_missing_skills(skills, career_matches):

    if not career_matches:
        return []

    # Get the highest matching career
    top_career = career_matches[0]["career"]

    career_requirements = {

        "Python Developer": [
            "python",
            "git",
            "github",
            "flask",
            "sql"
        ],

        "Data Analyst": [
            "python",
            "sql",
            "excel",
            "power bi",
            "data analysis"
        ],

        "Machine Learning Engineer": [
            "python",
            "machine learning",
            "sql",
            "git"
        ],

        "Web Developer": [
            "html",
            "css",
            "javascript",
            "python",
            "flask"
        ],

        "Data Scientist": [
            "python",
            "sql",
            "machine learning",
            "data analysis"
        ]
    }

    required_skills = career_requirements.get(
        top_career,
        []
    )

    user_skills = set(
        skill.lower()
        for skill in skills
    )

    missing = []

    for skill in required_skills:

        if skill not in user_skills:
            missing.append(skill)

    return missing


# ==========================================
# AI-POWERED RECOMMENDATIONS
# ==========================================

def get_recommendations(missing_skills, career_matches):

    if not career_matches:
        return []

    top_career = career_matches[0]["career"]
    top_match = career_matches[0]["match"]

    missing_skills_text = (
        ", ".join(missing_skills)
        if missing_skills
        else "None"
    )

    prompt = f"""
You are an AI career advisor for a student.

The student's resume analysis produced these results:

Target career:
{top_career}

Career match:
{top_match}%

Missing skills:
{missing_skills_text}

Provide exactly 4 short and practical recommendations.

Focus on:

1. Skills the student should learn or improve
2. Practical projects they should build
3. Resume improvement
4. Job and internship preparation

The recommendations should be:
- Beginner-friendly
- Specific
- Practical
- Easy to understand

Return ONLY the 4 recommendations as a numbered list.
Do not add an introduction or conclusion.
"""

    try:

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        recommendations = response.output_text.strip().split("\n")

        # Remove empty lines
        recommendations = [
            item.strip()
            for item in recommendations
            if item.strip()
        ]

        return recommendations[:4]

    except Exception:

        # Fallback recommendations
        recommendations = []

        recommendations.append(
            f"Focus on skills required for {top_career}."
        )

        for skill in missing_skills:

            recommendations.append(
                f"Consider learning {skill}."
            )

        recommendations.append(
            "Add more practical projects to strengthen your resume."
        )

        recommendations.append(
            "Keep your GitHub profile updated with your best projects."
        )

        return recommendations[:4]


# ==========================================
# AI RESUME ANALYSIS
# ==========================================

def get_ai_resume_analysis(resume_text):

    prompt = f"""
You are an AI career assistant.

Analyze the following student's resume.

Provide:

1. A short overall assessment
2. Top 3 strengths
3. Top 3 areas to improve
4. Recommended skills to learn
5. Suitable career roles

Keep the response:
- Beginner-friendly
- Clear
- Practical
- Easy to understand

Do not make up information that is not present in the resume.

Resume:
{resume_text}
"""

    try:

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return response.output_text.strip()

    except Exception:

        return "AI resume analysis is currently unavailable."


# ==========================================
# PATHPILOT AI CHATBOT
# ==========================================

def ask_pathpilot_ai(question, context=""):

    prompt = f"""
You are PathPilot AI, an intelligent and helpful AI assistant.

Answer the user's question clearly, accurately, and practically.

You can help with:

- Career guidance
- Resume improvement
- Programming and coding
- Debugging and programming errors
- Python, Java, C, C++, JavaScript, SQL and other programming topics
- Technical concepts
- Projects
- Skills and learning roadmaps
- Job and internship preparation
- Questions about uploaded documents

If resume or document context is provided, use it when relevant.

Important rules:

- Do not make up information.
- If you are unsure about something, clearly say that you are unsure.
- For programming questions, provide explanations and code examples when useful.
- Keep explanations beginner-friendly unless the user asks for advanced detail.
- If the user asks about their resume, use the provided resume context.
- Do not claim that information is current unless current information is actually provided.

Context:
{context}

User Question:
{question}

Give a clear and useful answer.
"""

    try:

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return response.output_text.strip()

    except Exception:

        return "Sorry, I couldn't process your question right now. Please try again."

