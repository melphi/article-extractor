FROM node:8-alpine

COPY service/ /opt/service
WORKDIR /opt/service
RUN npm install

WORKDIR /opt/service/app
ENTRYPOINT []
CMD ["node", "service.js"]

EXPOSE 5000
	
