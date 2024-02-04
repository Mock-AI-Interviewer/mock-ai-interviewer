# Stage 1: Build the React application
FROM node:14 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the React application from Nginx
FROM nginx:alpine

# Create .htpasswd file
ARG FRONTEND_PASSWORD
ARG FRONTEND_USERNAME
RUN apk add --no-cache apache2-utils && \
    htpasswd -b -c /etc/nginx/.htpasswd $FRONTEND_USERNAME $FRONTEND_PASSWORD

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
