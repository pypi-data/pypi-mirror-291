import openai
from dotenv import load_dotenv
import os

from codefeedback.format.general_format import ai_content_format


def ai_response(response, answer):
    if len(answer) < 100:
        model = "gpt-4o"
    elif len(answer) < 200:
        model = "gpt-4-turbo"
    else:
        model = "gpt-4"
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        return "No api key is provided"

    openai.api_key = api_key
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user",
                       "content": f"Given the following student response: \n\"{response}\"\n and answer: \n\"{answer}\"\n"
                                  f"Give me feedbacks of the response in the form of 'Bool' (True or False), 'Feedback' (The feedback of the response"}]
        )
    except openai.error.AuthenticationError:
        return "Incorrect api key"
    reply_content = completion.choices[0].message.content
    return reply_content


def ai_prompt_check(response, answer):
    reply_content = ai_response(response, answer)
    if "No api key is provided" == reply_content or "Incorrect api key" == reply_content:
        return False, reply_content
    is_correct, feedback = ai_content_format(reply_content)
    return is_correct, feedback


