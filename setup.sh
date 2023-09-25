#!/bin/bash
if [ ! -p $PIPE_PATH/exec_in.pipe ]; then
    mkfifo $PIPE_PATH/exec_in.pipe
fi
if [ ! -p $PIPE_PATH/exec_out.pipe ]; then
    mkfifo $PIPE_PATH/exec_out.pipe
fi
while true; do eval "$(cat $PIPE_PATH/exec_in.pipe)" &> $PIPE_PATH/exec_out.pipe; done