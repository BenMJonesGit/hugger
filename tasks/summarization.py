# summarization
from transformers import pipeline
from datasets import load_dataset
import os

# Name of the task, which is a grouping within HuggingFace.
task = "summarization"

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
    return pipeline(task, model_path)

# Given the {model} object returned by 'loadModel', process an "input" string
# which might be a string or blob, returning the result of that process,
# which is a printable string.
def execModel(model, input):
    return model(input, max_length=200, min_length=30, do_sample=False)[0]['summary_text']+'\n'

# This is an array containing the names of models for this "task".
# The hugger.py module will index into this array to select a model.
models = [
    "facebook/bart-large-cnn",
    "sshleifer/distilbart-xsum-12-1",
    "google/pegasus-multi_news",
    "knkarthick/MEETING_SUMMARY",
    "philschmid/bart-large-cnn-samsum",
     
    "slauw87/bart_summarisation",
    "mukayese/transformer-turkish-summarization",
    "yihsuan/mt5_chinese_small",
    "recogna-nlp/ptt5-base-summ-xlsum",
    "pszemraj/long-t5-tglobal-base-sci-simplify-elife",

    "transformer3/H2-keywordextractor",
    "madushakv/t5_xsum_samsum_billsum_cnn_dailymail",
    "ArtifactAI/phi-arxiv-math-instruct",
    "nsi319/legal-led-base-16384",
    "transformer3/H2-keywordextractor",

    "Shahm/bart-german",
    "cointegrated/rut5-base-absum",
    "human-centered-summarization/financial-summarization-pegasus",
    "csebuetnlp/mT5_multilingual_XLSum",
    "google/pegasus-xsum",

    "csebuetnlp/mT5_multilingual_XLSum"
]

# This is an array of descriptors for datasets which can be used with
# this task.  Each element is an object containing the following fields:
#   name - The name of the database on Hugging Face.
#   split - The name of the split to be used.
#   input - The name of the subset of this dataset to be used for input.
#   take - Number of dataset elements to download (all if not specified or 0).
datasets = [
    {
        "name":"EdinburghNLP/xsum",
        "split": "test", 
        "input": "document"
    },
    {
        "name":"roneneldan/TinyStories", 
        "split": "validation",
        "input": "text"
    }
]
