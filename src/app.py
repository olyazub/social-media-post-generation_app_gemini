from flask import Flask, render_template, redirect, url_for, session, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField
import google.generativeai as genai
from config import Config
import json
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "dev" 
bootstrap = Bootstrap5(app)

# Initialize Gemini
config = Config()
genai.configure(api_key=config.gemini_api_key)

class PostForm(FlaskForm):
    topic = TextAreaField(label="Write a post about:")
    submit = SubmitField('Generate')

def load_prompt_config():
    with open('system prompts/Social media post CoT.json', 'r') as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    if form.validate_on_submit():

        cot_config = load_prompt_config()
        temperature = float(request.form.get('temperature', 1.75))
        

        cot_prompt = (cot_config["systemInstruction"]["parts"][0]["text"] + "\n" + 
                    f"write a post about {form.topic.data}")
        

        model_params = {
            "temperature": temperature,
            "top_p": cot_config["parameters"]["topP"],
        }

        cot_model_1 = genai.GenerativeModel(
            model_name=cot_config["model"],
            generation_config=model_params
        )
        
        cot_model_2 = genai.GenerativeModel(
            model_name=cot_config["model"],
            generation_config=model_params
        )
        

        response_1 = cot_model_1.generate_content(cot_prompt)
        response_2 = cot_model_2.generate_content(cot_prompt)
        
        logging.debug(f"First response: {repr(response_1.text)}")
        logging.debug(f"Second response: {repr(response_2.text)}")
        

        return render_template("post.html",
                             user_topic=form.topic.data,
                             temperature=temperature,
                             cot_post=response_1.text,
                             zeroshot_post=response_2.text)
    
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
