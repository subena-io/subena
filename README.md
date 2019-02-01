Subena Artificial Intelligence
===

The following project has been developped for bringing a solution to **artificial intelligency** problematic.

It is currently running on 2 different projects :
> SmartIOT - Intelligency in smart objects

> Fakerz - Fake websites detection

The aim is to detect *unexceptable* things. The whole problem is to define in mathematics words how an event can be considered as *unexceptable*.

## Quick overview

![alt](https://github.com/subena-io/resources/blob/master/images/overview.png)

## Requirements

### Docker
[optional] [Dockerfile](https://www.docker.com/) in base project can be used in order to facilitate environment installation.

Docker-compose can be used for having multiple container instances (1 Db container / 2 python container) thanks to docker-compose.yml.dist.

Please note two files are available in 'docker' folder according to your server 
- `rpi/Dockerfile` Raspberry Debian OS configured thanks to Hypriot team [See Hypriot Blog](http://blog.hypriot.com/)
- `std/Dockerfile` Standard configuration (Linux, Mac OS, Windows)

### Python package
Project is running on Python v2.7

Following librairies are required for compiling project
* **PIP** for project lib dependencies [doc here](https://pypi.python.org/pypi/pip)
* **Numpy** for using complex mathematics concepts [doc here](http://www.numpy.org/)
* **SQLAlchemy** for managing entities (ORM) [doc here](http://www.sqlalchemy.org/)
* **EVE-SQLAlchemy** for easily exposing database through Rest services [doc here](http://eve-sqlalchemy.readthedocs.org/en/stable/)

## Architecture

The architecture is based on easy concepts :

>**Subena IA** has to detect `unexceptable` events according to calculated stats.

>An event at timestamp T contains N values where N is the number of criteria.
>>Criterion << 1 : N >> Value

>Criteria can be grouped by families. 
>>Criterion << N : 1 >> Family

>Criteria can be linked with each other.
>>Criterion << N : N >> Criterion
 
Thus, used database `sub_ia` is :

![alt](https://github.com/subena-io/resources/blob/master/images/db_model.png)

| Tables       | Description
|--------------|----------------------------------------------------
| `alerts`     | Unexceptable events are stored here
| `criterion`  | Algorithm is based on evaluating values of these
| `dependency` | Algorithm calculates dependencies between criteria
| `family `    | Criteria can be grouped by family (calculation are not impacted)
| `settings`   | Contains any additional parameters
| `stats`      | Algorithm calculated relevant correlation between sensors and store value here
| `value`      | Values for criteria. One line equals to one value for one criterion at a given timestamp

## Configuration
Thanks to **SQLAlchemy**, every kind of database should be supported but only MySQL has been effectively used and tested for now.

An init MySQL script can be found at the following path `scripts/init-schema.sql`

An example of database with data can be found at `scripts/example.sql`. In this example, values are get from 8 criteria corresponding to 8 sensors.

## Project
Hearth of algorithm is contained in `package` folder.

`alerts` folder contains methods for storing `unexceptable` events 
`learning` parameter and structure learning algorithm
`model` defines classes linked with database

For launching project just execute main script :
>python scripts/main.py -v

## Credits
Author : Jessy HANZO
