import matplotlib

# ---------------------------------------------------
# FIX TKINTER / THREADING ISSUE
# ---------------------------------------------------

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os

# ---------------------------------------------------
# GENERATE ENGINEERING DIAGRAM
# ---------------------------------------------------

def generate_engineering_diagram(subject, chapter, topic):

    fig, ax = plt.subplots(figsize=(8, 4))

    topic_lower = topic.lower()

    # ---------------------------------------------------
    # HEAT CONDUCTION
    # ---------------------------------------------------

    if "conduction" in topic_lower:

        ax.plot([0.1, 0.9], [0.5, 0.5], linewidth=12)

        ax.text(0.15, 0.6, "T1", fontsize=12)

        ax.text(0.8, 0.6, "T2", fontsize=12)

        ax.arrow(
            0.35,
            0.5,
            0.25,
            0,
            head_width=0.03,
            length_includes_head=True
        )

        ax.text(0.42, 0.56, "Heat Flow", fontsize=10)

        ax.set_title("Heat Conduction Through Plane Wall")

    # ---------------------------------------------------
    # DISTILLATION
    # ---------------------------------------------------

    elif "distillation" in topic_lower:

        ax.plot([0.5, 0.5], [0.15, 0.85], linewidth=10)

        ax.text(0.55, 0.8, "Condenser", fontsize=11)

        ax.text(0.55, 0.2, "Reboiler", fontsize=11)

        ax.arrow(
            0.5,
            0.3,
            0,
            0.3,
            head_width=0.03,
            length_includes_head=True
        )

        ax.text(0.55, 0.5, "Vapor Flow", fontsize=10)

        ax.set_title("Distillation Column")

    # ---------------------------------------------------
    # HEAT EXCHANGER
    # ---------------------------------------------------

    elif "heat exchanger" in topic_lower:

        ax.plot([0.1, 0.9], [0.65, 0.65], linewidth=8)

        ax.plot([0.1, 0.9], [0.35, 0.35], linewidth=8)

        ax.arrow(
            0.2,
            0.65,
            0.4,
            0,
            head_width=0.03,
            length_includes_head=True
        )

        ax.arrow(
            0.8,
            0.35,
            -0.4,
            0,
            head_width=0.03,
            length_includes_head=True
        )

        ax.text(0.2, 0.72, "Hot Fluid", fontsize=10)

        ax.text(0.55, 0.25, "Cold Fluid", fontsize=10)

        ax.set_title("Heat Exchanger")

    # ---------------------------------------------------
    # DEFAULT GENERIC DIAGRAM
    # ---------------------------------------------------

    else:

        ax.text(
            0.3,
            0.5,
            topic,
            fontsize=16
        )

        ax.set_title("Engineering Diagram")

    # ---------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------

    ax.axis("off")

    os.makedirs("outputs/diagrams", exist_ok=True)

    image_path = "outputs/diagrams/diagram.png"

    plt.savefig(image_path, bbox_inches="tight")

    plt.close()

    return image_path