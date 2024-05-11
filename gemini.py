import google.generativeai as genai
import os
import dotenv

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
        return r

    def generate(self, prompt: str) -> str:
        r = self.chat.send_message(prompt)
        return r.text


if __name__ == "__main__":
    gemini = Gemini()

    r = gemini.start()
    print(r)
    while True:
        prompt = input("You: ")
        r = gemini.generate(prompt)
        print(f"Bot: {r}")
