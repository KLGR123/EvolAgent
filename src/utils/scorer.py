import re
import string
import warnings
from typing import Any
from dotenv import load_dotenv
load_dotenv()

def normalize_number_str(number_str: str) -> float:
    """
    Normalize a number string to a float.
    """

    for char in ["$", "%", ","]:
        number_str = number_str.replace(char, "")
    try:
        return float(number_str)
    except ValueError:
        print(f"String {number_str} cannot be normalized to number str.")
        return float("inf")


def split_string(
    s: str,
    char_list: list[str] = [",", ";"],
) -> list[str]:
    """
    Split a string into a list of strings using the given character list.
    """
    pattern = f"[{''.join(char_list)}]"
    return re.split(pattern, s)


def is_float(element: Any) -> bool:
    """
    Check if a string can be converted to a float.
    """
    try:
        float(element)
        return True
    except ValueError:
        return False


def normalize_str(input_str: str, remove_punct: bool = True) -> str:
    """
    Normalize a string by:
    - Removing all white spaces
    - Optionally removing punctuation (if remove_punct is True)
    - Converting to lowercase
    Parameters:
    - input_str: str, the string to normalize
    - remove_punct: bool, whether to remove punctuation (default: True)
    Returns:
    - str, the normalized string
    """
    # Remove all white spaces. Required e.g for seagull vs. sea gull
    no_spaces = re.sub(r"\s", "", input_str)

    # Remove punctuation, if specified.
    if remove_punct:
        translator = str.maketrans("", "", string.punctuation)
        return no_spaces.lower().translate(translator)
    else:
        return no_spaces.lower()


def check_prediction_contains_answer_letters_in_order(prediction: str, true_answer: str) -> bool:
    """
    Check if the prediction contains the answer letters in order.
    """
    prediction = prediction.lower()
    true_answer = true_answer.lower()
    if len(prediction) > len(true_answer) * 3:
        return False
    i = 0
    for letter in true_answer:
        if letter in prediction[i:]:
            i += prediction[i:].index(letter)
        else:
            return False
    return True


def question_scorer(
    model_answer: str,
    ground_truth: str,
) -> bool:
    """
    Check if the model answer is correct.
    """

    # if gt is a number
    if not model_answer:
        return False
    if is_float(ground_truth):
        normalized_answer = normalize_number_str(str(model_answer))
        return normalized_answer == float(ground_truth)

    # if gt is a list
    elif any(char in ground_truth for char in [",", ";"]):
        # question with the fish: normalization removes punct

        gt_elems = split_string(ground_truth)
        ma_elems = split_string(model_answer)

        # check length is the same
        if len(gt_elems) != len(ma_elems):
            warnings.warn("Answer lists have different lengths, returning False.", UserWarning)
            return False

        # compare each element as float or str
        comparisons = []
        for ma_elem, gt_elem in zip(ma_elems, gt_elems):
            if is_float(gt_elem):
                normalized_ma_elem = normalize_number_str(ma_elem)
                comparisons.append(normalized_ma_elem == float(gt_elem))
            else:
                # we do not remove punct since comparisons can include punct
                comparisons.append(
                    normalize_str(ma_elem, remove_punct=False) == normalize_str(gt_elem, remove_punct=False)
                )
        return all(comparisons)

    # if gt is a str
    else:
        return normalize_str(model_answer) == normalize_str(ground_truth)


def check_close_call(prediction: str, true_answer: str, is_correct: bool) -> bool:
    """
    Check if the prediction is close to the true answer.
    """
    if is_correct:
        return True
    else:
        if is_float(true_answer):
            return is_correct
        else:
            if (
                check_prediction_contains_answer_letters_in_order(str(prediction), str(true_answer))
                and len(str(true_answer)) * 0.5 <= len(str(prediction)) <= len(str(true_answer)) * 2
            ):
                print(f"Close call: {prediction} vs {true_answer}")
                return True
            else:
                return False

def llm_scorer(question: str, prediction: str, true_answer: str) -> bool:
    """
    Check if the prediction is correct through LLM.
    """
    import openai
    import uuid
    import os
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        max_retries=3,
    )
    response=client.chat.completions.create(
        model="gpt-4.1",
        max_tokens=2000,
        timeout=600,
        extra_headers={
            'x-ms-client-request-id': "agent-"+str(uuid.uuid4()),
        },
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are an evaluator determining if a prediction correctly answers a question.\n"
                    "# Evaluation criteria:\n"
                    "- Focus on semantic equivalence, not exact wording\n"
                    "- Consider different valid phrasings of the same answer\n"
                    "- Ignore formatting differences or extra explanations\n"
                    "Response: Only 'YES' or 'NO' - no other text.\n"
                ),
            },
            {
                "role": "user", 
                "content": (
                    "Evaluate if the prediction correctly answers the question by comparing it with the true answer.\n"
                    f"**Question:** {question}\n\n"
                    f"**Prediction:** {prediction}\n"
                    f"**True Answer:** {true_answer}\n"
                    "Is the prediction correct? Return only 'YES' or 'NO' - no other text."
                )
            }
        ],

    )
    return "yes" in response.choices[0].message.content.lower()