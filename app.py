from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from os.path import join
from tempfile import TemporaryDirectory
# from llama_index import GPTSimpleVectorIndex
from index import construct_index
from file_to_txt import FileToTXT
# import openai
from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
CORS(app)
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
# embeddings = None
json_index = None


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
            # with TemporaryDirectory() as temp_txt_dir:
            for file in files:
                file_path = join(temp_dir, file.filename)
                file.save(file_path)
                txt = FileToTXT(file_path)
                # texts.extend(txt.text_in_list())
                # txt.save_to_directory(temp_txt_dir)
            global json_index
            json_index = construct_index(temp_dir)
            # global embeddings
            # embeddings = model.encode(sentences=texts)[0].reshape(1, -1)
        # global json_index
        # json_index = GPTSimpleVectorIndex.load_from_disk("index.json")
        return jsonify({"status": "success"})


@app.route("/query", methods=["POST"])
def process_query():
    question = request.form.get("question")
    print(f"\nquestion={question}")
    # max_cosine_similarity = 0.0
    # if embeddings is not None:
    #     q_embedding = model.encode(sentences=[question])[0].reshape(1, -1)
        # max_cosine_similarity = max(cosine_similarity(X=embeddings, Y=q_embedding))
        # print(f"maximum cosine similarity={max_cosine_similarity}")
    # answer = ""
    print(f"json_index={json_index}")
    answer = json_index.query(question).response
    # I may work on this code below at a later date. It's intended to switch between asking questions
    # of the provided files and asking questions of the generic ChatGPT API, and distinguish
    # between the user's questions appropriately.
    # if json_index is not None and max_cosine_similarity > 0.12 and not question.startswith("."):
    #     print("json_index present")
    #     print("question relevant to json_index")
    #     answer = json_index.query(question).response
    # else:
    #     # 10.01 - 9.85 = $0.16 for 334 pages
    #     # TODO: Find total number of pages among Zoltan PDFs + Apple + Amazon + LMC 334
    #     # $0.96 to process all that (above)
    #     print("json_index NOT present OR question NOT relevant to json_index")
    #     answer = openai.Completion.create(
    #         engine="gpt-3.5-turbo",
    #         prompt=question,
    #         max_tokens=1600,
    #         temperature=0.6,
    #         n=1,
    #         stop=None,
    #         presence_penalty=0.6,
    #         frequency_penalty=0.6,
    #         best_of=1,
    #         logprobs=None,
    #         echo=False,
    #         stream=False,
    #     ).choices[0].text
    print(f"answer=\"{answer}\"")
    return jsonify({"status": "success", "response": answer})


if __name__ == "__main__":
    app.run(debug=True)
