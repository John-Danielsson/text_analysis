from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from os.path import join
from tempfile import TemporaryDirectory
from index import construct_index
from sentence_transformers import SentenceTransformer


app = Flask(__name__)
CORS(app)
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
json_index = None


@app.route("/")
def index():
    print(f"json_index={json_index}")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("files[]")
        with TemporaryDirectory() as temp_dir:
            for file in files:
                file_path = join(temp_dir, file.filename)
                file.save(file_path)
                txt = FileToTXT(file_path)
            global json_index
            json_index = construct_index(temp_dir)
        return jsonify({"status": "success"})


@app.route("/query", methods=["POST"])
def process_query():
    question = request.form.get("question")
    print(f"\nquestion={question}")
    print(f"json_index={json_index}")
    answer = json_index.query(question).response
    print(f"answer=\"{answer}\"")
    return jsonify({"status": "success", "response": answer})


if __name__ == "__main__":
    app.run(debug=True)
