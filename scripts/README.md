## Script for setup and fill DB and web-app script

The file describes the scripts that were created for Practical assignment.

### Setup.py

The python script reads the settings for connecting to DB from OS env. The database is filled with 20 words from file ```name-list.txt```. The file contains the 10 most common Norwegian male and female first names. Scritp is idempotent with DB operation.

#### Name-list.txt

File contains the 10 most common Norwegian male and 10 most common Norwegian female first name.

### Web-app.py

The python script also reads the settings for connecting to DB from OS env. At startup, it finds the number of rows in the table __words__. Then randomly asks for a word in a given range (__1 - db.words_count__). The script starts __SimpleHTTPRequestHandler__ and return string __Hello <word\_from\_db\_by\_id>__.

Example response for request:
  * ```Hello Thea```
  * ```Hello Jonas```
  * ```Hello Hanna``` ect.
  
Server run on port __80__.

### Dockerfile

File for building docker images. Was used __python:3.7-alpine__ docker image (space saving). Dockerfile also setup os env for connect to db.

### Build.sh

Bash script for building docker image from Dockerfile.