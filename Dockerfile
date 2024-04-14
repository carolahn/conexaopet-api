# pull official base image
FROM python:3.12.1

# set work directory
WORKDIR /srv/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV DB_ENGINE=${DB_ENGINE}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD} 

# debug: print package sources
RUN apt-cache policy

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev

# install python dependencies
COPY requirements.txt /srv/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# start server
CMD [ "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:5000" ]