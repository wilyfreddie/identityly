import os
import mysql.connector
import numpy as np
import face_recognition as facerecg

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import base64
import json


def numpy_to_json(n_array):
    n_list = n_array.tolist()
    j_array = json.dumps(n_list)
    return j_array


def json_to_numpy(j_data):
    j_array = json.loads(j_data)
    n_array = np.array(j_array)
    return n_array


def main():
    while True:
        # AddFace()
        CheckFace()



def AddToDB(name, face_encoding):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database = "users"
    )

    mycursor = mydb.cursor()

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS ImageDB(
            Person TEXT,
            Face_Encoding JSON
        );
    """)

    mycursor.execute("""
                INSERT INTO ImageDB (Person, Face_Encoding)
                VALUES(%s, %s)""", (name, face_encoding))

    mydb.commit()
    mycursor.close()
    print("User {0} added to the database!".format(name))


def AddFace():
    print("===Add Face===")
    path = input("Enter file path of image: ")
    img = facerecg.load_image_file(path)
    img_enc = facerecg.face_encodings(img)
    print(type(img_enc[0]))
    print(img_enc[0])

    if (len(img_enc) > 0):
        im = Image.open(path)
        im.show()

        name = input("Please enter the name of the individual shown: ")
        face_enc = numpy_to_json(img_enc[0])

        AddToDB(name, face_enc)

    else:
        print("Did not find any face.")


def CheckFace():
    print("===Check Face===")
    path = input("Enter file path of image: ")
    img = facerecg.load_image_file(path)
    img_enc = facerecg.face_encodings(img)

    if (len(img_enc) > 0):
        _img_enc = img_enc[0]
        # print(_img_enc)
        # print(">>>test")
        # connect to existing image.db file
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database = "users"
        )

        mycursor = mydb.cursor()

        # Extract face encoding data from DB
        mycursor.execute("SELECT Face_Encoding FROM ImageDB")
        rows = mycursor.fetchall()
        # Extract names from DB
        mycursor.execute("SELECT Person FROM ImageDB")
        names = mycursor.fetchall()

        found = False
        person = ""
        distance = 1
        for row, name in zip(rows, names):
            name = "".join(name)
            row = b''.join(row)

            row = json_to_numpy(row)

            # comparing both images
            match = facerecg.compare_faces([_img_enc], row, tolerance=0.5)
            face_distance = facerecg.face_distance([_img_enc], row)
            print("{name} - {match} - {face_distance}".format(name=name,
                                                              match=match[0], face_distance=face_distance[0]))
            # print(name)
            # print(match[0])
            if match[0]:
                if face_distance < distance:
                    person = name
                    distance = face_distance
                    found = True

        if found == True:
            print("Face matched with user {person}!".format(person=person))
        else:
            print("No match found.")



if __name__ == "__main__":
    main()
