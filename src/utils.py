import slack
import os
from dotenv import load_dotenv
load_dotenv()

client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))

def add_message_to_slack(message):
    client.chat_postMessage(channel='#test',text=message)