#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import http.server
import socketserver
import random
import psycopg2
import logging
from http import HTTPStatus

logger = logging.getLogger("Setup_db")


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        """ Func to manage every GET request to server

        """
        # Manage only request to "/"
        if self.path == '/':
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            # Get random int from range of all words
            word_id = random.randint(1, db.words_count)
            # Get word from db by id
            word = db.get_word_by_id(db_cred, word_id)
            # Format and print output
            output = "Hello {}".format(word)
            self.wfile.write(output.encode('utf-8'))
            # Log output also to console
            logger.info(output)
        
        # Set healthcheck endpoint    
        elif self.path == '/healthcheck':
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            pass
        

    def log_message(self, format, *args):
        """ Func to mute request info console

        """
        return


class read_db():

    words_count = None

    def __init__(self, db_cred: dict):

        # Get count of all words
        read_db.words_count = self.get_row_count(db_cred)

    def get_row_count(self, cred: dict) -> int:
        """ Func to get count of all rows in table words

        Args:
           cred (dist): credentials from postgresql db

        Returns:
           int: count of all rows from table words

        """
        conn = psycopg2.connect(
            host=cred['host'],
            dbname=cred['dbname'],
            password=cred['password'],
            user=cred['user']
        )
        # Query
        sql = "SELECT COUNT(*) FROM words"

        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Problem with creating db words: {}".format(error))
        finally:
            if conn is not None:
                conn.close()

        return result[0]

    @staticmethod
    def get_word_by_id(cred: dict, id: int) -> str:
        """ Func to get specific word from db by id

        Args:
           cred (dist): credentials from postgresql db
           if (int): if value from db to get word

        Returns:
           str: one word from db by id

        """

        conn = psycopg2.connect(
            host=cred['host'],
            dbname=cred['dbname'],
            password=cred['password'],
            user=cred['user']
        )
        # Query
        sql = "SELECT word FROM words where id = %s;"

        cursor = conn.cursor()
        try:
            cursor.execute(sql, [id])
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Problem with creating db words: {}".format(error))
        finally:
            if conn is not None:
                conn.close()

        return result[0]


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')

    # Load credentials to postgresql db
    db_cred = {
        'host': os.environ['DB_HOSTNAME'],
        'dbname': os.environ['DB_NAME'],
        'user': os.environ['DB_USERNAME'],
        'password': os.environ['DB_PASSWORD']
    }

    # Read data from db
    db = read_db(db_cred)
    logger.info("Counted all {} rows from db".format(db.words_count))
    
    # App web address
    server_address = ('', 80)

    logger.info("Web app will start on address {}".format(server_address))
    # Setup server and run
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(server_address, Handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('^C received, shutting down the server.')
        httpd.socket.close()
