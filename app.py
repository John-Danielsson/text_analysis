from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import tempfile
from llama_index import GPTSimpleVectorIndex
from index import construct_index
from file_to_txt import FileToTXT
import openai


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


temp_dir = ""


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in files:
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                txt = FileToTXT(file_path)
                txt.save_to_directory("txts")
        construct_index("txts")
        return jsonify({'status': 'success'})


@app.route('/query', methods=['POST'])
def process_query():
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    question = request.form.get("question")
    answer = ""
    # if files in temp_dir:
    #     answer = index.query(question).response
    # else:
    #     answer = openai.Completion.create(
    #         engine="text-davinci-003",
    #         prompt=question,
    #         max_tokens=1024,
    #         temperature=0.7,
    #         n=1,
    #         stop=None,
    #         presence_penalty=0.6,
    #         frequency_penalty=0.6,
    #         best_of=1,
    #         logprobs=None,
    #         echo=False,
    #         stream=False,
    #         response_format="json",
    #     ).choices[0].text
    if not index:
        return jsonify({'status': 'error', 'message': 'No index available. Please upload files first.'})
    answer = index.query(question).response
    return jsonify({'status': 'success', 'response': answer})


if __name__ == '__main__':
    app.run(debug=True)
