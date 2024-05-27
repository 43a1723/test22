from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Route để nhận yêu cầu
@app.route('/', methods=['POST', 'PUT', 'GET', 'DELETE'])
def index():
    hook_urls = os.getenv('hookurl', '').split('!!')  # Tách các webhook URL từ biến môi trường hookurl
    for hook_url in hook_urls:
        if hook_url.strip():  # Bỏ qua các khoảng trắng thừa
            # Thực hiện gửi yêu cầu đến webhook Discord
            response = requests.post(hook_url.strip(), json=request.json)
            if response.status_code != 200:
                return f"Failed to send message to {hook_url}", 500

    return "Success"

if __name__ == '__main__':
    app.run(debug=True)
