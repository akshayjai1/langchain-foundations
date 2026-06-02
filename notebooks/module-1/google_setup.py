from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI

modelName1 = "gemini-2.5-flash-lite"
model1 = init_chat_model(modelName1)

model2 = ChatGoogleGenerativeAI(modelName1)
