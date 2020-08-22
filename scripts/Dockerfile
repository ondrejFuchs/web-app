FROM python:3.7-alpine

RUN apk update && \
    apk add postgresql-dev python3-dev gcc musl-dev

WORKDIR /app
ADD name-list.txt .
ADD setup.py .
ADD web-app.py .

ENV DB_HOSTNAME="sixty.c9pwzjvvfbdr.eu-west-2.rds.amazonaws.com" \
    DB_NAME="sixty_db" \
    DB_USERNAME="sixty" \
    DB_PASSWORD="iNousONTumBr"

# Expose port
EXPOSE 80

# Python pycopg2
RUN pip3 install psycopg2

# Create db and insert values and run web-app
CMD python3 setup.py && python3 web-app.py
