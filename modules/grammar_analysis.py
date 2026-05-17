def analyze_grammar(text: str) -> dict:

    errors = []

    try:
        import language_tool_python

        tool = language_tool_python.LanguageTool("en-US")
        matches = tool.check(text)

        tool.close()

        for match in matches:

            msg = match.message

            if match.replacements:
                suggestion = match.replacements[0]
                msg += f" → Suggestion: '{suggestion}'"

            errors.append(msg)

    except Exception:
        errors = _fallback_grammar_check(text)

    error_count = len(errors)

    word_count = len(text.split()) if text.strip() else 1

    penalty_per_error = max(
        5,
        100 // max(word_count // 5, 1)
    )

    score = max(
        0,
        100 - error_count * penalty_per_error
    )

    return {
        "errors": errors,
        "error_count": error_count,
        "score": round(score, 1),
        "word_count": word_count,
    }


def _fallback_grammar_check(text: str) -> list:

    import re

    errors = []

    sentences = re.split(r'[.!?]+', text)

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if sentence and sentence[0].islower():
            errors.append(
                f"Sentence should start with a capital letter: '{sentence[:40]}...'"
            )

        if "  " in sentence:
            errors.append("Avoid double spaces in text.")

        words = sentence.lower().split()

        for i in range(len(words) - 1):

            if words[i] == words[i + 1] and len(words[i]) > 2:
                errors.append(
                    f"Repeated word detected: '{words[i]}'"
                )

    if len(text.split()) < 10:
        errors.append(
            "Answer is very short. Consider providing more detail."
        )

    if text.strip() and text.strip()[-1] not in ".!?":
        errors.append(
            "Consider ending your answer with proper punctuation."
        )

    return errors