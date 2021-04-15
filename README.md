## Publishing platform

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This is an educational project loosely inspired by https://medium.com/

## Technologies
Project was created with:
* Django
* Javascript

## Setup
To run this project, run following commands

```
$ git clone https://github.com/MindFigment/publishing-platform.git
$ cd publishing-platform
$ docker-compose up -d --build 
```
After that, navigate in web browser to http://localhost:8000/

Default database with some data was prepared
You can create your own account or use one of the following:

username: mindfigment
password mindfigment

username: lisa
password: lisa

username: hania
password: hania

To stop and remove docker containers run

```
$ docker-compose down -v
```
