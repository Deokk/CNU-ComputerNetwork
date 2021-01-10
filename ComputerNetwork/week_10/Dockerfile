FROM node:12

MAINTAINER Seongdeok "deokk1112@gmail.com"

WORKDIR /app

COPY package*.json ./

RUN npm install
COPY . /app

EXPOSE 3000
CMD [ "node", "201602011_server.js" ]
