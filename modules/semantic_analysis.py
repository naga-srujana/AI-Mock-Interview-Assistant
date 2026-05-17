def analyze_semantic_similarity(
    candidate_text: str,
    ideal_text: str
) -> dict:

    try:
        from sentence_transformers import SentenceTransformer, util

        model = SentenceTransformer("all-MiniLM-L6-v2")

        emb1 = model.encode(
            candidate_text,
            convert_to_tensor=True
        )

        emb2 = model.encode(
            ideal_text,
            convert_to_tensor=True
        )

        cosine_score = util.cos_sim(
            emb1,
            emb2
        ).item()

        score = round(
            max(0, min(cosine_score, 1)) * 100,
            1
        )

    except Exception:
        score = _fallback_similarity(
            candidate_text,
            ideal_text
        )

    if score >= 75:
        label = "Highly Relevant"

    elif score >= 55:
        label = "Moderately Relevant"

    elif score >= 35:
        label = "Somewhat Relevant"

    else:
        label = "Low Relevance"

    return {
        "score": round(score, 1),
        "label": label,
        "details": f"Your answer matched the ideal response with {score:.1f}% semantic similarity."
    }


def _fallback_similarity(
    text1: str,
    text2: str
) -> float:

    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = words1 & words2
    union = words1 | words2

    jaccard = len(intersection) / len(union)

    return round(
        min(jaccard * 2.5, 1.0) * 100,
        1
    )