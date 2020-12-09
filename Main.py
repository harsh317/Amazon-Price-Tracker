import requests
from bs4 import BeautifulSoup
import smtplib
import time
from datetime import datetime, timedelta
url = input("Enter Amazon product page link:")


headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

def check_price():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    f = soup.find(id="priceblock_ourprice").get_text()
    available = soup.find(id="availability").get_text().strip()
    if available != "In stock.":
        print("Stock is not available!!")
        send_mail("Soory Product is Sold Out!!!Now Cry","Sold out")
        exit()

    converted_price = f[2:10]
    converted_price = converted_price.replace(',', '')
    converted_price = float(converted_price)

    print("Product price was:",converted_price)
    print("The product name was:",title.strip())
    print("The product is ", available)
    try:
        minimum = int(input("Tell the Minimum price you want the product to come down:"))
        print("please enter amount that is low to the actual ammont")
    except:
        print("Type numbers only")

    if (converted_price < minimum or converted_price == minimum):
        send_mail(f"Hey whom is seeing this , i want to tell that the price fell down to {converted_price}.....check the amazon link:{url}","Alert!!!!!!!!Price down")


    send_mail("This is to check if it worked","trial Mail!!!!")
    print("A Confirmation Email Has Been Sent...we will inform you if price goes down below",minimum)

def send_mail(body_main,subject_mail):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('abcd@gmail.com','mygmailpassword')
    subject = subject_mail
    body = body_main
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'abcdto@gmail.com',
        'abcdfrom@gmail.com',
        msg
    )
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    next = str(datetime.now() + timedelta(hours=24))[11:19]
    print("Email Sent..!\nEmail sent at:",time_string,"\n Next try after:",next)

    server.quit()
while True:
    check_price()
    time.sleep(60*(60*24))
