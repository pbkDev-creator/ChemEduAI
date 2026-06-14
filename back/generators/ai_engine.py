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
# CENTRAL AI TEACHING ENGINE
# ---------------------------------------------------

def generate_teaching_content(subject, chapter, topic):

    prompt = f"""
You are an expert engineering professor and textbook author.

Generate professional university-level engineering teaching material.

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

2. Use textbook-quality engineering explanations.

3. ALL mathematical equations must use LaTeX.

4. Inline equations MUST use:
$ ... $

Example:
$Q = m C_p \\Delta T$

5. Block equations MUST use:
$$ ... $$

Example:

$$
Q = \\frac{{kA(T_1-T_2)}}{{L}}
$$

6. NEVER use:
\\(
\\)

OR:
\\[
\\]

7. Use proper:
- fractions
- superscripts
- subscripts
- Greek symbols
- engineering units

8. IMPORTANT VARIABLE NOTATION RULE:

Whenever defining variables or notation,
ALWAYS use this format:

$W$ = total moles of liquid in still

$F$ = feed quantity

$x_A$ = mole fraction of component A

$\\alpha$ = relative volatility

NEVER use:
- $W$ :
- $F$ :
- $x_A$ :

Always use equal sign notation.

9. Use clean engineering notation.

10. Use SI units properly.

==================================================
CONTENT REQUIREMENTS
==================================================

Generate the following sections:

# Introduction

# Theory Explanation

# Fundamental Concepts

# Important Equations

# Stepwise Derivations

# Engineering Applications

# Industrial Applications

# Solved Numerical Example

# Important Examination Questions

# Key Takeaways

# Summary

# Faculty Teaching Notes

==================================================
SOLVED NUMERICAL REQUIREMENTS
==================================================

1. Include at least ONE detailed solved numerical problem.

2. Numerical solution must contain:
- Given Data
- Formula Used
- Stepwise Solution
- Final Answer with units

3. Use engineering textbook style.

==================================================
EXAMINATION QUESTIONS
==================================================

Generate:
- short answer questions
- long answer questions
- derivation questions
- numerical problems

==================================================
QUALITY REQUIREMENTS
==================================================

1. Content must be student friendly.

2. Content must be university examination oriented.

3. Content must be technically accurate.

4. Use professional engineering terminology.

5. Keep explanations clear and structured.

6. Use clean spacing and headings.

7. Generate detailed and meaningful content.

8. Make the output look like a professional engineering textbook.
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