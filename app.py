import os
from slack_bolt import App
from helpers import *
import requests
import json

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)

iterable_api_key=os.environ.get('ITERABLE_API_KEY')
rs_cold_marketing_id=int(os.environ.get('RS_COLD_MARKETING_ID'))
rs_reg_marketing_id=int(os.environ.get('RS_REG_MARKETING_ID'))
marketing_group=os.environ.get('MARKETING_GROUP')
iter_base_url='https://api.iterable.com/api'

@app.command("/list")
def get_list(ack,say,command):
    # Acknowledge command request
    ack()
    # Validate email and say channels user unsubbed from
    email = command['text']
    if validate_email(email,say):
        list_subs(say,email)
        
@app.command("/unsub-cold")
def unsub_cold(ack,say,command):
    # Acknowledge that slack received command
    ack()
    email=command['text']
    # If email valid, unsub user
    if validate_email(email,say):
        if manageSub("unsub",rs_cold_marketing_id,email,say):
            say(f"{email} unsubscribed from cold marketing!")

@app.command("/sub-cold")
def sub_user(ack,say,command):
    # Acknowledge that slack received command
    ack()
    email=command['text']
    # If email valid, sub user to cold marketing
    if validate_email(email,say):
        if manageSub("sub",rs_cold_marketing_id,email,say):
            say(f"{email} subscribed to cold marketing!")

@app.command("/unsub-reg")
def unsub_reg(ack,say,command):
    # Acknowledge that slack received command
    ack()
    email=command['text']
    # If email valid, unsub user from regular marketing
    if validate_email(email,say):
        if manageSub("unsub",rs_reg_marketing_id,email,say):
            say(f"{email} unsubscribed from regular marketing!")

@app.command("/sub-reg")
def sub_reg(ack,say,command):
    # Acknowledge that slack received command
    ack()
    email=command['text']
    # If email valid, unsub user from regular marketing
    if validate_email(email,say):
        if manageSub("sub",rs_reg_marketing_id,email,say):
            say(f"{email} subscribed to regular marketing!")

@app.command("/unsub-all")
def unsub_all(ack,say,command):
    # Acknowledge that slack received command
    ack()
    email=command['text']
    # If email valid, unsub user from regular marketing
    if validate_email(email,say):
        if manageSub("unsub",rs_cold_marketing_id,email,say) and manageSub("unsub",rs_reg_marketing_id,email,say):
            say(f"{email} unsubscribed from all marketing channels!")

@app.command("/sub-all")
def unsub_all(ack,say,command):
    # Acknowledge that slack received command
    ack()
    email=command['text']
    # If email valid, unsub user from regular marketing
    if validate_email(email,say):
        if manageSub("sub",rs_cold_marketing_id,email,say) and manageSub("sub",rs_reg_marketing_id,email,say):
            say(f"{email} subscribed to all marketing channels!") 

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))