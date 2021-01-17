from bs4 import BeautifulSoup
import os
import smtplib, ssl # for email
from urllib.request import Request, urlopen
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#setup email
port = 465
email_password = os.getenv('ETEXT_PASS')
email_sender = os.getenv('ETEXT_EMAIL')
context = ssl.create_default_context()
server = smtplib.SMTP_SSL('smtp.gmail.com', port, context=context)
try:
    server.login(email_sender, email_password)
except:
    print('could not sign in to email')

# hardcode the page at first, then later we will get it live
# with open('genshin.html') as fp:
#     soup = BeautifulSoup(fp, 'html.parser')

url = 'https://www.pockettactics.com/genshin-impact/codes'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

tmp = soup.findAll("div", {"class": "entry-content"})[0].findAll("ul")[1].findAll("strong")


try:
    f = open('used_keys.txt', 'r')
except:
    open('used_keys.txt', 'a').close()
    f = open('used_keys.txt', 'r')

used_keys = f.read()
f.close()

f = open('used_keys.txt', 'a')

for code in tmp:
    code = code.string.strip()
    if code in used_keys:
        continue
    
    tmp = 'NEW GENSHIN CODE: ' + code + '\nhttps://genshin.mihoyo.com/en/gift'
    print(tmp)

    msg = MIMEMultipart()
    body = tmp
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()

    try:
        server.sendmail(email_sender, os.getenv('ETEXT_ZACH'), sms)
    except:
        print('could not send message to Zach')
    
    try:
        server.sendmail(email_sender, os.getenv('ETEXT_ADAM'), sms)
    except:
        print('could not send message to Adam')

    try:
        server.sendmail(email_sender, os.getenv('ETEXT_MOE'), sms)
    except:
        print('could not send message to Adam')

    f.write(code + '\n')

f.close()
server.quit()
