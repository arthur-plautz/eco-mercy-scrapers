source ../.env

export DRIVER_PATH=/usr/local/bin/$DRIVER

sudo cp ./$DRIVER $DRIVER_PATH

du $DRIVER_PATH