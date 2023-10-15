from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
from pathlib import Path
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