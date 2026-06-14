from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel


import os

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------
# IMPORT GENERATORS
# ---------------------------------------------------

from generators.ai_engine import generate_teaching_content

from generators.numerical_engine import generate_numerical_problems

from generators.exam_engine import generate_exam_questions

from generators.question_paper_engine import generate_question_paper

from generators.diagram_generator import generate_engineering_diagram

from generators.pdf_generator import generate_pdf

from generators.ppt_generator import generate_ppt

from generators.tutor_engine import generate_tutor_response

from generators.chat_memory import clear_history

from generators.quiz_engine import generate_quiz

from generators.interactive_quiz_engine import generate_interactive_quiz

from generators.recommendation_engine import generate_recommendations



# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------
# ---------------------------------------------------
# SUPABASE CONFIGURATION
# ---------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI()

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------

class TopicRequest(BaseModel):
    subject: str
    chapter: str
    topic: str


class SavedPDFRequest(BaseModel):
    topic: str
    content: str

class TutorRequest(BaseModel):

    user_id: str

    subject: str

    chapter: str

    topic: str

    question: str

class ClearChatRequest(BaseModel):
    user_id: str    

class QuizRequest(BaseModel):

    subject: str

    chapter: str

    topic: str

    num_questions: int = 10

class InteractiveQuizRequest(BaseModel):

    subject: str

    chapter: str

    topic: str

    num_questions: int = 10    
# ---------------------------------------------------
# ROOT
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Backend Working Successfully"
    }


# ---------------------------------------------------
# GENERATE TEACHING CONTENT
# ---------------------------------------------------

@app.post("/generate")
def generate_content(request: TopicRequest):

    content = generate_teaching_content(
        request.subject,
        request.chapter,
        request.topic
    )

    return {
        "content": content
    }


# ---------------------------------------------------
# GENERATE NUMERICALS
# ---------------------------------------------------

@app.post("/generate_numericals")
def generate_numericals(request: TopicRequest):

    content = generate_numerical_problems(
        request.subject,
        request.chapter,
        request.topic
    )

    return {
        "content": content
    }


# ---------------------------------------------------
# GENERATE EXAM QUESTIONS
# ---------------------------------------------------

@app.post("/generate_exam_questions")
def generate_questions(request: TopicRequest):

    content = generate_exam_questions(
        request.subject,
        request.chapter,
        request.topic
    )

    return {
        "content": content
    }


# ---------------------------------------------------
# GENERATE QUESTION PAPER
# ---------------------------------------------------

@app.post("/generate_question_paper")
def generate_paper(request: TopicRequest):

    content = generate_question_paper(
        request.subject,
        request.chapter,
        request.topic
    )

    return {
        "content": content
    }

# ---------------------------------------------------
# GENERATE QUIZ
# ---------------------------------------------------

@app.post("/generate_quiz")
def generate_quiz_endpoint(request: QuizRequest):

    quiz_content = generate_quiz(
        request.subject,
        request.chapter,
        request.topic,
        request.num_questions
    )

    return {
        "content": quiz_content
    }

# ---------------------------------------------------
# GENERATE INTERACTIVE QUIZ
# ---------------------------------------------------

@app.post("/generate_interactive_quiz")
def generate_interactive_quiz_endpoint(
    request: InteractiveQuizRequest
):

    quiz_data = generate_interactive_quiz(
        request.subject,
        request.chapter,
        request.topic,
        request.num_questions
    )

    return quiz_data    
# ---------------------------------------------------
# AI TUTOR
# ---------------------------------------------------

# ---------------------------------------------------
# AI TUTOR
# ---------------------------------------------------

@app.post("/ask_tutor")
def ask_tutor(request: TutorRequest):

    response = generate_tutor_response(
        request.user_id,
        request.subject,
        request.chapter,
        request.topic,
        request.question
    )

    return {
        "content": response
    }

# ---------------------------------------------------
# CLEAR TUTOR CHAT
# ---------------------------------------------------

@app.post("/clear_tutor_chat")
def clear_tutor_chat(request: ClearChatRequest):

    clear_history(request.user_id)

    return {
        "message": "Tutor memory cleared successfully."
    }

# ---------------------------------------------------
# AI LEARNING RECOMMENDATIONS
# ---------------------------------------------------

# @app.get("/recommendations/{user_id}")
# def get_recommendations(user_id: str):

#     try:

#         response = supabase.table(
#             "quiz_results"
#         ).select(
#             "*"
#         ).eq(
#             "user_id",
#             user_id
#         ).execute()

#         results = response.data

#         recommendations = generate_recommendations(
#             results
#         )

#         return recommendations

#     except Exception as e:

#         return {
#             "error": str(e)
#         }        




# ---------------------------------------------------
# EXPORT PDF
# ---------------------------------------------------

@app.post("/export/pdf")
def export_pdf(request: TopicRequest):

    content = generate_teaching_content(
        request.subject,
        request.chapter,
        request.topic
    )

    pdf_path = generate_pdf(
        subject=request.subject,
        chapter=request.chapter,
        topic=request.topic,
        content=content
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="study_material.pdf"
    )


# ---------------------------------------------------
# DOWNLOAD SAVED PDF
# ---------------------------------------------------

@app.post("/download_saved_pdf")
def download_saved_pdf(request: SavedPDFRequest):

    try:

        # ---------------------------------------------
        # GENERATE PDF FROM SAVED CONTENT
        # ---------------------------------------------

        pdf_path = generate_pdf(
            subject="Saved Study Material",
            chapter="Study History",
            topic=request.topic,
            content=request.content
        )

        safe_topic = request.topic.replace(" ", "_")

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"{safe_topic}.pdf"
        )

    except Exception as e:

        print("Saved PDF Error:", str(e))

        return {
            "error": str(e)
        }


# ---------------------------------------------------
# EXPORT PPT
# ---------------------------------------------------

@app.post("/export/ppt")
def export_ppt(request: TopicRequest):

    content = generate_teaching_content(
        request.subject,
        request.chapter,
        request.topic
    )

    title = (
        f"{request.subject} - "
        f"{request.chapter} - "
        f"{request.topic}"
    )

    ppt_path = generate_ppt(
        title,
        content,
        "lecture_slides.pptx"
    )

    return FileResponse(
        path=ppt_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="lecture_slides.pptx"
    )


# ---------------------------------------------------
# GENERATE DIAGRAM
# ---------------------------------------------------

@app.post("/diagram")
def diagram(request: TopicRequest):

    image_path = generate_engineering_diagram(
        request.subject,
        request.chapter,
        request.topic
    )

    return FileResponse(
        path=image_path,
        media_type="image/png",
        filename="diagram.png"
    )


# ---------------------------------------------------
# SOLVE NUMERICAL
# ---------------------------------------------------

@app.get("/solve")
def solve():

    return {
        "solution":
        """
# Numerical Solution

## Problem

A wall of thickness:

$$
L = 0.2 \\, m
$$

has thermal conductivity:

$$
k = 1.5 \\, W/mK
$$

Find heat transfer rate if temperature difference is:

$$
\\Delta T = 100^\\circ C
$$

---

## Formula

$$
Q = \\frac{kA\\Delta T}{L}
$$

---

## Solution

Given:

$$
k = 1.5 \\, W/mK
$$

$$
L = 0.2 \\, m
$$

$$
\\Delta T = 100^\\circ C
$$

Assume:

$$
A = 1 \\, m^2
$$

Substitute:

$$
Q = \\frac{1.5 \\times 1 \\times 100}{0.2}
$$

$$
Q = 750 \\, W
$$

---

# Final Answer

$$
Q = 750 \\, W
$$
        """
    }


# ---------------------------------------------------
# SERVER START MESSAGE
# ---------------------------------------------------

print("ChemEduAI Backend Started Successfully")