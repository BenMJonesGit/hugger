This project is used for trying out models in HuggingFace.

In the "tasks" folder, there are modules named for different tasks in HuggingFace.
The names of these modules are all lower case with '-' replaced by '_'.

In the tasks folder are modules defining the following variables and functions
(see template.py):

    task
        Name of the task, which is a grouping within HuggingFace.

    ext
        The extension for input files to be processed by the model.
    
    mode
        The mode for opening input files.  This is "rt" for text files, "rb" for binary.
    
    model = loadModel(model_name)
        This function causes a model_name to be loaded into the cache.  The return value
        is an object representing the model.
    
    execModel(model, input)
        Run the input against the model (returned by loadModel).  Depending on the model, the input might be a string of text or json or it might be a blob
        (such as audio or video).

    models = [ "name0", "name1", ... ]
        This array contains the names of models for a given type of "task".  When 
        you look at the Models tab in HuggingFace, these names are shown on the 
        right for a given task selected on the left.  Other processes in this
        project will select a given model by an index into this array.
    
    datasets = [ object0, object1, ... ]
        This array contains objects representing datasets in HuggingFace.  Each
        object contains the following names and values:
            name - The name of the dataset on HuggingFace.
            split - The name of the split to be used when loading the dataset.
            input - The name of the subset of this dataset to be used for input.
                If it contains names separated by commas, create a jason string from
                those fields.
            take - The number of dataset elements to download (all if not specified or 0).

The model is run as follows:

    python hugger.py taskName m1 input11 input12 ... m2 ... repeat n

        Select a model according to "taskName".  The module to be loaded is from "tasks/taskName.py".

        The first parameter after "taskName" is a number indicating the model to be selected first (index into the models array).  If it is a series of numbers
        separated by commas, it indicates that the rest of the parameter list is to be
        repeated for each of the models indicated.  If 'all' is specified, all the the
        models in the 'models' array are to be used.  If numbers are specified as 'x-y',
        models x through y inclusive are indicated.

        After that, a name indicates that "inputs/taskName/name.ext" should be run against the model.  If 'all' is specified, all files in "inputs/taskName"
        are used in alphabetical order.

        A number indicates a different model to be used for subsequent names.

        ds=n:i indicates input(s) to be taken from dataset indicated by datasets[n].
        The 'i' may be a number indicating the element of the dataset to be used.
        If 'i' is a series of numbers separated by commas, those dataset elements
        are to be used in that order.  If a number is specified as 'x-y', elements
        'x' through 'y' inclusive are indicated.  If 'all' is specified, all elements
        are indicated.

        At the end of the parameter list "repeat" indicates that the parameter list
        after "taskName" should be repeated.  If a number is given after "repeat",
        the parameter list should be repeated that many times after the initial
        run.  If no number is given after "repeat", repeat indefintely.

        If no other parameters are given after "taskName", prompt first for the
        model number, then for input.  If a number is specified, select a new
        model.  If "quit" is specified, exit the program.

        If the EXECUTE environment variable is defined as a string with space-
        separated values, it overrides whatever parameters were given after
        the taskName.

        If the TASK environment variable is defined as a taskName, it overrides
        the taskName parameter.

A docker container may be built as follows:

    docker build -t dockerName args .

        The following args may be given:

            --build-arg task=taskName

            --build-arg models="m1 m2 ..."

            --build-arg arguments="m1 name11 name12 ... m2 name21 ... repeat n"

A docker container may be run as follows:

    docker run -it dockerName --name myName
        This automatically runs:
            python hugger.py taskname arguments

        If --name myName is not specified, a name will be assigned to the
        container.  This name may be discovered by running 'docker ps'.

        The -name switch may be used to assign a particular name but if this has
        been done before, it must be removed by saying 'docker rm myName'.

    docker run -it dockerName bash
        Run bash in the docker container.  From here, you may
        execute the above python command but may also inspect
        the folder structure, defaulting to /app.

We can check to see how running a docker container changes its file structure by calling:

    docker diff myName
        where myName is the name specified by --name or assigned automatically.

The following script allows you to compare the current docker diff with a previous one:

    python compare.py myName
        This checks for a file 'cmp/myName.cmp'.  If it does not exist, create it
        from the output of 'docker diff myName'.  If it does exist, output the
        differences between the current run of 'docker diff' to the previously
        stored run.  This way, as the contained called 'myName' runs, you can see
        if anything changes between various phases, such as running the containing
        with no extra arguments which put it into interactive mode.
        
Docker compose sets it up so that 'summary' (specified for dockerName) may be run
in conjunction with a monitoring program.  This is set up by running:
    docker build -t tcpdump --file Dockerfile-tcpdump .

Then you can run them together by calling:
    docker compose up

The only problem with this is it doesn't exit gracefully when the summary service
finishes therefore, say the following:
    source compose.sh
        This will apply the --abort-on-container-exit to the compose.
    EXECUTE="parameters" TASK=taskName source compose.sh
        This will set the EXECUTE environment variable and the TASK environment
        variable to override the parameters to the hugger.py module given
        in the compose.yml file.

Finally, we have the following to do a single model that has already been loaded
into a folder:
    python simple.py modelFolder inputFolder
        Load the model stored in modelFolder and then apply the files in
        inputFolder to the model.  It will print out the name of each input
        file as it is applied.

To build it, we can use Dockerfile-simple.  This proceeds on the assumption that
the model and input folders have been loaded with something.  We also have
compose-simple.yaml to run it and compose-simple.sh to run it so that it
exits gracefully.

