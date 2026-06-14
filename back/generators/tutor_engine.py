from openai import OpenAI
from dotenv import load_dotenv

from generators.chat_memory import (
    get_history,
    save_message
)

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI()

# ---------------------------------------------------
# AI TUTOR ENGINE
# ---------------------------------------------------

def generate_tutor_response(
    user_id,
    subject,
    chapter,
    topic,
    student_question
):

    # ---------------------------------------------------
    # LOAD PREVIOUS CONVERSATION
    # ---------------------------------------------------

    history = get_history(user_id)

    # ---------------------------------------------------
    # SYSTEM PROMPT
    # ---------------------------------------------------

    messages = [
        {
            "role": "system",
            "content": f"""
You are an expert Engineering Professor and AI Tutor.

Subject:
{subject}

Chapter:
{chapter}

Topic:
{topic}

Always answer in a professional engineering textbook style.

Provide responses using the following structure:

# Direct Answer

Provide a concise answer first.

# Concept Explanation

Explain the concept clearly in textbook style.

# Step-by-Step Explanation

Break down the reasoning process.

# Engineering Insight

Explain the practical engineering significance.

# Worked Example

Provide a solved example whenever applicable.

# Common Mistakes

List common student mistakes.

# Examination Tips

Explain how this topic is commonly asked in university exams.

# Related Concepts

Suggest related concepts for further learning.

Important Requirements:

- Use professional engineering terminology.
- Use Markdown formatting.
- Use LaTeX equations wherever necessary.
- Make explanations student-friendly.
- Include units properly.
- Follow undergraduate engineering standards.
- Remember previous questions in the conversation.
- Answer follow-up questions using the previous context.
"""
        }
    ]

    # ---------------------------------------------------
    # ADD PREVIOUS CHAT HISTORY
    # ---------------------------------------------------

    messages.extend(history)

    # ---------------------------------------------------
    # ADD CURRENT QUESTION
    # ---------------------------------------------------

    messages.append(
        {
            "role": "user",
            "content": student_question
        }
    )

    # ---------------------------------------------------
    # OPENAI CALL
    # ---------------------------------------------------

    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )

    response_text = (
        response.choices[0]
        .message.content
    )

    # ---------------------------------------------------
    # SAVE CONVERSATION MEMORY
    # ---------------------------------------------------

    save_message(
        user_id,
        "user",
        student_question
    )

    save_message(
        user_id,
        "assistant",
        response_text
    )

    # ---------------------------------------------------
    # RETURN RESPONSE
    # ---------------------------------------------------

    return response_text