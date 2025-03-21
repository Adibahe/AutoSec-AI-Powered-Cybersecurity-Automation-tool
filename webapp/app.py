from flask import Flask, render_template, request, jsonify
from NmapHandler import scanner

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_tool', methods=['POST'])
def run_tool():
    tool = request.form.get('tool')
    user_query = request.form.get('user_query')
    
    if tool == 'nmap':
        result = scanner(user_query)
        return jsonify(result=result)
    # Add more tools here as needed

if __name__ == '__main__':
    app.run(debug=True)