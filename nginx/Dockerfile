FROM nginx:1.25.4
RUN mkdir /app
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
WORKDIR /app