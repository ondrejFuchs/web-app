## Script for setup and fill DB and web-app script

The file describes the scripts that were created for practical assignment.

### Setup.py

The python script reads the settings for connecting to postgresql DB from OS env. The script creates table __words__ by:

  * ```
    CREATE TABLE IF NOT EXISTS words (id serial PRIMARY KEY, word character varying(255) NOT NULL UNIQUE);
    ```
After that the table is filled with values ​​from the file ```name-list.txt```:

  * ```
    INSERT INTO words(word) VALUES(%s) ON CONFLICT (word) DO NOTHING;
    ```

The file contains the 10 most common Norwegian male and female first names. Script is idempotent with DB operations.

#### Name-list.txt

File contains the 10 most common Norwegian male and 10 most common Norwegian female first name.

### Web-app.py

The python script also reads the settings for connecting to DB from OS env. At startup, it loads the number of rows in the table __words__. Then randomly asks for a word in a given range (__<1 ; db.words_count>__). The script starts __SimpleHTTPRequestHandler__ and return string __Hello <word\_from\_db\_by\_id>__ to every request on path __"/"__.

#### Example response for request:
  * ```Hello Thea```
  * ```Hello Jonas```
  * ```Hello Hanna``` ect.
  
Server runs on port __80__.

### Dockerfile

File for building docker image. Was used __python:3.7-alpine__ docker image from docker hub because of space saving. Dockerfile also setup os env for connect to db.

### Build.sh

Bash script for building docker image from Dockerfile.