import os

from dotenv import load_dotenv

from openai import OpenAI

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv(dotenv_path=".env")

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------------------------
# AI EXAM PREPARATION ENGINE
# ---------------------------------------------------

def generate_exam_questions(subject, chapter, topic):

    prompt = f"""
You are an expert university engineering professor.

Generate a COMPLETE university examination preparation set.

==================================================
SUBJECT:
{subject}

CHAPTER:
{chapter}

TOPIC:
{topic}
==================================================

IMPORTANT FORMATTING RULES:

1. Use proper markdown formatting.

2. Use engineering textbook style formatting.

3. Use LaTeX equations where required.

4. Inline equations must use:
$ ... $

5. Block equations must use:
$$ ... $$

6. NEVER use:
\\(
\\)

OR:
\\[
\\]

==================================================
EXAM GENERATION REQUIREMENTS
==================================================

Generate the following sections:

# PART A — 2 MARK QUESTIONS

Generate 10 short-answer questions.

For each question:
- mention Bloom taxonomy level

Example:
(Bloom Level: Remember)

==================================================

# PART B — 5 MARK QUESTIONS

Generate 10 medium-level questions.

Include:
- theory questions
- derivations
- short numericals

Mention Bloom taxonomy level.

==================================================

# PART C — 10/15 MARK QUESTIONS

Generate 10 long-answer questions.

Include:
- derivations
- detailed explanations
- industrial applications
- advanced numerical problems

Mention Bloom taxonomy level.

==================================================

# NUMERICAL PROBLEMS

Generate 10 university-level numerical problems.

Include:
- easy
- moderate
- advanced

==================================================

# MULTIPLE CHOICE QUESTIONS (MCQs)

Generate 15 MCQs.

Format:

Q1. Question

A.
B.
C.
D.

Answer: ____

==================================================

# VIVA QUESTIONS

Generate 15 viva voce questions with short answers.

==================================================

# IMPORTANT UNIVERSITY QUESTIONS

Generate:
- frequently asked questions
- derivation-focused questions
- important theory questions

==================================================
BLOOM TAXONOMY RULES
==================================================

Use proper Bloom classification:

- Remember
- Understand
- Apply
- Analyze
- Evaluate
- Create

==================================================
QUALITY REQUIREMENTS
==================================================

1. Questions must be engineering-oriented.

2. Questions must be university examination level.

3. Questions must be technically accurate.

4. Include practical and industrial relevance.

5. Use proper engineering terminology.

6. Ensure variety in difficulty levels.

7. Use professional formatting.

8. Make the output look like a real university exam preparation guide.
"""

    response = client.chat.completions.create(

        model="gpt-5-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content