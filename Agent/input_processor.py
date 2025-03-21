import re

# key words for factual question
wh_words = [
    "what",
    "how",
    "where",
    "when",
    "who",
    "why",
    "which",
    "how much",
    "how many",
    "how long",
    "how far",
    "what time",
    "which way",
    "what kind",
    "what type",
]
# key words for creative task
creative_keywords = [
    "write",
    "create",
    "design",
    "describe",
    "imagine",
    "draw",
    "invent",
    "generate",
    "craft",
    "tell",
    "compose",
    "narrate",
    "explain",
    "come up with",
    "formulate",
    "paint",
    "build",
    "sculpt",
    "develop",
    "conceptualize",
    "brainstorm",
    "plan",
    "ideate",
    "illustrate",
    "produce",
    "dream up",
    "create a story",
    "compose a song",
    "sketch",
    "choreograph",
    "give",
]


def classify_query(query):

    query = query.lower()

    for wh in wh_words:
        pattern = r"\b" + re.escape(wh) + r"\b"
        if re.search(pattern, query) or query.strip().endswith("?"):
            return "Factual Question"
        elif any(keyword in query for keyword in creative_keywords):
            return "Creative Task"

    return "Unknown"
