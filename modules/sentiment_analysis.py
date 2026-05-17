def analyze_sentiment(text: str) -> dict:
    try:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        import nltk
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon", quiet=True)

        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        compound = scores["compound"]

    except Exception:
        compound, scores = _fallback_sentiment(text)

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    emotion = _detect_emotion(text, compound)

    return {
        "compound": round(compound, 3),
        "label": label,
        "pos": round(scores.get("pos", 0), 3),
        "neg": round(scores.get("neg", 0), 3),
        "neu": round(scores.get("neu", 1), 3),
        "emotion": emotion,
    }


def _detect_emotion(text: str, compound: float) -> str:
    text_lower = text.lower()

    confident_words = ["confident", "certain", "definitely", "absolutely", "successfully", "achieved", "led", "managed", "delivered", "proven", "demonstrated"]

    nervous_words = ["nervous", "worried", "anxious", "unsure", "hopefully", "maybe", "perhaps", "i think", "i guess", "not sure", "kind of"]

    enthusiastic_words = ["excited", "passionate", "love", "enjoy", "thrilled", "amazing", "excellent", "great", "fantastic", "wonderful", "eager"]

    tense_words = ["difficult", "challenging", "hard", "struggle", "problem", "issue", "concern", "failed", "mistake", "unfortunately"]

    scores_map = {
        "Confident": sum(1 for w in confident_words if w in text_lower),
        "Nervous": sum(1 for w in nervous_words if w in text_lower),
        "Enthusiastic": sum(1 for w in enthusiastic_words if w in text_lower),
        "Tense": sum(1 for w in tense_words if w in text_lower),
    }

    dominant = max(scores_map, key=scores_map.get)

    if scores_map[dominant] == 0:
        if compound > 0.3:
            return "Enthusiastic"
        elif compound > 0.05:
            return "Confident"
        elif compound < -0.2:
            return "Tense"
        else:
            return "Neutral"

    return dominant


def _fallback_sentiment(text: str):
    positive = ["good", "great", "excellent", "positive", "success", "achieved", "improved", "skilled", "strong", "confident", "best", "well"]

    negative = ["bad", "poor", "failed", "difficult", "problem", "issue", "weak", "struggle", "unfortunately", "unable", "worst"]

    words = text.lower().split()

    pos = sum(1 for w in words if w in positive)
    neg = sum(1 for w in words if w in negative)

    total = len(words) or 1

    compound = (pos - neg) / total * 5
    compound = max(-1, min(compound, 1))

    scores = {
        "pos": pos / total,
        "neg": neg / total,
        "neu": max(0, 1 - (pos + neg) / total),
        "compound": compound,
    }

    return compound, scores