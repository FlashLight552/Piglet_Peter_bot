FROM python:3.10

WORKDIR /usr/src/piter_bot

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

COPY . .

COPY /cofig/config.py.example /cofig/config.py

CMD [ "python", "main.py" ]