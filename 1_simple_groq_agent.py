from http.client import responses

from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import a_color as clr_fl

load_dotenv()

agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))

while True:
    msg = input("\n\nType here for further help: ")
    if msg == "11":
        print("Exiting...")
        break
    agent.print_response(msg)
