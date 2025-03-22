from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/generate_post', methods=['POST'])
def generate_post():
    prompt = request.form['prompt']
    temperature = float(request.form['temperature'])
    
    # Load the system prompt
    with open('system prompts/Social media post CoT.json', 'r') as f:
        system_prompt = json.load(f)
    
    # Update temperature in the config
    system_prompt['temperature'] = temperature
    
    # Your existing model generation code here
    # ...
    
    return render_template('index.html', 
                         generated_post=generated_post, 
                         user_prompt=prompt)