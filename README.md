This page describes all you have to know about this python project
Python version 2.7
Author : Jessy HANZO

#DESCRIPTION
The following project has been developped for bringing a solution to artificial intelligency problematic.

He has currently running on 2 different projects :
- SmartIOT (bring intelligency to smart objects)
- Fakerz (detect fake websites)

The aim is to detect unexceptable things. But what means unexceptable ? The entire problem is to define in mathematics words how an event can be considered as unexceptable.

For many years, I have wondered how an intelligency can be mathematically programmed. My training in engineering school, work experience and personnal researches came me to point Bayesian Network (BN) as the best solution for deducing links between criteria. BN is a complex theory based on a very simple statistic formula : Bayes' Rule P(A|B) = P(B|A)*P(A) / P(B). But behind the scene, there are a lot of other problematics which letting BN usually considered more complex than other theories (decision tree, neuronal networks...).

#INSTALLATION

##MODULES
The following project is running on Python v2.7

Following librairies are required for compiling project
* numpy for using complex mathematics concepts
* pip for project lib dependencies
* SQLAlchemy for managing entities (ORM)
* eve for rest exposition
* eve-sqlalchemy for easily exposing database through eve

#CONFIGURATION

##CONFIG FILES
* eve-config.py for eve-sqlachemy (rest services)
* [a Dockerfile](https://www.docker.com/) for docker usage (implement an env easily)

##DATABASE
There is an additional parameter to set in your variable environment named SMARTIO_DB containing the url for logining to the database.
For example : export SMARTIO_DB=mysql://root:@localhost:8888/subena

Structure of database is described in scripts/init-schema.sql.
* alerts
* criterion
* dependency
* stats
* value

#TODO list
* Numba for improving performance
* Test integration with other databases