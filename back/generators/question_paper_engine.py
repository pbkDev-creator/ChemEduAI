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
# AI MODEL QUESTION PAPER GENERATOR
# ---------------------------------------------------

def generate_question_paper(subject, chapter, topic):

    prompt = f"""
You are an expert university engineering professor and examination paper setter.

Generate a PROFESSIONAL UNIVERSITY MODEL QUESTION PAPER.

==================================================
SUBJECT:
{subject}

CHAPTER:
{chapter}

TOPIC:
{topic}
==================================================

IMPORTANT FORMATTING RULES:

1. Use professional university exam formatting.

2. Use markdown formatting.

3. Use proper headings and spacing.

4. Use LaTeX equations where required.

5. Inline equations must use:
$ ... $

6. Block equations must use:
$$ ... $$

7. NEVER use:
\\(
\\)

OR:
\\[
\\]

==================================================
QUESTION PAPER REQUIREMENTS
==================================================

Generate a COMPLETE question paper containing:

# UNIVERSITY HEADER

Include:
- University Name
- Department
- Subject Name
- Examination Type
- Duration
- Maximum Marks

==================================================

# EXAMINATION INSTRUCTIONS

Include:
- answer all compulsory questions
- assumptions if any
- use of calculators
- units requirement
- neat diagrams

==================================================

# PART A — SHORT ANSWER QUESTIONS

Generate:
10 questions × 2 marks

Requirements:
- conceptual
- definitions
- short theory
- formula-based

Mention:
(Bloom Level: ____)

==================================================

# PART B — MEDIUM ANSWER QUESTIONS

Generate:
5 questions × 5 marks

Include:
- derivations
- theory
- applications
- short numericals

Mention:
(Bloom Level: ____)

==================================================

# PART C — LONG ANSWER QUESTIONS

Generate:
3 questions × 15 marks

Include:
- detailed derivations
- industrial applications
- advanced numericals
- engineering analysis

Mention:
(Bloom Level: ____)

==================================================

# MCQ SECTION

Generate:
10 MCQs

Format:

Q1.

A.
B.
C.
D.

Answer: ___

==================================================

# NUMERICAL SECTION

Generate:
5 university-level numerical problems.

Include:
- easy
- medium
- advanced

==================================================

# IMPORTANT THEORY QUESTIONS

Generate:
important derivation and theory questions frequently asked in university exams.

==================================================
BLOOM TAXONOMY RULES
==================================================

Use proper Bloom taxonomy levels:
- Remember
- Understand
- Apply
- Analyze
- Evaluate
- Create

==================================================
QUALITY REQUIREMENTS
==================================================

1. Questions must be technically accurate.

2. Questions must be engineering-oriented.

3. Questions must look like real university papers.

4. Maintain balanced difficulty.

5. Include industrial relevance.

6. Use professional academic formatting.

7. Ensure proper marks distribution.

8. Make the paper suitable for engineering degree students.

9. Include derivation-focused and numerical-focused questions.

10. Output must resemble a real semester-end examination paper.
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