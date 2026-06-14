from openai import OpenAI
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI()

# ---------------------------------------------------
# QUIZ ENGINE
# ---------------------------------------------------

def generate_quiz(
    subject,
    chapter,
    topic,
    num_questions=10
):

    prompt = f"""
You are an expert Engineering Professor.

Generate {num_questions} high-quality Multiple Choice Questions.

Subject:
{subject}

Chapter:
{chapter}

Topic:
{topic}

Requirements:

- Follow undergraduate engineering standards.
- Cover conceptual understanding.
- Include numerical and application questions whenever appropriate.
- Use Bloom's Taxonomy levels:
  Remember
  Understand
  Apply
  Analyze

For every question provide:

Question

A)
B)
C)
D)

Correct Answer

Explanation

Use Markdown formatting.
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

    return response.choices[0].message.content