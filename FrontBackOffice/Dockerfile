FROM node:16-alpine3.15 as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install -g npm@latest
RUN npm i
COPY . .
## EXPOSE [Port you mentioned in the vite.config file]
EXPOSE 5174
CMD ["npm", "run", "dev"]