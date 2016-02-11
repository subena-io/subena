FROM python:2.7

## project environment variable
ENV SMARTIO_DB mysql://root:root@172.27.175.240:4006/smartio

#create a repo for project
RUN mkdir -p /opt/smartio

## manually import file
#add project files to container
#ADD src/* /opt/smartio/

RUN apt-get update && \
 apt-get install mysql-server && \
 service mysql start

##import project from github
RUN git clone https://github.com/jhanzo/smartio.git /opt/smartio

#add python dependencies for compiling source code
RUN pip install numpy && \
 pip install SQLAlchemy && \
 pip install eve && \
 pip install eve-sqlalchemy && \
 pip install MySQL-python

WORKDIR /opt/smartio

##CRONTAB for executing main script every day at 0:00
#ADD crontab /etc/cron.d/smartio-main
#RUN chmod 0644 /etc/cron.d/smartio-main 
#RUN touch /var/log/cron.log
#CMD cron

# 5000 = expose rest service through eve-sqlachemy
EXPOSE 5000

CMD [ "python", "/opt/smartio/expose.py" ]
