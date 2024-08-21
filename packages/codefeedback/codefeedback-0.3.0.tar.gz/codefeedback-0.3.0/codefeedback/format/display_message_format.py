import random

from IPython.display import display, HTML

wrong_msgs = [
    "The response is not correct: ",
    "The code has some problems: ",
    "This isn't quite right: ",
    "There's an issue with the code: ",
    "The answer is incorrect: ",
    "The provided solution has errors: ",
    "Check your code, it's not correct: ",
    "Something went wrong: ",
    "This response is not accurate: ",
    "Review your code, it contains mistakes: ",
    "Incorrect submission: ",
    "The following code needs revision: ",
    "Error detected: ",
    "The code does not work as expected: ",
    "There are issues with the provided response: "
]

correct_msgs = [
    "Well done! The response is correct.",
    "Great job! The code is accurate.",
    "Nice work! The solution is correct.",
    "Good job! Your code is working.",
    "Excellent! The answer is correct.",
    "That's right! The code is correct.",
    "Well done! Your solution is accurate.",
    "Perfect! The code runs as expected.",
    "Correct solution.",
    "Great work! The response is correct.",
    "Your code is correct.",
    "Fantastic! Everything looks good.",
    "That's correct! Nice work.",
    "Good job! The code behaves as expected."
]


def display_feedback(is_correct):
    if is_correct:
        html_code = f'<p style="color:green;">{random.choice(correct_msgs)}</p>'
        display(HTML(html_code))
    else:
        html_code = f'<p style="color:red;">{random.choice(wrong_msgs)}</p>'
        display(HTML(html_code))

