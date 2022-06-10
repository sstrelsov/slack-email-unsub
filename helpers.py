from slack_bolt import App
import os
import requests
from app import rs_cold_marketing_id,rs_reg_marketing_id,iter_base_url,iterable_api_key,marketing_group

def validate_email(email,say):
    url=iter_base_url+'/users/{}?api_key={}'.format(email,iterable_api_key)
    response=requests.get(url)
    # Use Invalid email response text to confirm valid email format
    if 'Invalid email' in response.text:
        say("ERROR: Invalid email format. Make sure to use 'email@example.com'")
        return False
    # Use empty response text to confirm whether email in Iterable database
    elif response.text == "{{}}".format(1):
        say(f"ERROR: Valid email format, but {email} not in Iterable database.")
        return False
    else:
        return True

def manageSub(type,id,email,say):
    # Get user's URL
    url = iter_base_url+'/subscriptions/{}/{}/user/{}?api_key={}'.format(marketing_group,id,email,iterable_api_key)
    if type == "unsub":
        response = requests.delete(url)
    elif type == "sub":
        response = requests.patch(url)
    else:
        print("ERROR: Check that type is either 'sub' or 'unsub'")
        return
    # Check response and confirm subscription or deletion
    if response.status_code == 202:
                return True         
    else:
        say(f"ERROR: Code {response.status_code}. Couldn't subscribe or unsubscribe user.")
        return False

def list_subs(say,email):
    # Get user data and isolate id's of channels unsubscribed from
    url=iter_base_url+'/users/{}?api_key={}'.format(email,iterable_api_key)
    response = requests.get(url)
    unsubbed_channel_ids = response.json()['user']['dataFields']['unsubscribedChannelIds']
    # Map channel names to channel ids
    channel_ids = [rs_cold_marketing_id,rs_reg_marketing_id]
    
    for id in unsubbed_channel_ids:
        if id in channel_ids:
            channel_ids.remove(id)
    # Say channel names user is subscribed to
    if channel_ids:
        channel_names = []
        for id in channel_ids:
            if id == rs_cold_marketing_id:
                channel_names.append("Cold Marketing Channel")
            if id == rs_reg_marketing_id:
                channel_names.append("Regular Marketing Channel")
        if len(channel_names) > 1:
            channel_output = ", ".join(channel_names)
        else:
            channel_output = channel_names[0]
        say(f"{email} is subscribed to the following marketing channels: {channel_output}")
    else:
        say(f"{email} not subscribed to any marketing channels!")