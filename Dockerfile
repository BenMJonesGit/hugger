# Create a docker image containing HuggingFace models.

FROM python:latest

# Define arguments to be set by --build-arg switches:

# This references modules in the "tasks" folder.  This will 
# indicate what models to build and what processes to run for
# those models.
ARG task=summarization

# The "models" array in a given "task" module calls out the name
# of models asssociated with a particular task.  This variable is
# a string containing indexes in the "models" array to indicate
# which ones to load into the docker image.  If this string is
# empty all of the models named will be loaded.
ARG models="0 2 6"

# This indicates which type of save we want to do (saveModels or
# savePretrained):
ARG save="savePretrained"

# This string indicates what arguments are given to the hugger.py
# module to select models and run test files:
#    n - An index into the models array indicating which model to operate on.
#    name - The name of an input file in the "inputs/taskname" folder.
#    repeat r - Indicates the number of times to repeat this list.
#
ARG arguments=""

# FROM ubuntu:latest
# RUN apt update

# This module is needed by "automatic_speech_recognition":
# RUN apt install ffmpeg -y


# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy necessary files:
COPY *.py .
COPY tasks/. tasks/.
COPY inputs/. inputs/.

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to "requirements.txt" to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Download model using "saveModels" variable:  
RUN python $save.py $task $models
COPY models/. models/.

# Switch to the non-privileged user to run the application.
# USER appuser

# Run the application.
ENV TASK="$task"
ENV ARGUMENTS=$arguments
CMD [ "sh", "-c", "python hugger.py ${TASK} $ARGUMENTS" ]
