import re

FILLER_WORDS = [
    "um", "uh", "er", "ah", "uhh", "umm", "hmm",
    "like", "basically", "actually", "literally",
    "you know", "kind of", "sort of", "i mean",
    "right", "okay so", "so yeah", "well",
    "stuff", "things", "whatever", "honestly",
]

def detect_filler_words(text: str) -> dict:

    text_lower = text.lower()
    words = text_lower.split()

    total_words = len(words) if words else 1

    found = {}

    multi_word = [f for f in FILLER_WORDS if " " in f]
    single_word = [f for f in FILLER_WORDS if " " not in f]

    for filler in multi_word:
        count = text_lower.count(filler)

        if count > 0:
            found[filler] = count

    for filler in single_word:

        pattern = r'\b' + re.escape(filler) + r'\b'
        count = len(re.findall(pattern, text_lower))

        if count > 0:
            found[filler] = count

    total_count = sum(found.values())

    filler_ratio = total_count / total_words

    if filler_ratio <= 0.02:
        fluency_score = 95

    elif filler_ratio <= 0.05:
        fluency_score = 85

    elif filler_ratio <= 0.10:
        fluency_score = 70

    elif filler_ratio <= 0.15:
        fluency_score = 55

    elif filler_ratio <= 0.20:
        fluency_score = 40

    else:
        fluency_score = 25

    if total_count == 0:
        fluency_score = 98

    return {
        "found": found,
        "total_count": total_count,
        "total_words": total_words,
        "filler_ratio": round(filler_ratio * 100, 1),
        "fluency_score": fluency_score,
    }