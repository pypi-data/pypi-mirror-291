from openai import OpenAI
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret



class Embed:
    def __init__(self):
        self.client = OpenAI()

    def invoke(self, text):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding


class OpenAILLM:
    def __init__(self, model_id = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model_id = model_id

    def invoke(self, prompt, schema=None):
        messages = [{"role": "user", "content": prompt}]
        try:
            if schema is None:
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                )
                return response.choices[0].message.content
            else:
                response = self.client.beta.chat.completions.parse(
                    model=self.model_id,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                    response_format=schema,
                )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return None
        
class MiniMax:
    def __init__(self):
        print("initialize minimax")
        self.client = OpenAIGenerator(
            api_base_url="https://api.minimax.chat/v1",
            api_key=Secret.from_env_var("MINIMAX_API_KEY"),
            model="abab6.5s-chat"
        )

    def invoke(self, prompt):
        response = self.client.run(prompt)
        return response["replies"]