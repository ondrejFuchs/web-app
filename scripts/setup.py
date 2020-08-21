#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import psycopg2

FILE_WORDS = "name-list.txt"
logger = logging.getLogger("Setup_db")


class Setup_db:

    def __init__(self, words, db_cred):
        # Create table in db
        self.create_table(db_cred)
        # OInsert values to table
        self.insert_db_list(words, db_cred)

    def create_table(self, cred: dict) -> None:
        """ Func to create table in db

        Args:
           cred (dist): credentials from postgresql db

        """
        conn = psycopg2.connect(
            host=cred['host'],
            dbname=cred['dbname'],
            password=cred['password'],
            user=cred['user']
        )
        # Query
        sql = "CREATE TABLE IF NOT EXISTS words (id serial PRIMARY KEY, word character varying(255) NOT NULL UNIQUE);"
        
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Problem with creating db words: {}".format(error))
        finally:
            if conn is not None:
                conn.close()

    def insert_db_list(self, words: dict, cred: dict) -> None:
        """ Func to insert multiple value to postgresql db

        Args:
           words (dist): all values of words to insert
           cred (dist): credentials from postgresql db

        """
        conn = psycopg2.connect(
            host=cred['host'],
            dbname=cred['dbname'],
            password=cred['password'],
            user=cred['user']
        )
        # Query
        sql = "INSERT INTO words(word) VALUES(%s) ON CONFLICT (word) DO NOTHING;"
        
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, [[w] for w in words])
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Problem with inserting values to db: {}".format(error))
        finally:
            if conn is not None:
                conn.close()


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')

    # Load all words from file
    words = []
    with open(FILE_WORDS) as f:
        words += [line.rstrip() for line in f]
        
    # Load credentials to postgresql db
    db_cred = {
        'host': os.environ['DB_HOSTNAME'],
        'dbname': os.environ['DB_NAME'],
        'user': os.environ['DB_USERNAME'],
        'password': os.environ['DB_PASSWORD']
    }
    
    # Setup postgresql db
    Setup = Setup_db(words, db_cred)
    logger.info("End setup")
