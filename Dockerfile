FROM python:2.7

## project environment variable
#if you need any env variable please set here
#ENV SUBDB mysql://root:@127.0.0.1:3306/db_subia

#create a repo for project
RUN mkdir -p /opt/subena

RUN apt-get update && \
 apt-get install mysql-server && \
 service mysql start

##SOURCES FROM MANUAL
#ADD * /opt/subena/

##SOURCES FROM GITHUB
RUN git clone https://github.com/subena-io/subena.git /opt/subena

#add python dependencies for compiling source code
RUN pip install numpy && \
 pip install SQLAlchemy && \
 pip install eve && \
 pip install eve-sqlalchemy && \
 pip install MySQL-python

WORKDIR /opt/subena

# 5000 = expose rest service through eve-sqlachemy
EXPOSE 5000

CMD [ "python", "/opt/subena/expose.py" ]
