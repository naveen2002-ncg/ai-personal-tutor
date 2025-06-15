def recommend_topics(subject):
    recommendations = {
        "Math": ["Practice multiplication tables", "Understand fractions", "Try solving puzzles"],
        "Science": ["Read about gravity", "Explore the solar system", "Learn about photosynthesis"],
        "Python Basics": ["Try list comprehension", "Practice writing functions", "Build a simple calculator"]
    }

    return recommendations.get(subject, ["Explore more topics on your own!"])
