import matplotlib.pyplot as plt

import uuid

import os

# ---------------------------------------------------
# RENDER LATEX EQUATION TO IMAGE
# ---------------------------------------------------

def render_equation(equation, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.png"

    filepath = os.path.join(output_dir, filename)

    fig = plt.figure(figsize=(8, 1))

    fig.text(
        0.05,
        0.5,
        f"${equation}$",
        fontsize=16
    )

    plt.axis("off")

    plt.savefig(
        filepath,
        bbox_inches="tight",
        transparent=True,
        dpi=300
    )

    plt.close(fig)

    return filepath