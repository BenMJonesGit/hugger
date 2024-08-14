# python copyCache folder/name
#   Copy from ~/.cache/huggingface/hub/models--folder--name/snapshot/* to models/folder/name

import sys, os

if len(sys.argv) < 2:
    exit(0)

folders = sys.argv[1].split("/")
folder = folders[0]
name = folders[1]

if not os.path.exists("models"):
    os.mkdir("models")
if not os.path.exists(f"models/{folder}"):
    os.mkdir(f"models/{folder}")
os.system(f"cp -r -L ~/.cache/huggingface/hub/models--{folder}--{name}/snapshots/* models/{folder}/{name}/")

