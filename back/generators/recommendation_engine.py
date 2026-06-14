def generate_recommendations(results):

    if not results:

        return {
            "strong_topics": [],
            "weak_topics": [],
            "recommendations": [
                "Attempt more quizzes to generate recommendations."
            ]
        }

    topic_scores = {}

    for item in results:

        topic = item["topic"]

        percentage = (
            item["score"] /
            item["total_questions"]
        ) * 100

        if topic not in topic_scores:

            topic_scores[topic] = []

        topic_scores[topic].append(
            percentage
        )

    averages = {

        topic:
        sum(scores) / len(scores)

        for topic, scores in topic_scores.items()

    }

    strong_topics = [

        topic

        for topic, avg in averages.items()

        if avg >= 80

    ]

    weak_topics = [

        topic

        for topic, avg in averages.items()

        if avg < 60

    ]

    recommendations = []

    for topic in weak_topics:

        recommendations.append(

            f"Revise topic: {topic}"

        )

        recommendations.append(

            f"Attempt numerical problems on {topic}"

        )

        recommendations.append(

            f"Ask AI Tutor questions on {topic}"

        )

    return {

        "strong_topics": strong_topics,

        "weak_topics": weak_topics,

        "recommendations": recommendations

    }