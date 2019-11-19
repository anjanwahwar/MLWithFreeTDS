#Use python as base image
FROM python:3.5-slim

# install FreeTDS
RUN apt-get update
RUN apt-get install unixodbc -y
RUN apt-get install unixodbc-dev -y
RUN apt-get install freetds-dev -y
RUN apt-get install freetds-bin -y
RUN apt-get install tdsodbc -y
RUN apt-get install --reinstall build-essential -y

# populate "ocbdinst.ini"
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

#Use working directory /app
WORKDIR /app

#Copy all the content of current directory to /app
ADD . /app

#Installing required packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Open port 5000
EXPOSE 5000

#Set environment variable
ENV NAME OpentoAll

#Run python program
CMD ["python","app.py"]
