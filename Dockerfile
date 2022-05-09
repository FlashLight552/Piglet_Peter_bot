FROM python:3.10.4

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

RUN python3 -m venv ./venv
COPY requirements.txt ./

RUN . /venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]