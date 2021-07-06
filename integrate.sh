#!/bin/bash
docker build -f Dockerfile -t vcwild/wildoverflow .
docker-compose up -d
