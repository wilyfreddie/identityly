import os
import sqlite3
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
        # loadfacedb()
        # facerecog()
        # compare_img()
        # test()
        # AddFace()
        CheckFace()


def AddToDB(name, face_encoding):
    conn = sqlite3.connect("Image.db")
    cur = conn.cursor()

    # create sql table
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS ImageDB(
            Person TEXT,
            Face_Encoding JSON
        );
    """)

    cur.execute("""
                INSERT INTO ImageDB (Person, Face_Encoding)
                VALUES(?, ?)""", (name, face_encoding))

    conn.commit()
    cur.close()
    print("Successfully saved!")


def AddFace():
    print("===Add Face===")
    path = input("Enter file path of image: ")
    img = facerecg.load_image_file(path)
    img_enc = facerecg.face_encodings(img, num_jitters=25)
    print(type(img_enc[0]))
    print(img_enc[0])

    if (len(img_enc) > 0):
        im = Image.open(path)
        im.show()

        name = input("Please enter the name of the individual shown: ")
        face_enc = numpy_to_json(img_enc[0])
        # print(str(face_enc))
        AddToDB(name, face_enc)

    else:
        print("Did not find any face.")


def CheckFace():
    print("===Check Face===")
    path = input("Enter file path of image: ")
    img = facerecg.load_image_file(path)
    img_enc = facerecg.face_encodings(img, num_jitters=50)

    if (len(img_enc) > 0):
        _img_enc = img_enc[0]
        # print(_img_enc)
        # print(">>>test")
        # connect to existing image.db file
        conn = sqlite3.connect("Image.db")
        cur = conn.cursor()

        # Extract face encoding data from DB
        cur.execute("SELECT Face_Encoding FROM ImageDB")
        rows = cur.fetchall()
        # Extract names from DB
        cur.execute("SELECT Person FROM ImageDB")
        names = cur.fetchall()

        found = False
        person = ""
        for row, name in zip(rows, names):
            name = "".join(name)
            row = ''.join(row)

            row = json_to_numpy(row)

            # comparing both images
            match = facerecg.compare_faces([_img_enc], row, tolerance=0.4)
            print(name)
            print(match[0])
            if match[0]:
                print("Matched!")
                person = name
                found = True
                break

        if found == True:
            print("The person is {person}!".format(person=person))
        else:
            print("No match found.")


def loadfacedb():

    # making a sql file
    conn = sqlite3.connect("Image.db")
    # cursor to enter commands in sql
    cur = conn.cursor()

    # create sql table
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS ImageDB(
            Person TEXT,
            Person_Img BLOB,
            Face_Encoding TEXT
        );
    """)

    print("Created SQL file")

    # def to conv image file to binary
    def convert_binary(file):
        with open(file, "rb") as img_read:
            img = img_read.read()
            return img

    print("Label the Images properly")
    # input folder path, checks the folder for .jpg file
    path = input("Folder Path: ")
    print("Scanning for image files")

    for files in os.listdir(path):
        if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".jpeg"):
            print(f"Encoding {files}")
            # extract the name of file
            name = files.split(".")[0]
            # print (name)
            # extract the path of img file
            file_path = os.path.join(path, files)
            # print(file_path)
            # converts img to binary
            img_binary = convert_binary(file_path)
            # print(img_binary)
            # #load the image file
            face = facerecg.load_image_file(file_path)
            # #encoding the image file
            face_encoding = facerecg.face_encodings(face, num_jitters=25)[0]
            # print (type(face_encoding))

            # entering values in SQL
            cur.execute("""
                INSERT INTO ImageDB (Person, Person_Img, Face_Encoding)
                VALUES (?, ?, ?)""", (name, img_binary, face_encoding))

    # writing all the values in DB
    conn.commit()
    cur.close()
    print("Suceffully created Image DB")


def facerecog():

    # connect to existing image.db file
    conn = sqlite3.connect("Image.db")
    cur = conn.cursor()

    # load & encode image
    img_path = input("Enter Image Path to Compare: ")
    img = facerecg.load_image_file(img_path)
    img_enc = facerecg.face_encodings(img, num_jitters=25)[0]

    # Extract face encoding data from DB
    cur.execute("SELECT Face_Encoding FROM ImageDB")
    rows = cur.fetchall()
    # Extract names from DB
    cur.execute("SELECT Person FROM ImageDB")
    names = cur.fetchall()

    # iterate through both name & encoding
    for row, name in zip(rows, names):
        name = "".join(name)
        row = b''.join(row)
        # print (len(row))
        # converting the encoding from DB to numpy array
        db_enc = np.frombuffer(row)
        # print (db_enc)
        # comapiring both images
        match = facerecg.compare_faces([img_enc], db_enc, tolerance=0.5)
        # print (match)
        # 0 referes to true
        if match[0]:
            print(f"Match Found >>> {name}")
            break
        else:
            print("No Match")
    print("PROCESS COMPLETED")


def compare_img():
    known_face_loc = input("Enter file path: ")
    known_face = facerecg.load_image_file(known_face_loc)
    known_face_encoding = facerecg.face_encodings(known_face)[0]

    known_face_encoding = facerecg.face_locations(known_face)

    test_face_loc = input("Enter file path: ")
    test_face = facerecg.load_image_file(test_face_loc)
    test_face_encoding = facerecg.face_encodings(test_face)[0]

    result = facerecg.compare_faces(
        [known_face_encoding], test_face_encoding)

    # True/False
    print(result)


def test():
    # location = "test.jpg"
    # image = facerecg.load_image_file(location)

    # face_locations = facerecg.face_locations(
    #     image, number_of_times_to_upsample=2)

    # print("I found {} face(s) in this photograph.".format(len(face_locations)))

    # for face_location in face_locations:

    #     # Print the location of each face in this image
    #     top, right, bottom, left = face_location
    #     print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(
    #         top, left, bottom, right))

    #     # You can access the actual face itself like this:
    #     face_image = image[top:bottom, left:right]
    #     pil_image = Image.fromarray(face_image)
    #     pil_image.show()

    # known_face_loc = input("Enter file path: ")
    # known_face = facerecg.load_image_file(known_face_loc)
    # known_face_encoding = facerecg.face_encodings(known_face)[0]

    # test_face_loc = input("Enter file path: ")
    # test_face = facerecg.load_image_file(test_face_loc)
    # test_face_encoding = facerecg.face_encodings(test_face)[0]

    # result = facerecg.compare_faces([known_face_encoding], test_face_encoding)
    print("Ralph")
    known_image = facerecg.load_image_file("Ralph_0.jpg")
    unknown_image = facerecg.load_image_file("Ralph_1.jpg")

    _known_image = facerecg.face_encodings(known_image, num_jitters=25)
    _unknown_image = facerecg.face_encodings(
        unknown_image, num_jitters=25)

    print(len(_known_image))
    print(len(_unknown_image))
    biden_encoding = _known_image[0]
    unknown_encoding = _unknown_image[0]

    results = facerecg.compare_faces([biden_encoding], unknown_encoding)

    # True/False
    print(results)


if __name__ == "__main__":
    main()
