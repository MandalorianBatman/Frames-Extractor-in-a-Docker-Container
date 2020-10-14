FROM python:3.8.5

RUN pip install --upgrade pip && \
    pip install --no-cache-dir opencv-python

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y
RUN apt-get update

WORKDIR /usr/src/app

COPY ./frames_extractor.py /usr/src/app
# COPY ./batman-teaser.mp4 /usr/src/app
