FROM python:3
WORKDIR /myapp
RUN mkdir /myapp/tests
ADD tests /myapp/tests
COPY imageSimilarity.py /myapp
COPY monkeymagic.py /myapp
COPY requirements.txt /myapp
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
CMD [ "python3", "/myapp/imageSimilarity.py", "--runServer" ]
