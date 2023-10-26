from flask import Flask, render_template, request, jsonify
import requests
import accessScript

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_url', methods=['POST'])
def process_url():
    url = request.form['url']
    response = requests.get(url)
    html_content = response.text

    data = accessScript.detect_data(html_content)

    return data

if __name__ == '__main__':
    app.run(debug=True, port=5001)

