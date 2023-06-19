from model import get_response

prompt = """Hello
"""

if __name__ == '__main__':

    response = get_response(prompt, model='gpt-3.5-turbo', temperature=0, max_tokens=2000)
    print(response)
    