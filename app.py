from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from os.path import join
from tempfile import TemporaryDirectory
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
temp_txt_dir = ""

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        global temp_dir
        global temp_txt_dir
        with TemporaryDirectory() as temp_dir:
            with TemporaryDirectory() as temp_txt_dir:
                for file in files:
                    file_path = join(temp_dir, file.filename)
                    file.save(file_path)
                    txt = FileToTXT(file_path)
                    txt.save_to_directory(temp_txt_dir)
                construct_index(temp_txt_dir)
        return jsonify({'status': 'success'})


@app.route('/query', methods=['POST'])
def process_query():
    question = request.form.get("question")
    if len(temp_dir) > 0:
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        answer = index.query(question).response
    else:
        answer = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=None,
            temperature=0.6,
            n=1,
            stop=None,
            presence_penalty=0.6,
            frequency_penalty=0.6,
            best_of=1,
            logprobs=None,
            echo=False,
            stream=False,
        ).choices[0].text
    return jsonify({'status': 'success', 'response': answer})


if __name__ == '__main__':
    app.run(debug=True)
