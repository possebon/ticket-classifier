# set base image (host OS)
FROM python:3.9.5-slim

ARG DATABASE_HOST
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ENV DATABASE_HOST $DATABASE_HOST
ENV DATABASE_NAME $DATABASE_NAME
ENV DATABASE_USER $DATABASE_USER
ENV DATABASE_PASSWORD $DATABASE_PASSWORD

# set the temporary directory to download additional files
WORKDIR /tmp

RUN apt-get update && apt-get install -y \
  wget \
  lsb-release \
  gnupg \
  python-mysqldb \
  && rm -rf /var/lib/apt/lists/*


    # wget https://dev.mysql.com/get/mysql-apt-config_0.8.17-1_all.deb 
    # dpkg -i "/tmp/mysql-apt-config_0.8.17-1_all.deb" \
    #apt update -y \
    #apt install python-mysqldb -y

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY preprocess.requirements.txt requirements.txt

RUN mkdir /data && mkdir /data/preprocess

# install dependencies
RUN pip install -r requirements.txt

# Additional modules
RUN python -c 'import nltk; nltk.download("mac_morpho")' && python -c 'import nltk; nltk.download("stopwords")' \
  && python -c 'import nltk; nltk.download("punkt")'

# copy the content of the local src directory to the working directory
#COPY ../../src/. .
COPY ["tmp/src/", "/code"]



# command to run on container start
#CMD [ "python", "./server.py" ]
ENTRYPOINT ["tail", "-f", "/dev/null"]
