FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt update && apt install -y curl python3-pip 
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - 
RUN apt install -y nodejs && npm install --global yarn
RUN pip3 install transformers tokenizers datasets contractions torch nltk spacy urlextract internet-ml django djangorestframework
RUN cd /app/frontend/ && yarn install
RUN cd ../ && npm i -g concurrently
CMD [ "./run.sh" ]
EXPOSE 3000:3000
