from openai import OpenAI
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI()

# ---------------------------------------------------
# GENERATE NUMERICAL PROBLEMS
# ---------------------------------------------------

def generate_numerical_problems(subject, chapter, topic):

    prompt = rf"""
You are an expert engineering professor.

Generate 10 engineering numerical problems with detailed step-by-step solutions.

Subject: {subject}
Chapter: {chapter}
Topic: {topic}

IMPORTANT REQUIREMENTS:

1. Use professional textbook-style formatting.

2. Use proper Markdown headings.

3. All equations MUST use LaTeX syntax.

4. Use $$ ... $$ for display equations.

5. Include:
   - Given Data
   - Formula
   - Substitution
   - Final Answer

6. Use engineering units properly.

7. Problems should cover:
   - Basic
   - Intermediate
   - Advanced levels

8. Include Bloom's Taxonomy variation.

9. Ensure formulas render beautifully using KaTeX.

EXAMPLE FORMAT:

# Problem 1

## Question

A wall has thickness:

$$
L = 0.2 \ m
$$

Thermal conductivity:

$$
k = 1.5 \ W/mK
$$

Find heat transfer rate if:

$$
\Delta T = 100^\circ C
$$

## Solution

### Formula

$$
Q = \frac{{kA\Delta T}}{{L}}
$$

### Substitution

$$
Q = \frac{{1.5 \times 1 \times 100}}{{0.2}}
$$

### Final Answer

$$
Q = 750 \ W
$$

Now generate 10 complete numerical problems.
"""

    # ---------------------------------------------------
    # OPENAI RESPONSE
    # ---------------------------------------------------

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # ---------------------------------------------------
    # RETURN GENERATED CONTENT
    # ---------------------------------------------------

    return response.choices[0].message.content