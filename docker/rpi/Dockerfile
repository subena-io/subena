FROM hypriot/rpi-python

## project environment variable
#if you need any env variable please set here
#ENV SUBDB mysql://root:@127.0.0.1:3306/db_subia

#create a repo for project
RUN mkdir -p /opt/subena

RUN apt-get -y update && \
 apt-get -y install mysql-server && \
 apt-get -y install libmysqlclient-dev && \
 service mysql start && \
 apt-get -y install git-core

#for python use
RUN apt-get -y install build-essential python-dev && \
 apt-get -y install python-numpy

#ADD * /opt/subena/

##SOURCES FROM GITHUB
RUN git clone https://github.com/subena-io/subena.git /opt/subena

#add python dependencies for compiling source code
RUN pip install SQLAlchemy
RUN pip install eve
RUN pip install eve-sqlalchemy
RUN pip install MySQL-python

WORKDIR /opt/subena

# 5000 = expose rest service through eve-sqlachemy
EXPOSE 5000

CMD [ "python", "/opt/subena/expose.py" ]
