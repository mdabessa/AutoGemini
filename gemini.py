import google.generativeai as genai
import google.ai.generativelanguage_v1beta.types as types
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
        r = self.chat.send_message(f'[{tag}]\n{prompt}\n')
        return r.text
    
    def parse(self, text: str, early_stop: str = ['entrada', 'saida']) -> dict:
        # early_stop para descartar previsões de texto que são entradas do usuário
        
        regex = r"\[(?P<chave>\w+)\](?P<valor>.*?)(?=\n\[|\Z)"
        data = {}
        for match in re.findall(regex, text, re.DOTALL):
            if match[0] in data: continue
            if early_stop and match[0] in early_stop: break

            data[match[0]] = match[1].strip()

        return data
    
    def send_message(self, message: str, tag: str = 'entrada') -> dict:
        r = self.generate(message, tag=tag)
        r = self.parse(r)

        # editar o histórico de conversa, limpando as tags desnecessárias
        out = ''
        for key, value in r.items():
            out += f'[{key}]\n{value}'

        part = types.content.Part(text=out)
        self.chat.history[-1].parts[-1] = part

        print(f'{Fore.YELLOW}Prompt:\n{Style.RESET_ALL}{message}')
        print(f'{Fore.YELLOW}Response:\n{Style.RESET_ALL}{out}')

        return r


if __name__ == "__main__":
    gemini = Gemini()

    r = gemini.start()
    print(r)
    while True:
        prompt = input("You: ")
        r = gemini.send_message(prompt)
        print(f"Bot: {r}")
