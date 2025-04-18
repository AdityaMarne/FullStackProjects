FROM node:20

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install
RUN npm install axios react-router-dom
RUN npm install @react-oauth/google

copy . .

EXPOSE 3000

CMD ["npm", "start"]

