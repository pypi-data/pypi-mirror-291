import json
import os

from openai import OpenAI

open_ai_api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=open_ai_api_key)
model_engine = "gpt-3.5-turbo"


def get_prompt(prompt_name, json_filename, prompt_category):
    """
    get prompt by its name frm the prompts.json file
    """
    file_path = os.path.join(os.path.dirname(__file__), json_filename)
    with open(file_path, 'r') as file:
        prompts = json.load(file)[prompt_category]
        return prompts.get(prompt_name, None)


def format_prompt(prompt, **kwargs):
    """
    the prompt contains placeholder, use this method to replace the placeholder with variables
    """
    return prompt.format(**kwargs)


def ask_chatgpt(prompt, temperature=0.7):
    explanation_completions = client.chat.completions.create(
        model=model_engine,
        messages=[
            {
                "role": "assistant",
                "content": prompt
            }
        ],
        temperature=temperature,
        stop=None,
        n=1,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5,

    )

    # Extract the first response
    all_responses = [choice.message.content for choice in explanation_completions.choices]
    return all_responses[0]


def ask_chatgpt_for_json(prompt, temperature=0.7):
    explanation_completions = client.chat.completions.create(
        model=model_engine,
        messages=[
            {
                "role": "assistant",
                "content": prompt
            }
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
        stop=None,

    )

    # Extract the first response
    all_responses = [choice.message.content for choice in explanation_completions.choices]
    return all_responses[0]


def prepare_prompt_and_send_to_chatgpt(prompt_name, json_filename, prompt_category, is_json=False, **kwargs):
    """
    This method prepares a prompt using a specified prompt name and keyword arguments, sends the formatted prompt to
    ChatGPT for a response, and returns the HTML response.

    Parameters:
    - prompt_name (str): The name of the prompt to be retrieved from prompts.json.
    - **kwargs: Arbitrary keyword arguments to be formatted into the prompt.

    Returns:
    - str: A string containing the HTML response data from ChatGPT.
    """
    prompt = get_prompt(prompt_name, json_filename, prompt_category)
    formatted_prompt = prompt.format(**kwargs)
    # Modify the request to ask for an HTML response
    if is_json:
        json_file = ask_chatgpt_for_json(formatted_prompt)
        return json_file
    open_ai_response = ask_chatgpt(formatted_prompt)
    return open_ai_response
