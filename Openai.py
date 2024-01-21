from openai import OpenAI

import os


class Openai:
    def __init__(self, model="gpt-3.5-turbo-1106"):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.model = model
        self.prompt_response
        self.cost_per_token = {
            "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-1106-vision-preview": {"input": 0.01, "output": 0.03},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-32": {"input": 0.06, "output": 0.12},
            "gpt-3.5-turbo-1106": {"input": 0.0010, "output": 0.0020},
            "gpt-3.5-turbo-instruct": {"input": 0.0015, "output": 0.0020},
        }
        self.related_models = {
            "gpt-3.5-turbo-0613": "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-16k-0613": "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0301": "gpt-3.5-turbo-0613",  #
            "gpt-4-0314": "gpt-4-0613",
            "gpt-4-32k-0314": "gpt-4-32k-0613",
        }

    def send_prompt(self, prompt: str):
        self.prompt_response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        return self.prompt_response

    def calculate_cost(self) -> float:
        # this is in dollar
        # the pricing is per 1000 tokens
        model = self.get_related_model(self.model)
        if model == "":
            return -1.0
        return (
            self.prompt_response.usage.completion_tokens
            * self.cost_per_token[model]["output"]
            + self.prompt_response.usage.prompt_tokens
            * self.cost_per_token[model]["input"]
        ) / 1000

    def get_related_model(self, model: str) -> str:
        model = self.model
        if self.cost_per_token[self.model] is None:
            while self.cost_per_token[model] is None:
                if self.related_models[model] is None:
                    print("Error: the modul that ure using is not existens")
                    return ""
                else:
                    model = self.related_models[model]
        return model

    def check_model(self, model: str) -> bool:
        model = self.get_related_model(model)
        return model != ""

    def estimate_cost_prompt(self, prompt: str) -> float:
        model = self.get_related_model(self.model)
        if model == "":
            return -1.0
        # calculate the estimatatio of tokens
        return self.cost_per_token[model]["input"] * (len(prompt.split()) * (3 / 4))

    def estimate_cost_prompt_and_answer(self, prompt: str, answer_factor=0.7) -> float:
        cost_prompt = self.estimate_cost_prompt(prompt)
        # if here are negative cost then no model is found
        if cost_prompt == -1.0:
            return -1.0
        return cost_prompt + (
            answer_factor
            * len(prompt.split())
            * (3 / 4)
            * self.cost_per_token[self.model]["output"]
        )
