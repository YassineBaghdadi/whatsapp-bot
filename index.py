import datetime
import sys
import time
import datetime as dt
import json
import os
import requests
import shutil
import pickle

import pymysql
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from bs4 import BeautifulSoup

rate = 0.5
langs = {}

def conn():
    return pymysql.connect(host="10.73.100.101", user="user", password="user", port=3306, database="wsupbot")

def getLang(user) :
    cnx = conn()
    cur = cnx.cursor()
    cur.execute(f"""select lang from clients where phone like "{user}" or fullname like "{user}" ;""")
    lng = cur.fetchone()
    cnx.close()
    return lng

def getLastQ(user):
    cnx = conn()
    cur = cnx.cursor()
    cur.execute(f"select l.lastQ from lastQ l inner join clients c on l.usr = c.id where c.phone like {user} or c.fullname like {user};")
    lastQ = cur.fetchone()
    cnx.close()
    return lastQ



def logs(txt):
    ctime = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open("logs.txt", "a") as f:
        f.write(f"""@@ {ctime} ==> {txt}\n\n""")
    cnx = conn()
    cur = cnx.cursor()
    cur.execute(f"""insert into log(datetime, action)values("{ctime}", "{txt.replace("'", '"')}")""")
    cnx.commit()
    cnx.close()


class WhatsAppElements:
    search = (By.CSS_SELECTOR, "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
    msgTt = (By.CSS_SELECTOR, "#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div.p3_M1 > div > div._13NKt.copyable-text.selectable-text")
    # pin = (By.XPATH, """//*[@id="pane-side"]/div[1]/div/div/div[6]/div/div/div/div[2]/div[2]/div[2]/span[1]/div""")
    optionsBTN = (By.XPATH, """//*[@id="main"]/header/div[3]/div/div[2]/div/div""")
    closeChatBTN = (By.XPATH, """//*[@id="app"]/div[1]/span[4]/div/ul/div/div/li[5]/div[1]""")


class WhatsApp:
    browser =  None
    timeout = 20

    def __init__(self, wait, screenshot=None, session=None):
        self.browser = webdriver.Chrome(executable_path="chromedriver.exe")# change path
        self.browser.get("https://web.whatsapp.com/") #to open the WhatsApp web
        WebDriverWait(self.browser,wait).until(
        EC.presence_of_element_located(WhatsAppElements.search))
        logs("Started New Session ")
        # time.sleep(wait)

    def unread_usernames(self, scrolls=20):
        initial = 10
        usernames = []
        for i in range(0, scrolls):
            self.browser.execute_script(f"document.getElementById('pane-side').scrollTop={initial}")
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_3m_Xw"):
                if i.find("div", class_="_1pJ9J"):
                    username = i.find("div", class_="zoWT4").text
                    if username not in [i for i in langs.keys()]:
                        langs[username] = getLang(username)
                    usernames.append(username)
            initial += 10
        # Remove duplicates
        usernames = list(set(usernames))
        return usernames
    def get_last_sent_msg_for(self, name):
        messages = list()
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name + Keys.ENTER)
        time.sleep(0.5)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-out"):
            message = i.find("span", class_="selectable-text")
            if message:
                message2 = message.find("span")
                if message2:
                    messages.append(message2.text)
        messages = list(filter(None, messages))
        return messages


    def get_last_message_for(self, name):
        messages = list()
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name + Keys.ENTER)
        time.sleep(0.5)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-in"):
            message = i.find("div", class_="copyable-text")
            if message:
                message2 = message.find("span")
                if message2:
                    messages.append(message2.text)
        messages = list(filter(None, messages))
        return messages


    def send_to(self, user, msg):

        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(user + Keys.ENTER)
        time.sleep(0.5)
        # soup = BeautifulSoup(self.browser.page_source, "html.parser")
        msgT = self.browser.find_element(*WhatsAppElements.msgTt)
        msg += "\n\n# --> page d'accueil"
        if "\n" in msg:
            for line in msg.split('\n'):
                ActionChains(self.browser).send_keys(line).perform()
                ActionChains(self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ActionChains(self.browser).send_keys(Keys.RETURN).perform()
            # msgT.send_keys(Keys.ENTER)
        else:
            msgT.send_keys(msg + Keys.ENTER)
        # msgT.send_keys(msg + Keys.ENTER)
        time.sleep(0.5)
        logs(f"Message sent to : {user}")
        # self.browser.refresh()

        #
        # pin = self.browser.find_element(*WhatsAppElements.pin)
        # pin.click()


    def closeChat(self):
        try:
            home = self.browser.find_element_by_class_name("WM0_u")
            print("no chat opened ...")
        except NoSuchElementException:

            self.browser.find_element(*WhatsAppElements.optionsBTN).click()
            time.sleep(0.5)
            # self.browser.find_element(*WhatsAppElements.closeChatBTN).click()

            html_list = self.browser.find_element_by_xpath("""//*[@id="app"]/div[1]/span[4]/div""")
            items = html_list.find_elements_by_tag_name("li")
            for item in items:
                if item.text == "Close chat":
                    item.click()


    def archiveChat(self, user):
        try:
            search = self.browser.find_element(*WhatsAppElements.search)
            search.send_keys(user)
            action = ActionChains(self.browser)

            time.sleep(1.5)
            theUser = self.browser.find_element_by_class_name("HONz8")

            # theUser = self.browser.find_element_by_css_selector("#pane-side > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div._3OvU8 > div._3vPI2 > div.zoWT4 > span > span > span")
            # theUser = None
            # choises = self.browser.find_elements_by_class_name("ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr")
            # for i in choises:
            #     if i .text == user:
            #         theUser = i
            print(theUser)
            action.context_click(theUser).perform()
            #
            time.sleep(0.8)
            html_list = self.browser.find_element_by_xpath("""//*[@id="app"]/div[1]/span[4]/div""")
            items = html_list.find_elements_by_tag_name("li")
            for item in items:
                if item.text == "Archive chat":
                    item.click()
            #
            time.sleep(0.5)
            self.browser.find_element_by_css_selector("#side > div.uwk68 > div > button > div._1KJ7A.bHvlO").click()
            print(f'## {user} Archived Successfully.')
            logs(f"{user} Archived Successfully")
        except Exception as e:
            print(f'Archive {user} Failed. ERROR : {e}')
            logs(f"Archive {user} Failed. ERROR : {e}")


class Qst:
    def __init__(self, qts, ansrs):
        self.qts = qts
        self.ansrs = ansrs





whatsapp = WhatsApp(120, session="mysession")

wlcmar = """مرحباً ، نحن شركة توظيف كندية مقرها المغرب. نقوم بتوظيف العديد من الملفات الشخصية في قطاع المطاعم والمطابخ في كندا مع كل الدعم اللازم ، يرجى إرسال طلبك إلينا على canadarecrut@saccomcg.com حتى يتمكن موظف التوظيف من الإجابة على جميع أسئلتك. يوم رائع."""
wlcmfr = """Bonjour, nous sommes un cabinet de recrutement canadien basé au Maroc. Nous recrutons plusieurs profils dans le secteur de restauration et la cuisine au Canada avec tout l'accompagnement nécessaire, merci de nous envoyer votre candidature sur canadarecrut@saccomcg.com afin qu'une chargée de recrutement puisse répondre à toutes vos questions. Excellente journée."""
# whatsapp.archiveChat("+212 630-504606")

# print(whatsapp.get_last_sent_msg_for("+212 630-504606")[-1])
cnx = conn()
cur = cnx.cursor()
userlang = {}
tr = {"merci pour votre temps, un agent continuera avec vous dès que possible":"شكرًا لك على وقتك ، سيتواصل معك أحد الوكلاء في أقرب وقت ممكن"}

QnA = {"Quel sont les profils pour lesquels vous recrutez ?":"Restauration et Hôtellerie ( Managers, Shift-managers, Cuisiniers et Pâtissiers, Boulangers). Si vous êtes intéressés, envoyez-nous vos cordonnés pour qu'on puisse vous contacter. Juste votre numéro de tél suffit",
       "Comment faire pour postuler ?":"Envoyez votre CV ou seulement votre numéro de tel ici ou par mail à: canadarecrute@saccomcg.com, un chargé de recrutement se chargera de vous appeler. ",
       "J'ai des questions, je veux parler à quelqu'un. Merci":"Bonjour, merci de nous laisser votre / vos questions, nous allons répondre le plus tôt possible. Si vous êtes intéressé, envoyez-nous votre numéro de téléphone pour qu'on puisse vous contacter.",
       "Après le Covid-19, Est ce que l'immigration au Canada est toujours possible ?":"Oui, c'est possible nous avons d'ailleurs accompagné plusieurs candidats-clients et familles marocains qui sont actuellement au Canada. Si vous êtes intéressé, envoyez-nous vos cordonnés pour qu'on puisse vous ",
       "C'est quoi votre Numéro de téléphone":"05228-62839",
       "C'est quoi votre Adresse":"Bonjour, Nos locaux sont situés au 53-55, Rue Imam Boukhari, Socrate. Casablanca. Localisation :\nhttps://goo.gl/maps/SAAhMHJFnmSQoLRFA",
       "J’ai déjà postulé mais tjr sans réponse ": "Merci pour l'intérêt porté a notre structure, Merci de nous écrire votre nom et prénom complet. Nous vous répondons dans les brefs délais. Excellente journée ",
       "Intéressé par un poste":"Merci pour l'intérêt porté à notre structure, merci de nous envoyer votre candidature sur canadarecrute@saccomcg.com afin d'analyser votre profil et vous accompagner au mieux. Excellente journée",
       "Renseignement":"Merci pour l'intérêt porté à notre structure, merci de nous envoyer votre candidature sur canadarecrute@saccomcg.com ou nous laisser votre numéro de téléphone, afin qu'une chargée de recrutement puisse",
       "Avez-vous reçu mon CV ?":"Merci pour l'intérêt porté a notre structure, Merci de nous écrire votre nom et prénom complet afin de vérifier la réception de votre candidature. Nous vous répondons dans les brefs délais. Excellente journée  😊",
       }

# whatsapp.archiveChat("karim")

wrong = "wrong answer please try again"
while True:
    # try:
        whatsapp.closeChat()
        user_names = whatsapp.unread_usernames(scrolls=100)
        for name in user_names:
            messages = whatsapp.get_last_message_for(name)
            sent_messages = whatsapp.get_last_sent_msg_for(name)

            logs(f"got a message from : {name}")
            messgaes_len = len(messages)
            latest_msg = messages[messgaes_len-1] if len(messages) > 1 else messages
            txt = ""

            print(f'Message : {messages}\nlen : {messgaes_len}\nlatest msg : {latest_msg}')

            if messages:
                if latest_msg == "#":
                    cur.execute(f'update clients set lastQ = 2 where phone like "{name}" or fullname like "{name}"')
                    cnx.commit()
                    cur.execute(f'select qts from QTS where id = 2')
                    txt += f"{cur.fetchone()[0]}\n\n"

                    cur.execute(f'select ansr from ansrs where qts = 2;')
                    for i, v in enumerate([i[0] for i in cur.fetchall()]):
                        txt += f'{i + 1} --> {v}\n'

                    whatsapp.send_to(name, txt)
                    continue
                if len(sent_messages) < 1:
                    cur.execute(f'insert into clients(firstmsgdate, phone)values ("{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}", "{name}")')
                    cnx.commit()
                    whatsapp.send_to(name, wlcmar)
                    whatsapp.send_to(name, wlcmfr)
                    txt = ""
                    cur.execute(f'select qts from QTS where id = 1')
                    txt += f"{cur.fetchone()[0]}\n\n"

                    cur.execute(f'select ansr from ansrs where qts = 1;')
                    for i, v in enumerate([i[0] for i in cur.fetchall()]):
                        txt += f'{i+1} --> {v}\n'
                    whatsapp.send_to(name, txt)
                    cur.execute(f'update clients set lastQ = 1 where phone like "{name}" or fullname like "{name}"')
                    cnx.commit()
                else:
                    print(f"""select lastQ from clients where phone like "{name}" or fullname "{name}";""")
                    cur.execute(f"""select lastQ from clients where phone like "{name}" or fullname like "{name}";""")
                    lastQId = cur.fetchone()[0]
                    if str(lastQId) == "1":
                        if latest_msg in ["1", "2"]:
                            lng = "fr"
                            if latest_msg == "1":
                                lng = "ar"
                            cur.execute(f'update clients set lang = "{lng}" where phone like "{name}" or fullname like "{name}";')
                            userlang[name] = lng

                            cur.execute(
                                f'update clients set lastQ = 2 where phone like "{name}" or fullname like "{name}"')
                            cnx.commit()
                            txt = ""
                            cur.execute(f'select qts from QTS where id = 2')
                            txt += f"{cur.fetchone()[0]}\n\n"

                            cur.execute(f'select ansr from ansrs where qts = 2;')
                            for i, v in enumerate([i[0] for i in cur.fetchall()]):
                                txt += f'{i + 1} --> {v}\n'

                            whatsapp.send_to(name, txt)
                        else:
                            whatsapp.send_to(name, wrong)
                            txt = ""
                            cur.execute(f'select qts from QTS where id = 1')
                            txt += f"{cur.fetchone()[0]}\n\n"

                            cur.execute(f'select ansr from ansrs where qts = 1;')
                            for i, v in enumerate([i[0] for i in cur.fetchall()]):
                                txt += f'{i + 1} --> {v}\n'
                            whatsapp.send_to(name, txt)

                    if str(lastQId) == "2":

                        if latest_msg in [str(i) for i in range(1, 4)]:
                            if latest_msg == '1':
                                whatsapp.send_to(name, "merci pour votre temps, un agent continuera avec vous dès que possible" if langs[name] == "fr" else tr["merci pour votre temps, un agent continuera avec vous dès que possible"])
                                whatsapp.archiveChat(name)
                            if latest_msg == "2":
                                txt = "Pour quelle offre vous voulez postuler ?\n\n"
                                # cur.execute(f"select ansr from ansrs where qts = 3")
                                txt += "\n".join([f"{i+1} --> {v}" for i, v in enumerate(["Recrutement National", "Recrutement International"])])

                                whatsapp.send_to(name, txt)
                                cur.execute(f'update clients set lastQ = 3 where phone like "{name}" or fullname like "{name}"; ')
                                cnx.commit()


                            if latest_msg == "3":
                                cur.execute(f'update clients set lastQ = 6 where phone like "{name}" or fullname like "{name}"; ')
                                cnx.commit()
                                txt = "Q/N ??\n\n"
                                txt += "\n".join([f'{i+1} --> {v}' for i, v in enumerate(QnA.keys())])
                                whatsapp.send_to(name, txt)
                                # txt = ""
                                # cur.execute(f'select qts from QTS where id = 6')
                                # txt += f"{cur.fetchone()[0]}\n\n"
                                #
                                # cur.execute(f'select ansr from ansrs where qts = 6;')
                                # for i, v in enumerate([i[0] for i in cur.fetchall()]):
                                #     txt += f'{i + 1} --> {v}\n'
                                #
                                # whatsapp.send_to(name, txt)
                        else:
                            whatsapp.send_to(name, wrong)
                            txt = ""
                            cur.execute(f'select qts from QTS where id = 2')
                            txt += f"{cur.fetchone()[0]}\n\n"

                            cur.execute(f'select ansr from ansrs where qts = 2;')
                            for i, v in enumerate([i[0] for i in cur.fetchall()]):
                                txt += f'{i + 1} --> {v}\n'

                            whatsapp.send_to(name, txt)


                    if str(lastQId) == "3":

                        if latest_msg in [str(i) for i in range(1, 3)]:
                            if latest_msg == "1":
                                txt = "National offres :\n\n"
                                cur.execute(f"select ansr from ansrs where qts = 4")
                                txt += "\n".join([f"{i+1} --> {v[0]}" for i, v in enumerate(cur.fetchall())])
                                whatsapp.send_to(name, txt)
                                cur.execute(
                                    f'update clients set lastQ = 7 where phone like "{name}" or fullname like "{name}";')
                                cnx.commit()
                                # whatsapp.send_to(name, "Merci de nous envoyer vos coordonnées ainsi que votre CV")

                            if latest_msg == "2":
                                txt = "International offres :"
                                cur.execute(f"select ansr from ansrs where qts = 5")
                                ansrs = [i[0] for i in cur.fetchall()]
                                txt += "\n".join([f"{i+1} --> {v}" for i, v in enumerate(ansrs)])
                                whatsapp.send_to(name, txt)
                                cur.execute(
                                    f'update clients set lastQ = 7 where phone like "{name}" or fullname like "{name}";')
                                cnx.commit()
                                # whatsapp.send_to(name, "Merci de nous envoyer vos coordonnées ainsi que votre CV")


                        else:
                            whatsapp.send_to(name, wrong)
                            txt = "Pour quelle offre vous voulez postuler ?\n\n"
                            # cur.execute(f"select ansr from ansrs where qts = 3")
                            txt += "\n".join([f"{i + 1} --> {v}" for i, v in
                                              enumerate(["Recrutement National", "Recrutement International"])])

                            whatsapp.send_to(name, txt)


                    if str(lastQId) == "6":
                        if latest_msg == "3":
                            whatsapp.send_to(name, QnA[[i for i in QnA.keys()][2]])

                            whatsapp.archiveChat(name)
                            continue
                        if latest_msg in [str(i) for i in range(1, len([i for i in QnA.keys()])+1)]:
                            whatsapp.send_to(name, QnA[[i for i in QnA.keys()][int(latest_msg)-1]])
                            txt = "Q/A ??\n\n"
                            txt += "\n".join([f'{i + 1} --> {v}' for i, v in enumerate(QnA.keys())])
                            whatsapp.send_to(name, txt)
                        else:
                            whatsapp.send_to(name, wrong)

                            txt = "Q/A ??\n\n"
                            txt += "\n".join([f'{i + 1} --> {v}' for i, v in enumerate(QnA.keys())])
                            whatsapp.send_to(name, txt)


                    if str(lastQId) == "7":
                        ll = []
                        txt = whatsapp.get_last_sent_msg_for(name)[-1]
                        for i in txt.split("-->"):
                            ii = i.replace("\n", "").replace("National offres :1", "").replace("#", "").replace(
                                "page d'accueil", "").replace("International offres :1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "")
                            print(ii)
                            if ii.strip():
                                ll.append(ii.strip())

                        try:
                            cur.execute(f'update clients set interest = "{ll[int(latest_msg.strip())-1]}" where fullname like "{name}" or phone like "{name}"')
                        except :
                            pass

                        whatsapp.send_to(name, "Merci de nous envoyer vos coordonnées ainsi que votre CV")
                        #set interests
                        lastsent = whatsapp.get_last_sent_msg_for(name)

                        cur.execute(
                            f'update clients set lastQ = 8 where phone like "{name}" or fullname like "{name}";')
                        cnx.commit()


                    if str(lastQId) == "8":
                        whatsapp.send_to(name, """Merci, nous avons bien reçu votre candidature et nous vous remercions pour la confiance que vous nous témoignez.
                        Sans réponse de notre part dans un délai de 15 jours, vous pourrez considérer que votre dossier n'aura pas été retenu pour le poste demandé.
                        Nous nous permettons cependant de conserver votre CV dans notre base de données et ne manquerons pas de vous recontacter dès qu'une opportunité répondant à vos attentes se présentera.
                        Très cordialement.""")
                        whatsapp.archiveChat(name)
                        cur.execute(
                            f'update clients set lastQ = 2 where phone like "{name}" or fullname like "{name}";')
                        cnx.commit()















                # cur.execute(f'select count(id) where fullname like "{name}" or phone like "{name}"')
                # if not cur.fetchone()[0]:
                #     cur.execute(f'insert into clients(phone)value ("{name}");')
                #     cnx.commit()
                #
                # cur.execute(f'select lang from clients where fullname like "{name}", or phone like "{name}";')
                # lang = cur.fetchone()
                # if
                #
                # if not messgaes_len:
                #     whatsapp.send_to(name, lang)


                whatsapp.closeChat()


        time.sleep(rate)
        print('refreshing ...')
    # except Exception  as e :
    #     print(f"ERROR ==> {e}")
    #     logs(f"System down ERROR : {e}")
    #     cnx.close()

cnx.close()