docker build -t hugger --build-arg task=summarization --build-arg models="0 2 6" --build-arg arguments="0 input0 input1 input2 input3 input4 repeat 1" .
docker build -t monitor --file Dockerfile-monitor .
