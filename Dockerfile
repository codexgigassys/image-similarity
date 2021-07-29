FROM python:3
WORKDIR /image-similarity
RUN mkdir /image-similarity/tests
ADD tests /image-similarity/tests
COPY imageSimilarity.py /image-similarity
COPY monkeymagic.py /image-similarity
COPY requirements.txt /image-similarity
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
CMD [ "python3", "/image-similarity/imageSimilarity.py", "--runServer", "--logging" ]
