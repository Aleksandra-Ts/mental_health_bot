import requests
import json
from config import GigaChatKey, RQ_UID, URL_OAUTH, URL_GIGACHAT
from langchain.chat_models.gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


def ask_gigachat(message_history):
    payload = json.dumps({
        "model": "GigaChat",
        "messages": message_history,
        "temperature": 0.5,
        "max_tokens": 512,
    })

    headers = {
        "Content-Type": "application/json", 
        "Accept": "application/json",
        "Authorization": f"Bearer {get_giga_token()}"
    }

    response = requests.post(URL_GIGACHAT, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        assistant_reply = response.json()['choices'][0]['message']['content']
        return assistant_reply
    else:
        print(f"Ошибка при получении ответа: {response.status_code} - {response.text}")
        return None
    

def get_giga_token():
    payload = {
        "scope": "GIGACHAT_API_PERS"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": RQ_UID,
        "Authorization": f"Basic {GigaChatKey}"
    }

    response = requests.request("POST", URL_OAUTH, headers=headers, data=payload, verify=False)
    return response.json()['access_token']

user_giga_chat_active = {}
user_messages = {}

