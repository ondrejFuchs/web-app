FROM python:3.7

WORKDIR /app
ADD name-list.txt .
ADD setup.py .
ADD web-app.py .

ENV DB_HOSTNAME="localhost" \
    DB_NAME="sixty_db" \
    DB_USERNAME="sixty" \
    DB_PASSWORD="iNousONTumBr"

# Python pycopg2
RUN pip3 install psycopg2

# Create db and insert values and run web-app
CMD python3 setup.py && python3 web-app.py

