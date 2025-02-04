from openai import OpenAI

from ..config import CONFIG

EXTRACT_PROMPT = "Extract the following details from the input: location, cuisine type, budget, number of people, time.\n\nInput: {user_input}\n\nDetails:"

ai = OpenAI(api_key=CONFIG["OPENAI_API_KEY"])


def extract_details(user_input):
    response = ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and a restaurant finder."},
            {"role": "user", "content": EXTRACT_PROMPT.format(user_input=user_input)},
        ],
    )

    details = response.choices[0].message.content.strip()
    return details
