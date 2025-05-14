-Create venv
python -m venv venv
source venv/bin/activate
windows
.\venv\Scripts\activate

pip install -r requirements.txt

ollama run llama3.2:1b    

loader=WebBaseLoader("https://www.investopedia.com/how-nvidia-makes-money-4799532")

langraph dev 

#display graph
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
# load llm

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

#os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


llm=ChatGroq(model="qwen-2.5-32b")
#llm = ChatOpenAI(model="gpt-4o")
result=llm.invoke("Hello")
result


