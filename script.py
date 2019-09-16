from speech_text import recognize_speech_from_mic
import speech_recognition as sr

import psycopg2
from config import config


import psycopg2
from config import config
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def get_customer(name):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        name_like = '%' + name + '%'
        print(name_like)
        cur.execute("""
                    SELECT first_name, last_name, email, phone, address, address2, city, country
                    FROM customer 
                    LEFT JOIN address ON address.address_id = customer.address_id
                    LEFT JOIN city ON city.city_id = address.city_id
                    LEFT JOIN country ON country.country_id = city.country_id
                    WHERE concat(first_name,' ', last_name) ILIKE %s""", (name_like,))
        rows = cur.fetchall()
        print("The number of contact: ", cur.rowcount)
        for row in rows:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == "__main__":
   
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    PROMPT_LIMIT = 3

    print('Say customer\'s name to search:')
    name = recognize_speech_from_mic(recognizer, microphone)
    
    if name["transcription"]:
        print("You said: {}".format(name["transcription"]))
        get_customer(name["transcription"])
    if not name["success"]:
        print("I didn't catch that. What did you say?\n")

    if name["error"]:
        print("ERROR: {}".format(name["error"]))

