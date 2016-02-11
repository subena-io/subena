This page describes all you have to know about this python project
Python version 2.7
Author : Jessy HANZO

#DESCRIPTION
The following project has been developped for bringing a solution to an Internet Of Things (IOT) problematic named SmartIOT.

SmartIOT is an original idea thought by Arnaud PERSIE which wanted to bring intelligency to smart objects. His purpose was to link all of his home sensors with an "aritificial brain" able to deduce use case and triggers automatically actions when something is unexceptable.

But what means unexceptable ? The entire problem is to define in mathematics words how an event can be considered as unexceptable.

For many years, I have wondered how an intelligency can be mathematically programmed. I previously worked on fake website detection (~~see here for more information~~) where purpose was quite the same and I have some elements for answering to this question. My training in engineering school, work experience and personnal researches came me to point Bayesian Network (BN) as the best solution for deducing links between criteria. BN is a complex theory based on a very simple statistic formula : Bayes' Rule P(A|B) = P(B|A)*P(A) / P(B). But behind the scene, there are a lot of other problematics which letting BN usually considered more complex than other theories (decision tree, neuronal networks...). 

Thus, this current project will answer Arnaud's needs and letting everybody to customize it for his own purpose.

#INSTALLATION

##PYTHON VERSION
The following project is running on Python v2.7

##MODULES
Following librairies are required for compiling project
* numpy for using complex mathematics concepts
* pip for project lib dependencies
* SQLAlchemy for managing entities (ORM)
* eve for rest exposition
* eve-sqlalchemy for easily exposing database through eve

###TODO list
* Numba for improving performance

#CONFIGURATION

##CONFIG FILES
* eve-config.py for eve-sqlachemy
* Dockerfile for docker usage

##DATABASE
There is an additional parameter to set in your variable environment named SMARTIO_DB containing the url for logining to the database.
For example : export SMARTIO_DB=mysql://root:@localhost:8888/smartio

##REST SERVICES
For exposing the sqlalchemy database very easily, eve-sqlachemy is used. This lib is based on well known python lib named EVE which letting Rest exposition with MongoDB.
You can configure rest exposition in both file named expose.py (start services) and eve-config.py (config + mapping with database).

For more information, please see official website : http://eve-sqlalchemy.readthedocs.org/en/stable/

##DOCKER
In order to produce an environment very easily, a Dockerfile has been initialized. Docker lets us running an abstract machine containing all you need for compiling the project.

For more information about docker, please see official website : https://www.docker.com/.