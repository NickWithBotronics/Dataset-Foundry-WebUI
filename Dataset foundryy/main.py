from flask import Flask, render_template, request, send_file
import os
import json
import re
import openai
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\PC\Desktop\Dataset foundryy\UPLOAD_FOLDER' # Change this to your dirrectory of datasets

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')  # Assume the HTML file is named index.html and located in a templates directory

@app.route('/run_foundry', methods=['POST'])
def run_foundry():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load dataset
        with open(filepath, 'r') as f:
            dataset = [json.loads(line) for line in f.readlines()]

        output = []
        for data in dataset:
            instruction = data["instruction"]
            system = f"The user is an 8-year-old child who needs a step-by-step, simplified explanation of how to {instruction}"
            answer = ask_gpt(instruction, system)
            output.append(f"Instruction: {instruction}\nAnswer: {answer}\n")

        return '\n'.join(output)
    else:
        return 'No file part'

@app.route('/count_tokens', methods=['POST'])
def count_tokens():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        tokens = count_tokens(filepath)

        return f'The file {filename} contains {tokens} tokens.'
    else:
        return 'No file part'

@app.route('/calculate_cost', methods=['POST'])
def calculate_cost():
    version = request.form['version']
    tokens = int(request.form['tokens'])
    factor = int(request.form['factor'])

    cost = calculate_cost(version, tokens, factor)

    return f"The cost for {tokens} tokens using {version} is ${cost:.2f}"

@app.route('/format_dataset', methods=['POST'])
def format_dataset():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        delete_sections = request.form.get('delete_sections')
        phrases = request.form['phrases']

        formatted_dataset = format_dataset(filepath, delete_sections, phrases)

        return json.dumps(formatted_dataset)
    else:
        return 'No file part'

@app.route('/download_foundry_output', methods=['POST'])
def download_foundry_output():
    output = request.form['output']
    file = create_temp_file(output)
    return send_file(file, as_attachment=True, attachment_filename='foundry_output.txt')

@app.route('/download_formatted_dataset', methods=['POST'])
def download_formatted_dataset():
    dataset = json.loads(request.form['dataset'])
    file = create_temp_file(json.dumps(dataset, indent=2))
    return send_file(file, as_attachment=True, attachment_filename='formatted_dataset.json')

def ask_gpt(instruction, system):
    response = openai.Completion.create(
        engine="text-davinci-003.5",
        prompt=f"{system}\n{instruction}",
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def count_tokens(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read()

    tokens = re.findall(r'\b\w+\b', data)
    return len(tokens)

def calculate_cost(version, tokens, factor):
    cost_per_thousand = {
        'gpt3.5t': 0.002,
        'gpt4': 0.03
    }

    if version not in cost_per_thousand:
        return "Invalid version"

    cost = (tokens / 1000) * cost_per_thousand[version] * factor
    return cost

def format_dataset(filepath, delete_sections, phrases):
    with open(filepath, 'r') as file:
        dataset = json.load(file)

    formatted_dataset = []
    for data in dataset:
        input_text = data["input"]
        output_text = data["output"]

        if delete_sections:
            input_text = input_text.split("\n")[0]
            output_text = output_text.split("\n")[0]

        input_text = remove_phrases(input_text, phrases)
        output_text = remove_phrases(output_text, phrases)

        formatted_data = {
            "instruction": data["instruction"],
            "input": input_text,
            "output": output_text
        }

        formatted_dataset.append(formatted_data)

    return formatted_dataset

def remove_phrases(text, phrases):
    if phrases:
        phrases_list = phrases.split(',')
        for phrase in phrases_list:
            text = text.replace(phrase.strip(), '')

    return text

def create_temp_file(content):
    file = os.path.join(UPLOAD_FOLDER, 'temp.txt')
    with open(file, 'w') as f:
        f.write(content)
    return file

if __name__ == '__main__':
    app.run(debug=True)
