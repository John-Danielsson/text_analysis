from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from os.path import join
from tempfile import TemporaryDirectory
from llama_index import GPTSimpleVectorIndex
from index import construct_index
from file_to_txt import FileToTXT
import openai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import reshape, mean


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embeddings = None
index = None


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        texts = []
        with TemporaryDirectory() as temp_dir:
            with TemporaryDirectory() as temp_txt_dir:
                for file in files:
                    file_path = join(temp_dir, file.filename)
                    file.save(file_path)
                    txt = FileToTXT(file_path)
                    texts.extend(txt.text_in_list())
                    txt.save_to_directory(temp_txt_dir)
                construct_index(temp_txt_dir)
        global embeddings
        embeddings = model.encode(sentences=texts)
        global index
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        return jsonify({'status': 'success'})


@app.route('/query', methods=['POST'])
def process_query():
    question = request.form.get("question")
    cosine_similarity = 0.0
    print(f"                 question={question}")
    if embeddings is not None:
        question_embedding = model.encode(sentences=[question])[0].reshape(1, -1)
        cosine_similarity = max(cosine_similarity(X=embeddings, Y=question_embedding))
        print(f"maximum cosine similarity={cosine_similarity}")
    if index is not None:
        if cosine_similarity > 0.2 and not question.startswith("."):
            print("index present")
            print("question relevant to index")
            answer = index.query(question).response
    else:
        print("index NOT present (or question NOT relevant to index)")
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
