from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

openai_model = init_chat_model(model='gpt-5-nano')
