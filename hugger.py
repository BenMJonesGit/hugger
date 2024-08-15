# python hugger.py taskName m1 name11 name21 m2 name21 name22 ... repeat n
#
#   Select a model according to "taskName".  The module to be loaded is from "tasks/taskName.py".
#
#   The first parameter after "taskName" is a number indicating the model to be selected first.
#
#   After that, a name indicates that "inputs/taskName/name.ext" should be run against the model.
#
#   A number indicates a different model to be used for subsequent names.
#
#   At the end of the parameter list "repeat" indicates that the parameter list after "taskName"
#   should be repeated.  If a number is given after "repeat", the parameter list should be repeated
#   that many times after the initial run.  If no number is given after "repeat", repeat indefintely.
#
#   If TASK environment variable is defined use it instead of the taskName argument.
#
#   If EXECUTE environment variable is defined, split it with space to get the arguments to use
#   rather than the ones specified after taskName
#
#   If there are no other arguments either given or specified by EXECUTE, prompt for the model number
#   then for inputs.  Continue prompting until "quit" is given.
#
#   If the first parameter after taskName is a series of numbers separated by commas, apply the
#   inputs which follow to each of the model numbers indicates.  If 'all' is specified, run through
#   all the models listed in the task.
#
#   If the second parameter after taskName is 'all', run through each of the inputs in the
#   inputs/taskName folder, in alphabetic order.
#
#   At the end of a run, ask the operator to identify the model number that works best.

import sys, os, json
from datasets import load_dataset

# Return an array of numbers from 'text', which may be a numeric string
# a set of numeric strings separated by commas, which may include ranges
# indicated by lowNumber-highNumber, inclusive.  Give error if any of
# these are >= 'length'.  If 'all' is specified, do the entire range.
def sequence(text, length):
    numbers = []
    sNumbers = text.split(',')
    for n in sNumbers:
        if n.find('-') >= 0:
            low, high = n.split('-')
            if not low.isnumeric():
                print(f"Non-numeric: {low} in sequence: {text}")
                break
            if not high.isnumeric():
                print(f"Non-numeric: {high} in sequence: {text}")
                break
            rNumbers = []
            for r in range(int(low), int(high)+1):
                if r < length:
                    rNumbers.append(r)
                else:
                    print(f"Number {r} >= length {length} in sequence: {text}")
                    breakpoint
            numbers += rNumbers
        elif n.isnumeric():
            n = int(n)
            if n < length:
                numbers.append(int(n))
            else:
                print(f"Number {n} >= length {length} in sequence: {text}")
                break
        elif n == 'all':
            for r in range(0, length):
                numbers.append(r)
        else:
            print(f"Non-numeric: {n} in sequence: {text}")
            break
    return numbers

def execute(name):
    global model
    try:
        if type(name) is str and os.path.exists(name):
            file = open(name, mode)
            input = file.read()
            if mode ==  "rt":
                print(f"\nINPUT: {name}: {input}\n")
            else:
                print(f"\nINPUT: {name}\n")
            print(f"\nOUTPUT: {execModel(model, input)}\n")
        else:
            print(f"\nOUTPUT: {execModel(model, name)}\n")
    except Exception as ex:
        print(ex)

def setModel(n):
    global model
    if n >= len(models):
        n = 0
    print(f"\nMODEL[{n}]: {models[n]}\n")
    model = loadModel(models[n])

def setDataset(n):
    global dataset
    global dataset_split
    global dataset_input
    global dataset_output
    
    if n >= len(datasets):
        print(f"Dataset number {n} >= length {len(datasets)}")
        n = 0
    dataset_split = datasets[n]['split']
    dataset_input = datasets[n]['input']
    print(f"\nDATASET[{n}]: {datasets[n]['name']}\n")
    
    if 'take' in datasets[n].keys() and datasets[n]['take'] != 0:
        dataset = list(load_dataset(datasets[n]['name'], split=dataset_split, streaming=True).take(datasets[n]['take']))
    else:
        dataset = load_dataset(datasets[n]['name'], split=dataset_split)
        
if __name__ == "__main__":
     
    # First argument is the module to process:
    argc = len(sys.argv)
    if argc >= 2:
        module = sys.argv[1]
    else:
        module = "summarization"
    module = os.getenv("TASK", default=module)
    if not os.path.exists(f"tasks/{module}.py"):
        print(f"Specify the name of a module from 'tasks' folder instead of: {module}")
        exit(0)

    m = __import__(f"tasks.{module}", fromlist=["task", "models", "ext", "mode", "loadModel", "execModel", "datasets"])
    task = m.task
    models = m.models
    ext = m.ext
    mode = m.mode
    loadModel = m.loadModel
    execModel = m.execModel
    datasets = m.datasets

    arguments = os.getenv("EXECUTE", default="")
    if arguments != "":
        argv = arguments.split(" ")
    else:
        argv = sys.argv[2:]
    argn = len(argv)

    if argn == 0:
        n = int(input("Model: "))
        setModel(n)
        while True:
            name = input("Input: ")
            if name == 'quit':
                break
            elif name == '':
                continue
            elif name.isdigit():
                setModel(int(name))
            else:
                execute(f"inputs/{module}/{name}.{ext}")
    else:
        repeat = -1
        m = -1
        numbers = []
        while repeat != 0 or (m >= 0 and m < len(numbers)):
            if m < 0:
                repeat -= 1
            for i in range(0, argn):
                name = argv[i]
                if name.isnumeric():
                    if m < 0:
                        setModel(int(name))
                    elif m < len(numbers):
                        setModel(numbers[m])
                        m += 1
                    else:
                        break
                elif name.startswith("ds="):
                    ds_n, ds_is = name[3:].split(':')
                    setDataset(int(ds_n))
                    sets = sequence(ds_is, len(dataset))
                    for n in sets:
                        input = dataset[n]
                        if dataset_input.find(",") < 0:
                            input = input[dataset_input]
                        else:
                            item1, item2 = dataset_input.split(",")
                            items = {}
                            items[item1] = input[item1]
                            items[item2] = input[item2]
                            input = json.dumps(items)
                        print(f"\nINPUT[{n}]: {input}\n")
                        execute(input)
                elif name.find(',') >= 0 or name.find('-') >= 0:
                    if m < 0:
                        numbers = sequence(name, len(models))
                        m = 0
                    elif m == len(numbers):
                        break
                    setModel(numbers[m])
                    m += 1
                elif name == 'all':
                    if i == 0:  # All models
                        if m < 0:
                            numbers = [ 0 ]
                            for j in range(1, len(models)):
                                numbers += [ j ]
                            m = 0
                        elif m == len(numbers):
                            break
                        setModel(numbers[m])
                        m += 1
                    else:       # All inputs
                        inputNames = os.listdir(f"inputs/{module}")
                        inputNames.sort()
                        for inputName in inputNames:
                            execute(f"inputs/{module}/{inputName}")
                elif name != 'repeat':
                    execute(f"inputs/{module}/{name}.{ext}")
                elif m < 0 or m == len(numbers):
                    m = -1
                    if i == argn - 2:
                        if repeat < 0:
                            repeat = int(argv[i+1])
                        break
                    else:
                        break
                else:
                    break
            else:
                if m < 0 or m == len(numbers):
                    break
