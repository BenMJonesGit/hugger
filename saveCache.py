# python saveCache.py taskName n1 n2 n3 ...
#
#   Store models in a local folder by invoke the "tasks/taskName.py" module.
#   Modules are stored by using the "save_pretrained" method.
#
#   The n1, n2, etc. indicate indexes into the models array to cause models to
#   be downloaded into the "models/task" folder.  If not specified, load all the
#   models in the array.

import sys, os

## First argument is the module to process:
argc = len(sys.argv)
if argc < 2 or not os.path.exists(f"tasks/{sys.argv[1]}.py"):
    print(f"Specify the name of a module from 'tasks' folder instead of: {sys.argv[1]}")
    exit(0)
m = __import__(f"tasks.{sys.argv[1]}", fromlist=["models", "loadModel"])
models = m.models
loadModel = m.loadModel

def saveModel(model_name):
    model = loadModel(model_name)
    folders = model_name.split("/")
    folder = folders[0]
    name = folders[1]

    if not os.path.exists("models"):
        os.mkdir("models")
    if not os.path.exists(f"models/{folder}"):
        os.mkdir(f"models/{folder}")
    os.system(f"cp -r -L ~/.cache/huggingface/hub/models--{folder}--{name}/snapshots/* models/{folder}/{name}/")

if argc < 3:
    for m in models:
        saveModel(m)
else:
    for n in range(2, argc):
        saveModel(models[int(sys.argv[n])])
