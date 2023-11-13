from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
from pathlib import Path
from scipy import spatial
# from flask_cors import CORS

import joblib

app = Flask(__name__)

THIS_FOLDER = Path(__file__).parent.resolve()
my_file = THIS_FOLDER / "treeConditionKNN.pkl"

treeConditionKNN, transformerModel = joblib.load(my_file)
sentenceTransformer = SentenceTransformer(transformerModel)

# CORS(app, resources={r"/*":{"origins":"http://localhost"}})

@app.route("/")
def welcome():
  return jsonify('welcome to the PUA ai api')

@app.route("/get-condition-trees", methods=['POST'])
def conditionTrees():
  treesList = request.get_json()['trees']
  treesMapped = list(map(lambda x: x['sientific_name'], treesList))

  vectorizedTrees = sentenceTransformer.encode(treesMapped)
  predictions = treeConditionKNN.predict(vectorizedTrees)

  returnResults = []

  for index, item in enumerate(predictions):
    returnResults.append({ "condition" : item, "tree": treesList[index]})

  return jsonify({ "data": returnResults })


@app.route("/get-question-suggest", methods=['POST'])
def questionSuggestion():
    sentenceTransformer = SentenceTransformer('all-MiniLM-L6-v2')
    questions = request.get_json()['questions']
    newQuestion = request.get_json()['question']
    closestQuestions = []

    newQuestionVector = sentenceTransformer.encode(newQuestion)
    vectors = sentenceTransformer.encode(questions)

    for i, vector in enumerate(vectors):
        dist = spatial.distance.cosine(newQuestionVector, vector)
        closestQuestions.append((dist, questions[i]))

    # Filtra las preguntas que tienen una distancia menor o igual a 0.5
    filtered_questions = [(dist, question) for dist, question in closestQuestions if dist <= 0.5]

    # Ordena las preguntas filtradas por distancia de menor a mayor
    sorted_questions = sorted(filtered_questions, key=lambda x: x[0])

    # Obtiene las primeras 4 preguntas más cercanas a 0
    result = sorted_questions[:4]

    # Formatea el resultado para devolver solo las preguntas
    result_questions = [question for dist, question in result]

    return jsonify({"data": result_questions})