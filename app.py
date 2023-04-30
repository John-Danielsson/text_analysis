from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from os.path import join
from tempfile import TemporaryDirectory
from file_parser import FileParser
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

app = Flask(__name__)
CORS(app)
json_index = None
davinci = "text-davinci-003"
turbo = "gpt-3.5-turbo"
gpt4 = "gpt-4"


def primer(n_files: int) -> str:
    return f"""
All of the text after the 10 consecutive asterisks consists of text
extracted from {n_files} files in .pdf, .txt, .html, .docx, or .epub format.
The text of each file is formatted as follows:

==========
BEGIN FILE (file number)
File Name: (file name)
File Content:
(text of file)
END FILE (file number)
==========

**********

"""


def prompt_engineer(file_parser: FileParser, i: int) -> str:
    return f"""

==========
BEGIN FILE {i}
File Name: {file_parser.filename}
File Content:
{str(file_parser)}
END FILE {i}
==========

"""


@app.route("/")
def index():
    print(f"json_index={json_index}")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("files[]")
        print(f"number of files={len(files)}")
        with TemporaryDirectory() as temp_dir:
            with TemporaryDirectory() as txt_dir:
                txt_file_text = primer(len(files))
                for i in range(len(files)):
                    print(f"file name={files[i].filename}")
                    file_path = join(temp_dir, files[i].filename)
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
    question = request.form.get("question")
    print(f"\nquestion=\"{question}\"")
    print(f"\njson_index={json_index}")
    print("processing answer...")
    answer = json_index.query(question).response
    print(f"\nanswer=\"{answer}\"")
    return jsonify({"status": "success", "response": answer})


if __name__ == "__main__":
    app.run(debug=True)
