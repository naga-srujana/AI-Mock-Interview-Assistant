def calculate_confidence_score(
    grammar_score: float,
    fluency_score: float,
    sentiment_compound: float,
    semantic_score: float
) -> dict:

    sentiment_score = round((sentiment_compound + 1) / 2 * 100, 1)
    sentiment_score = max(0, min(sentiment_score, 100))

    grammar_contrib = round(grammar_score * 0.25, 1)
    fluency_contrib = round(fluency_score * 0.25, 1)
    sentiment_contrib = round(sentiment_score * 0.20, 1)
    relevance_contrib = round(semantic_score * 0.30, 1)

    overall = round(
        grammar_contrib +
        fluency_contrib +
        sentiment_contrib +
        relevance_contrib,
        1
    )

    overall = max(0, min(overall, 100))

    if overall >= 80:
        level = "Excellent"
    elif overall >= 65:
        level = "Good"
    elif overall >= 50:
        level = "Average"
    elif overall >= 35:
        level = "Below Average"
    else:
        level = "Needs Work"

    return {
        "overall": overall,
        "level": level,
        "grammar_contrib": grammar_contrib,
        "fluency_contrib": fluency_contrib,
        "sentiment_contrib": sentiment_contrib,
        "relevance_contrib": relevance_contrib,
        "sentiment_score": sentiment_score,
    }