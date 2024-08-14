# translation
from transformers import pipeline
from datasets import load_dataset
import os

# Name of the task, which is a grouping within HuggingFace.
task = "translation"

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
    return model(input, max_length=400, min_length=30, do_sample=False, src_lang='en', tgt_lang='fr')

# This is an array containing the names of models for this "task".
# The execute.py module will index into this array to select a model.
models = [
    "Helsinki-NLP/opus-mt-en-fr",
    "Helsinki-NLP/opus-mt-tc-big-en-fr",
    "cartesinus/iva_mt_wslot-m2m100_418M-en-fr"
]

# This is an array of descriptors for datasets which can be used with
# this task.  Each element is an object containing the following fields:
#   name - The name of the database on Hugging Face.
#   split - The name of the split to be used.
#   input - The name of the subset of this dataset to be used for input.
#   output - The name of the subset of this dataset which is the human answer.
#   take - Number of dataset elements to download (all if not specified or 0).
datasets = [
    {
        "name":"EdinburghNLP/xsum",
        "split": "test", 
        "input": "document", 
        "output": "summary"
    },
    {
        "name":"roneneldan/TinyStories", 
        "split": "validation",
        "input": "text",
        "output": "text"
    }
]
