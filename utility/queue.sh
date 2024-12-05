#!/usr/bin/bash


for((i=0;i<10;i++));
do
    echo "${i}"
    curl -X POST http://127.0.0.1:5000/produce -H "Content-Type: application/json" -d '{ "message": "HOLA SOY EL $i !!!!!"}'
done
