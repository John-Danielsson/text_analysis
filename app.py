from os.path import join
from os import kill, getpid
import signal
from tempfile import TemporaryDirectory

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from file_parser import FileParser
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from prompt_engineer import primer_str, prompt_engineer_str

app = Flask(__name__)
CORS(app)
json_index = None
davinci = "text-davinci-003"
turbo = "gpt-3.5-turbo"
gpt4 = "gpt-4"


def primer(n_files: int) -> str:
    """Returns the beginning of the prompt-engineered version of the file(s)."""
    return primer_str.format(n_files)


def prompt_engineer(file: FileParser, i: int) -> str:
    """Returns a prompt-engineered version of the file."""
    return prompt_engineer_str.format(i, file.filename, str(file), i)


@app.route("/")
def index():
    """Displays the app's HTML/CSS/JS."""
    print(f"json_index={json_index}")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Handles files uploads in PDF, HTML, EPUB, DOC, DOCX, and TXT."""
    if request.method == "POST":
        files = request.files.getlist("files[]")
        print(f"number of files={len(files)}")
        with TemporaryDirectory() as temp_dir:
            with TemporaryDirectory() as txt_dir:
                txt_file_text = primer(len(files))
                for i in range(len(files)):
                    file_name = secure_filename(files[i].filename)
                    print(f"file name={file_name}")
                    file_path = join(temp_dir, file_name)
                    files[i].save(file_path)
                    file_parser = FileParser(filepath=file_path)
                    txt_file_text += prompt_engineer(file_parser, i+1)
                with open(file=join(txt_dir, "data.txt"), mode="w", errors="ignore") as f:
                    f.write(txt_file_text)
                global json_index
                documents = SimpleDirectoryReader(txt_dir).load_data()
                json_index = GPTVectorStoreIndex.from_documents(documents)
                print("index construction success")
        return jsonify({"status": "success"})


@app.route("/query", methods=["POST"])
def process_query():
    """Handles user questions over the files uploaded. If no files have been,
    uploaded, the app simply indicates that no files have been uploaded yet."""
    question = request.form.get("question")
    print(f"\nquestion=\"{question}\"")
    print(f"\njson_index={json_index}")
    print("\nprocessing answer...")
    if json_index is not None:
        answer = json_index.query(question).response
        print(f"\nanswer=\"{answer}\"")
    else:
        print("\nindex not present, alerting user")
        answer = "There are no files. Please upload at least 1 file to ask questions."
    return jsonify({"status": "success", "response": answer})


app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handles excessively large files."""
    response = jsonify({"status": "error", "message": "Too much content uploaded. Maximum allowed size is 500MB."})
    response.status_code = 413
    return response


def shutdown_server() -> None:
    """Shuts down the app from the user's click."""
    kill(getpid(), signal.SIGTERM)


@app.route("/shutdown", methods=["POST"])
def shutdown() -> str:
    """Handles shutting down the app from the user's click."""
    shutdown_server()
    print("Server shutting down...")
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(debug=True)
