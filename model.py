import openai
import os
import backoff

open_api_key = os.getenv("OPENAI_API_KEY")
if open_api_key != None:
    openai.api_key = open_api_key 

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def get_response(prompt, model="gpt-3.5-turbo", temperature=0, max_tokens=300, n=1, stop=None) -> list:
    messages = [{"role": "user", "content": prompt}]
    out = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=1, stop=stop)
    response = {}
    response["content"] = [choice["message"]["content"] for choice in out["choices"]]
    # response["content"] = [out["choices"][0]["message"]["content"]]
    response["prompt_tokens"] = out["usage"]["prompt_tokens"]
    response["completion_tokens"] = out["usage"]["completion_tokens"]
    return response