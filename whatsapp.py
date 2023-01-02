import datetime
import difflib
import subprocess
from conversation import robot_say, take_command
import pywhatkit as k  # in order to send a whatsapp message


def open_whatsapp():
    subprocess.Popen(["C:\\Users\\yonat\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])


def send_massage():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    seconds = int(datetime.datetime.now().second)
    if 40 <= seconds < 60:
        minute = minute + 2
    else:
        minute = minute + 1
    robot_say("To who would you like to message?")
    my_contact = {
        # ###########family#################
        # me:
        "to me": '+972503345739',
        "to myself": '+972503345739',
        "me": '+972503345739',
        "myself": '+972503345739',
        "self": '+9725033'
                '45739',
        # mother:
        "mom": "+972537345739",
        "mother": "+972537345739",
        "emma": "+972537345739",
        "lia": "+972537345739",
        # father:
        "roni": "+972522744248",
        "abba": "+972522744248",
        "papa": "+972522744248",
        # shira:
        "shira": "+972523507576",
        "she-ra": "+972523507576",
        # dani:
        "daniel": '+972523218086',
        "loser": '+972523218086',
        "efes": '+972523218086',
        "dani": '+972523218086',
        "doona": '+972523218086',
        # micheal:
        "mishael": "+972524797269",
        "mishel": "+972524797269",
        "michel": "+972524797269",
        "michael": "+972524797269",
        # magal:
        "magal": "+972526003830",
        "miguel": "+972526003830",
        # ###########family#################

        # ###########friends#################
        # banov:
        "banov": "+972546156775",
        # idan:
        "beta": "+972586245315",
        "idan": "+972586245315",
        # dolev:
        "dolev": "+972506791105",
        # ori:
        "ori": "+972548015343",
        # alon:
        "alon": "+972587312954",
        # zelig:
        "zelig": "+972585667666",
        # lior:
        "lior": "+972542101004",
        # elad:
        "elad": "+972542214882",
        # bremer:
        "bremer": "+972542868238",
        # yahav:
        "yahav": "+972542600073",
        # ilan:
        "ilan": "+972506506033",
        # mati:
        "mati": "+972535223182",
        "matvey": "+972535223182"
    }
    contacts_names = list(my_contact.keys())
    which_person = take_command()

    rightPerson = difflib.get_close_matches(which_person, contacts_names, len(contacts_names), 0)
    rightPhoneNumber = my_contact[rightPerson[0]]

    robot_say("What is the message?")
    body_text = take_command()
    try:
        k.sendwhatmsg(rightPhoneNumber, body_text, hour, minute)
    except:
        robot_say("I was failed to send the message")
