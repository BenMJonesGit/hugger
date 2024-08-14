# python simple.py modelFolder inputFolder
#   Using modelFolder, run files in inputsFolder through it.

from transformers import pipeline
import sys, os

argc = len(sys.argv)
if argc < 3:
    print("Usage: python simple.py modelFolder inputsFolder")
    exit(0)
    
modelFolder = sys.argv[1]
inputFolder = sys.argv[2]

model = pipeline("summarization", modelFolder, device=-1)

inputNames = os.listdir(inputFolder)
inputNames.sort()

for inputName in inputNames:
    inputPath = os.path.join(inputFolder, inputName)
    if os.path.isfile(inputPath):
        file = open(inputPath)
        input = file.read()
        print(f"Using {inputPath}\n")
        output = model(input, max_length=184, min_length=30, do_sample=False)
        print(output[0]['summary_text']+'\n')
