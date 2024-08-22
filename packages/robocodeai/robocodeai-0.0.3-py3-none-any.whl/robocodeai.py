from g4f.client import Client
import asyncio
import sys

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

languages = {
    'en': 'talk to me using English language',
    'fr': 'Vous devez communiquer avec moi uniquement en francais',
    'ru': 'общайся со мной на русском языке',
    'ua': 'спілкуйся зі мною українською мовою'
}

class AI:
    def __init__(self, language: str) -> None:
        self.client = Client()
        self.message_history = []
        self.language = language

    def get_answer(self, question: str) -> str:
        user_message = {'role': 'user', "content": question}
        self.message_history.append(user_message)
        ai_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message_history,
        ).choices[0].message.content
        self.message_history.append({'role': 'assistant', 'content': ai_response})
        return ai_response

    def set_character(self, character: str) -> None:
        self.message_history.append({'role': 'user', "content": languages[self.language] + character})