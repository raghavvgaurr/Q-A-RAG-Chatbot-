from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage,SystemMessage
from typing import Literal,TypedDict,Annotated
import operator
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()

class Chatbot(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_message(state:Chatbot)->Chatbot:
    messages=state['messages']
    prompt=[SystemMessage(content=f'You are a helpful AI assistant. Help to solve the users problem. {messages}')]
    model=ChatGroq(model='openai/gpt-oss-120b',temperature=0.7)
    response=model.invoke(prompt)

    return {'messages':[response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)
graph=StateGraph(Chatbot)
graph.add_node('chat_message',chat_message)

graph.add_edge(START,'chat_message')
graph.add_edge('chat_message',END)

workflowtbot=graph.compile(checkpointer=checkpointer)
CONFIG={'configurable': {'thread_id':'thread-id'}}


all_threads=set()
def retrive_allthreads():
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)





#test
'''final_state=workflowtbot.invoke({'messages':[HumanMessage(content='What is the capital of India? ')]},config=CONFIG)
print(final_state)'''





