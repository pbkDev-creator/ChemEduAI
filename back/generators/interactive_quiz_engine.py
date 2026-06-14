from openai import OpenAI
from dotenv import load_dotenv
import json

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI()

# ---------------------------------------------------
# INTERACTIVE QUIZ ENGINE
# ---------------------------------------------------

def generate_interactive_quiz(
    subject,
    chapter,
    topic,
    num_questions=10
):

    prompt = f"""
You are an expert Engineering Professor.

Generate exactly {num_questions} multiple choice questions.

Subject:
{subject}

Chapter:
{chapter}

Topic:
{topic}

Return ONLY valid JSON.

Required format:

[
  {{
    "question": "...",
    "options": [
      "...",
      "...",
      "...",
      "..."
    ],
    "answer": "...",
    "explanation": "..."
  }}
]

Rules:

- Exactly 4 options.
- Answer must exactly match one option.
- Include engineering concepts.
- Include application-oriented questions.
- Include numerical reasoning when appropriate.
- No markdown.
- No commentary.
- Output JSON only.
"""

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)