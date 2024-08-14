# summarization
from transformers import pipeline
import os

# Name of the task, which is a grouping within HuggingFace.
task = "text2text-generation"

# The extension for input files to be processed by the model.
ext = "txt"

# The mode for opening input files.  This is "rt" for text files,
# "rb" for binary.
mode = "rt"

# Given a "model_name" (which is usually of the form "folder/subfolder"),
# return object representing the model.
def loadModel(model_name):
    model_path = f"models/{model_name}"
    if not os.path.exists(model_path):
        model_path = model_name       
    return pipeline(task, model_path, device=-1)

# Given the {model} object returned by 'loadModel', process an "input" string
# which might be a string or blob, returning the result of that process,
# which is a printable string.
def execModel(model, input):
    return model(input, max_length=200, min_length=30, do_sample=False)[0]['summary_text']+'\n'

# This is an array containing the names of models for this "task".
# The execute.py module will index into this array to select a model.
models = [
    "allenai/PRIMERA"
]