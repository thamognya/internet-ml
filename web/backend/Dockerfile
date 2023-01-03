FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt install -y curl && pip3 install poetry
RUN pip3 install transformers tokenizers datasets contractions torch nltk spacy urlextract internet-ml django djangorestframework
EXPOSE 8080
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
