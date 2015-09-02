#!/bin/bash

APP_NAME=$1
APP_DIR="$(dirname $0)/.."
PID_FILE="/var/run/esthenos/${APP_NAME}.pid"
LOG_FILE="/var/log/esthenos/${APP_NAME}.log"


if [[ ! -z $APP_NAME ]]; then
    echo "esthenos app : ${APP_NAME}"
else
    echo "esthenos app not specified."
    exit 1;
fi

case $APP_NAME in
    esthenos-beats)
	echo "starting up esthenos-beats in ${APP_DIR}."
	cd ${APP_DIR}
	nohup celery beat -A esthenos.tasks -l DEBUG --logfile $LOG_FILE 2>&1 &
	echo $! > $PID_FILE
	;;

    esthenos-celery)
	echo "starting up esthenos-celery in ${APP_DIR}."
	cd ${APP_DIR}
	nohup celery worker -A esthenos.tasks -l DEBUG --logfile $LOG_FILE 2>&1 &
	echo $! > $PID_FILE
	;;

    esthenos-webapp)
	echo "starting up esthenos-webapp in ${APP_DIR}."
	cd ${APP_DIR}
	nohup python manage.py rungunicorn > $LOG_FILE 2>&1 &
	echo $! > $PID_FILE
	;;

    *)
	echo "uknown option specified."
	exit 1;
	;;
esac
