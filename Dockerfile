from python:3.6.9

RUN apt-get update
RUN apt-get install vim -y
RUN apt-get install libhunspell-dev -y

WORKDIR /app
COPY . /app

ADD 'https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed' /app/useModel/temp
RUN tar -zxvf /app/useModel/temp -C /app/useModel/
RUN rm -rf /app/useModel/temp
RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 3456

ENTRYPOINT ["python3"]
CMD ["src/app.py"]