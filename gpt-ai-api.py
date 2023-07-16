import requests

def call_api(promptIn, input_text):
        api_key = "sk-121221213332112123"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Generate text
        prompt = f"{promptIn}"
        message = f"{input_text}"
        # API URL
        api_url = "https://api.openai.com/v1/chat/completions"
        data = {
            "model": "gpt-3.5-turbo",  # Specify the GPT model here
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ]
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API request failed with status code {response.status_code}.")
