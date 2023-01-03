FROM node:16
WORKDIR /app
COPY . /app
RUN apt install -y python3 && yarn install && yarn build
EXPOSE 3000
CMD ["yarn", "start"]
