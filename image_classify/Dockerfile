# set base image (host OS)
FROM python:3.8

# set the working directory in the container
#WORKDIR ./
RUN apt-get update && apt-get install -y python3-opencv
# copy the dependencies file to the working directory
COPY requirements.txt .
COPY crawl.py .
# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
#COPY src/ .

# command to run on container start
CMD [ "python", "./crawl.py" ]
