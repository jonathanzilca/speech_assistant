import datetime
import os
import numpy as np
import cv2
import face_recognition  # install cmake, dilib 19.18.0 by this order using terminal
from conversation import robot_say, take_command, robot_name
# for creating an id card
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import sqlite3


def faceRecognizerCalculator():
    path = "../Speech_Assistent-0.0.0/imagesAttendance"
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    # print(classNames)

    def findEncoding(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncoding(images)
    print("Encoding complete")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    curName = ""
    name = "  "

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        for encodeFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            face_accuracy = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(face_accuracy)

            if matches[matchIndex]:
                name = classNames[matchIndex]
                x1, y1, x2, y2 = faceLocation
                x1, y1, x2, y2 = x1 * 4, y1 * 4, x2 * 4, y2 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)  # to create a square around the face
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)  # place to write the name
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)  # writing the name
                the_most_right_match = min(face_accuracy)
                if the_most_right_match > 0.55:
                    name = "Unknown"
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

            if curName is not name:
                curName = name
            if curName == name:
                return name


def createIDCard():
    searched_person_name = "Daniel Zilca"

    # Set the ID card size and background color
    width = 10000
    height = int(width / 1.65)
    font_size = int(width / 25)
    x_space_object = int(width / 90)
    y_space_object = int(height / 50)
    space_between_objects = int(height / 8)
    photo_size = int(width / 3.5)
    color = (255, 255, 255)

    # Connect to the database
    conn = sqlite3.connect("peopleInfo.db")

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Select a single row from the table
    cursor.execute("SELECT * FROM people WHERE name = '" + searched_person_name + "'")

    # Fetch the row
    row = cursor.fetchone()

    # all person's data
    person_photo = row[0]
    person_name = row[1]
    person_date_of_birth = row[2]
    person_age = row[3]
    person_phone = row[4]
    person_gmail = row[5]
    person_address = row[6]
    person_education = row[7]
    person_job = row[8]

    # Close the connection to the database
    conn.close()

    # Create an empty image with the specified size and color
    id_card = Image.new("RGB", (width, height), color)

    # Load the photo
    background = Image.open("D:\\program shit\\background.png")
    photo = Image.open(person_photo)

    # Resize the photo to fit on the ID card
    background = background.resize((width, height))
    photo = photo.resize((photo_size, photo_size))

    # Create a mask image with a circular shape
    mask = Image.new("L", photo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, photo.width, photo.height), fill=255)

    # Apply the mask to the photo
    photo.putalpha(mask)

    # Paste the photo onto the ID card
    id_card.paste(background, (0, 0))
    id_card.paste(photo, (int(x_space_object * 1.5), int(y_space_object * 1.5)), mask)

    # Create a drawing context
    draw = ImageDraw.Draw(id_card)

    # Load a font

    font = ImageFont.truetype("david.ttf", font_size)

    # Add the person's name to the ID card
    name = "Name:" + person_name
    x, y = photo_size + x_space_object * 2.5, y_space_object
    draw.text((x, y), name, font=font, fill=(0, 0, 0))

    # Add the person's age to the ID card
    date_of_birth = "Date of birth:" + str(person_date_of_birth)
    x, y = photo_size + x_space_object * 2.5, y_space_object + space_between_objects
    draw.text((x, y), date_of_birth, font=font, fill=(0, 0, 0))

    # Add the person's age to the ID card
    age = "Age:" + str(person_age)
    x, y = photo_size + x_space_object * 2.5, y_space_object + space_between_objects * 2
    draw.text((x, y), str(age), font=font, fill=(0, 0, 0))

    # Add the person's address to the ID card
    phone_number = "Phone number:" + person_phone
    x, y = photo_size + x_space_object * 2.5, y_space_object + space_between_objects * 3
    draw.text((x, y), phone_number, font=font, fill=(0, 0, 0))

    # Add the person's address to the ID card
    gmail = "Gmail:" + person_gmail
    x, y = x_space_object, y_space_object + space_between_objects * 4
    draw.text((x, y), gmail, font=font, fill=(0, 0, 0))

    # Add the person's address to the ID card
    address = "Address:" + person_address
    x, y = x_space_object, y_space_object + space_between_objects * 5
    draw.text((x, y), address, font=font, fill=(0, 0, 0))

    # Add the person's address to the ID card
    education = "Education:" + person_education
    x, y = x_space_object, y_space_object + space_between_objects * 6
    draw.text((x, y), education, font=font, fill=(0, 0, 0))

    # Add the person's address to the ID card
    occupation = "Occupation:" + person_job
    x, y = x_space_object, y_space_object + space_between_objects * 7
    draw.text((x, y), occupation, font=font, fill=(0, 0, 0))

    # Save the ID card to a file
    plt.imshow(id_card)
    plt.show()


def faceRecognition():
    year = int(datetime.datetime.now().year)

    robot_say("Recognizing...")
    recognized_name = faceRecognizerCalculator()

    if "Jonathan" == recognized_name:
        robot_say("hey master")
        robot_say("your name is Jonathan Zilca and are " + str(year - 2002) + " years old.")
        robot_say("These days you work as a soldier.")

    if "Lia" == recognized_name:
        robot_say("Her name is Lia Zilca and she is " + str(year - 1961) + " years old.")
        robot_say("These days she works as a nurse in the Asaf Haroffe hospital.")

    if "Roni" == recognized_name:
        robot_say("His name is Roni Zilca and he is " + str(year - 1962) + " years old.")
        robot_say("These days he works as a lawyer.")

    if "Daniel" == recognized_name:
        robot_say("His name is Daniel Zilca and he is " + str(year - 1992) + " years old.")
        robot_say("These days he works as a programmer.")

    if "Michal" == recognized_name:
        robot_say("Her name is Micheal Zilca and she is " + str(year - 1999) + " years old.")
        robot_say("These days she works as a artist.")

    if "Alon" == recognized_name:
        robot_say("His name is Alon dalach and he is " + str(year - 2002) + " years old.")
        robot_say("These days she works as a soldier.")

    if "Banov" == recognized_name:
        robot_say("His name is Daniel Banovski and he is " + str(year - 2002) + " years old.")
        robot_say("These days he is a student in the Technion University.")

    if "Bremer" == recognized_name:
        robot_say("Her name is Adi Bremer and she is " + str(year - 2002) + " years old.")
        robot_say("These days she works as a soldier.")

    if "Dolev" == recognized_name:
        robot_say("His name is Dolev fishman and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Elad" == recognized_name:
        robot_say("His name is Elad Mani and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Idan" == recognized_name:
        robot_say("His name is Idan Pogrevinski and he is " + str(year - 2002) + " years old.")
        robot_say("These days he is a soldier-student in the Technion University.")

    if "Ilan" == recognized_name:
        robot_say("His name is Ilan Gimelferb and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Lior" == recognized_name:
        robot_say("His name is Lior Raphael and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Maya" == recognized_name:
        robot_say("Her name is Maya Gaver and she is " + str(year - 2002) + " years old.")
        robot_say("These days she learns UI UX.")

    if "Ori" == recognized_name:
        robot_say("His name is Ori Anvar and he is " + str(year - 2002) + " years old.")
        robot_say("These days he is a soldier-student in the Technion University.")

    if "Zelig" == recognized_name:
        robot_say("His name is Daniel Zelig and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Unknown" == recognized_name:
        robot_say("Sorry Sir, but this person does not appear in my database.")
