#!/bin/bash

docker run -d --name "yy" -p 5000:5000 -v /home/docker_home/docker_images:/var/lib/registry registry
