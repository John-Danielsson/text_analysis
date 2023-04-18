from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import tempfile
from llama_index import GPTSimpleVectorIndex
from index import construct_index
from file_to_txt import FileToTXT

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        print("FILES:")
        # TODO: Convert each file to .txt and use Nikulina's code.
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in files:
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                print(file.filename)
                txt = FileToTXT(file_path)
                txt.save_to_directory("test_txts")
        print("TEMP_DIR:")
        print(f"type(temp_dir)={type(temp_dir)}")
        print(f"      temp_dir={temp_dir}")
        construct_index("test_txts")
        print("index construction successful")
        # TODO: Implement a function that constructs a JSON index using the uploaded files
        #     The function takes in a directory path (str)
        #     and saves a file called 'index.json' to the current working directory.
        return jsonify({'status': 'success'})


@app.route('/query', methods=['POST'])
def process_query():
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    print("   index=", index)
    if not index:
        return jsonify({'status': 'error', 'message': 'No index available. Please upload files first.'})
    # TODO: Implement a function to answer questions.
    #     This function takes in a question (str) and
    #     returns an answer generated by the ChatGPT API.
    question = request.form.get("question")
    answer = str(index.query(question))
    print("question=", question)
    print("  answer=", answer)
    return jsonify({'status': 'success', 'response': answer})


if __name__ == '__main__':
    app.run(debug=True)
