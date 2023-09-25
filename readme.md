export PIPE_PATH=.
chmod +x ./setup.sh
nohup ./setup.sh > /dev/null &
docker build -t telepipe .
docker run -d -v $PIPE_PATH:/hostpipe telepipe
