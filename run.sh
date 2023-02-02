#!/bin/bash


function check_virtual_env(){
	if [ -z "$VIRTUAL_ENV" ]; then
		source venv/bin/activate
		python3 osint.py
	else
		python3 osint.py
	fi
}	


function start_script(){
	if ! [ -d "venv" ]; then
		python3 -m venv venv && source venv/bin/activate
		pip install -r requirements.txt
		python3 osint.py
	else
		check_virtual_env
	fi
}

start_script