from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from os.path import join
from tempfile import TemporaryDirectory
from index import construct_index
from file_parser import FileParser


app = Flask(__name__)
CORS(app)
json_index = None
davinci = "text-davinci-003"
turbo = "gpt-3.5-turbo"
gpt4 = "gpt-4"

@app.route("/")
def index():
    print(f"json_index={json_index}")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("files[]")
        # texts = []
        with TemporaryDirectory() as temp_dir:
            for file in files:
                file_path = join(temp_dir, file.filename)
                file.save(file_path)
                # txt = FileParser(file_path)
                # texts.append(f"BEGIN {txt.filename}")
                # texts.extend(txt.text)
                # texts.append(f"END {txt.filename}")
            global json_index
            # json_index = GPTSimpleVectorIndex.load_from_disk("index.json")
            json_index = construct_index(
                directory_path=temp_dir,
                model=turbo,
                temperature=0.5
            )
        return jsonify({"status": "success"})


@app.route("/query", methods=["POST"])
def process_query():
    question = request.form.get("question")
    print(f"\nquestion={question}")
    print(f"\njson_index={json_index}")
    answer = json_index.query(question).response
    print(f"\nanswer=\"{answer}\"")
    return jsonify({"status": "success", "response": answer})


if __name__ == "__main__":
    app.run(debug=True)
