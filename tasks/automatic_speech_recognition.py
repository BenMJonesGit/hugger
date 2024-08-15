# automatic_speech_recognition
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

import os

# Name of the task, which is a grouping within HuggingFace.
task = "automatic-speech-recognition"

# The extension for input files to be processed by the model.
ext = "flac"

# The mode for opening input files.  This is "rt" for text files,
# "rb" for binary.
mode = "rb"

# Given a "model_name" (which is usually of the form "folder/subfolder"),
# return object representing the model.
def loadModel(model_name):
    model_path = f"models/{model_name}"
    if not os.path.exists(model_path):
        model_path = model_name    
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device
    )
   
    return pipe

# Given the {model} object returned by 'loadModel', process an "input" string (or blob)
# which might be a string or blob, returning the result of that process,
# which is a printable string (or object).
def execModel(model, input):
    if type(input) is not str and type(input) is not bytes:
        input = input.copy()
    return model(input)['text']+'\n'

# This is an array containing the names of models for this "task".
# The hugger.py module will index into this array to select a model.
models = [
    "openai/whisper-large-v2",
    "openai/whisper-large-v3",
    "openai/whisper-medium",
    "openai/whisper-small"
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
        "name": "MLCommons/peoples_speech",
        "split": "test", 
        "input": "audio",
        "take": 100
    }
]
