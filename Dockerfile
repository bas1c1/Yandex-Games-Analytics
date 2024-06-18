FROM ubuntu:22.04

ENV TZ="Europe/Moscow"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
RUN mkdir /app/templates
RUN mkdir /app/static
COPY main.py /app
COPY templates /app/templates
COPY static /app/static
COPY requirements.txt /app

RUN apt update
RUN apt install software-properties-common --yes

RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
RUN apt update && apt install python3 python3-pip --yes

RUN python3 -m pip install --upgrade pip
RUN python3 --version
RUN python3 -m pip install -r requirements.txt --ignore-installed

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

ENTRYPOINT ["python3", "main.py"]