import google.generativeai as genai
import os
import dotenv
import re
from colorama import Fore, Back, Style


dotenv.load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])


class Gemini:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat()

        with open("definition.txt", "r") as f:
            self.definition = f.read()
        
    def start(self) -> str:
        r = self.chat.send_message(self.definition)
        return r.text

    def generate(self, prompt: str, tag: str = 'entrada') -> str:
        r = self.chat.send_message(f'[{tag}]\n{prompt}')

        print(f'{Fore.YELLOW}Prompt:\n{Style.RESET_ALL}{prompt}')
        print(f'{Fore.YELLOW}Response:\n{Style.RESET_ALL}{r.text}')
        return r.text
    
    def parse(self, text: str, early_stop: str = 'entrada') -> dict:
        regex = r"\[(?P<chave>\w+)\](?P<valor>.*?)(?=\n\[|\Z)"
        data = {}
        for match in re.findall(regex, text, re.DOTALL):
            if match[0] in data: continue
            if early_stop and match[0] == early_stop: break

            data[match[0]] = match[1].strip()

        return data


if __name__ == "__main__":
    gemini = Gemini()

    r = gemini.start()
    print(r)
    while True:
        prompt = input("You: ")
        r = gemini.generate(prompt)
        print(f"Bot: {r}")
