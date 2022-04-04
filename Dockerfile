FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && apt-get install ffmpeg -y

COPY . .

CMD [ "python", "./main.py" ]