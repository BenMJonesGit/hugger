# question_answering
from transformers import pipeline
import os, json

# Name of the task, which is a grouping within HuggingFace.
task = "question-answering"

# The extension for input files to be processed by the model.
ext = "json"

# The mode for opening input files.  This is "rt" for text files,
# "rb" for binary.
mode = "rt"

# Given a "model_name" (which is usually of the form "folder/subfolder"),
# return object representing the model.
def loadModel(model_name):
    model_path = f"models/{model_name}"
    if not os.path.exists(model_path):
        model_path = model_name       
    return pipeline(task, model=model_path)

# Given the {model} object returned by 'loadModel', process an "input" string (or blob)
# which might be a string or blob, returning the result of that process,
# which is a printable string (or object).
def execModel(model, input):
    q = json.loads(input)
    return model(q)['answer']

# This is an array containing the names of models for this "task".
# The hugger.py module will index into this array to select a model.
models = [
    "deepset/roberta-base-squad2",
    "distilbert/distilbert-base-cased-distilled-squad",
    "deepset/roberta-base-squad2-distilled"
]

# This is an array of descriptors for datasets which can be used with
# this task.  Each element is an object containing the following fields:
#   name - The name of the database on Hugging Face.
#   split - The name of the split to be used.
#   input - The name of the subset of this dataset to be used for input.
#       If it contains names separated by commas, create a json string
#       from those fields.
#   output - The name of the subset of this dataset which is the human answer.
#   take - Number of dataset elements to download (all if not specified).
datasets = [
    {
        "name": "rajpurkar/squad_v2",
        "split": "validation", 
        "input": "question,context", 
    }
]

