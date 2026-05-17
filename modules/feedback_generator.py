def generate_feedback(results: dict, answer_text: str) -> list:

    feedback = []

    semantic = results.get("semantic", {})
    sentiment = results.get("sentiment", {})
    filler = results.get("filler", {})
    grammar = results.get("grammar", {})
    confidence = results.get("confidence", {})

    word_count = len(answer_text.split()) if answer_text.strip() else 0

    sem_score = semantic.get("score", 0)

    if sem_score >= 75:
        feedback.append({
            "message": "Your answer is highly relevant to the question. Great job covering the key points!",
            "type": "positive"
        })

    elif sem_score >= 50:
        feedback.append({
            "message": "Your answer is moderately relevant. Try to address the core of the question more directly and use specific examples.",
            "type": "info"
        })

    else:
        feedback.append({
            "message": "Your answer seems off-topic. Re-read the question carefully and structure your response around it directly.",
            "type": "warning"
        })

    if word_count < 30:
        feedback.append({
            "message": "Your answer is too short. Aim for at least 80–150 words to demonstrate depth and confidence.",
            "type": "warning"
        })

    elif word_count > 300:
        feedback.append({
            "message": "Your answer is quite long. Try to be more concise — interviewers prefer focused, structured answers.",
            "type": "info"
        })

    else:
        feedback.append({
            "message": f"Good answer length ({word_count} words). You've provided enough detail without rambling.",
            "type": "positive"
        })

    filler_count = filler.get("total_count", 0)
    fluency = filler.get("fluency_score", 100)

    if filler_count == 0:
        feedback.append({
            "message": "Excellent fluency! No filler words detected — your communication sounds polished and professional.",
            "type": "positive"
        })

    elif filler_count <= 3:
        found_list = ", ".join(filler.get("found", {}).keys())

        feedback.append({
            "message": f"Minor filler words detected ({found_list}). Practice replacing them with a short pause for a more confident delivery.",
            "type": "info"
        })

    else:
        found_list = ", ".join(filler.get("found", {}).keys())

        feedback.append({
            "message": f"High filler word usage ({filler_count} instances: {found_list}). This reduces perceived confidence. Practice speaking with deliberate pauses instead.",
            "type": "warning"
        })

    gram_score = grammar.get("score", 100)
    gram_errors = grammar.get("error_count", 0)

    if gram_score >= 90:
        feedback.append({
            "message": "Your grammar is excellent. Clear and correct language makes a strong impression.",
            "type": "positive"
        })

    elif gram_score >= 70:
        feedback.append({
            "message": f"A few grammar issues detected ({gram_errors} errors). Proofread your answers and practice correct sentence structure.",
            "type": "info"
        })

    else:
        feedback.append({
            "message": f"Significant grammar issues found ({gram_errors} errors). Focus on sentence structure, tense consistency, and punctuation.",
            "type": "warning"
        })

    emotion = sentiment.get("emotion", "Neutral")
    compound = sentiment.get("compound", 0)

    if emotion == "Confident" or compound > 0.3:
        feedback.append({
            "message": "You sound confident and positive — exactly the tone interviewers love to hear!",
            "type": "positive"
        })

    elif emotion == "Enthusiastic":
        feedback.append({
            "message": "Your enthusiasm comes through clearly. Channel that energy into specific, structured examples for maximum impact.",
            "type": "positive"
        })

    elif emotion == "Nervous":
        feedback.append({
            "message": "Your tone sounds slightly uncertain. Use direct, assertive language — replace 'I think maybe' with 'I am confident that'.",
            "type": "warning"
        })

    elif emotion == "Tense":
        feedback.append({
            "message": "Your response has a tense tone. Try to balance challenges with outcomes and lessons learned to show resilience.",
            "type": "info"
        })

    answer_lower = answer_text.lower()

    has_numbers = any(char.isdigit() for char in answer_text)

    has_result_words = any(
        w in answer_lower
        for w in [
            "result",
            "outcome",
            "achieved",
            "increased",
            "reduced",
            "improved",
            "led to"
        ]
    )

    has_action_words = any(
        w in answer_lower
        for w in [
            "implemented",
            "designed",
            "built",
            "managed",
            "led",
            "created",
            "developed"
        ]
    )

    if not has_numbers:
        feedback.append({
            "message": "Add measurable achievements (e.g., 'increased efficiency by 30%', 'managed a team of 5'). Quantified results are more persuasive.",
            "type": "info"
        })

    if not has_result_words:
        feedback.append({
            "message": "Mention outcomes or results of your actions. Interviewers want to know the impact of what you did, not just what you did.",
            "type": "info"
        })

    if has_action_words:
        feedback.append({
            "message": "Strong use of action verbs. This demonstrates initiative and makes your answer more dynamic.",
            "type": "positive"
        })

    overall = confidence.get("overall", 0)

    if overall >= 75:
        feedback.append({
            "message": "Overall strong performance! You are well-prepared for this type of interview question.",
            "type": "positive"
        })

    elif overall >= 50:
        feedback.append({
            "message": "Decent performance with room to improve. Focus on the areas flagged above and practice with more structured answers.",
            "type": "info"
        })

    else:
        feedback.append({
            "message": "This answer needs significant improvement. Practice using frameworks like STAR (Situation, Task, Action, Result) to structure your responses.",
            "type": "warning"
        })

    return feedback