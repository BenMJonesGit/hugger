# Name of the task, which is a grouping within HuggingFace.
task = ""

# The extension for input files to be processed by the model.
ext = ""

# The mode for opening input files.  This is "rt" for text files,
# "rb" for binary.
mode = "rt"

# Given a "model_name" (which is usually of the form "folder/subfolder"),
# return object representing the model.
def loadModel(model_name):
    return {}

# Given the {model} object returned by 'loadModel', process an "input" string (or blob)
# which might be a string or blob, returning the result of that process,
# which is a printable string (or object).
def execModel(model, input):
    return {}

# This is an array containing the names of models for this "task".
# The execute.py module will index into this array to select a model.
models = [ 
    "folder0/subfolder0",
    "folder1/subfolder1",
    "folder2/subfolder2"
]

# This is an array of descriptors for datasets which can be used with
# this task.  Each element is an object containing the following fields:
#   name - The name of the dataset on Hugging Face.
#   split - The name of the split to be used.
#   input - The name of the subset of this dataset to be used for input.
#       If it contains names separated by commas, create a json string
#       from those fields.
#   output - The name of the subset of this dataset which is the human answer.
#   take - Number of dataset elements to download (all if not specified).
datasets = [
    {
        "name": "",
        "split": "", 
        "input": "", 
        "output": ""
    }
]

