import smtplib
import requests
from datetime import datetime
import time

MY_LAT = X.X
MY_LONG = X.X


def iss_is_on_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5):
        if (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5):
            return True
    return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()

    if time_now.hour <= sunrise or time_now.hour >= sunset:
        return True
    else:
        return False


def send_email():
    my_email = "XXXXXXX@google.com"
    password = "XXXX XXXX XXXX XXXX"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="XXXXXX@gmail.com",
            msg=f"Subject:ISS\n\nISS on ME!!")


test = 0
while True:
    if iss_is_on_me() and is_dark():
        send_email()
        print("ISS on me! email send!")
    print("ISS far away")
    time.sleep(60)
    test += 1
    print(f"Test number: {test}")
