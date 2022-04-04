FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get -y install ffmpeg 

COPY . .

CMD [ "python", "./main.py" ]