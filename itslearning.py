# -*- coding: utf-8 -*-

import os
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from xml.etree import ElementTree as ET
from BeautifulSoup import BeautifulSoup
import xmltodict, json
import datetime
import platform

def get_platform ():
    return platform.system()

def getdate():
    now = datetime.datetime.now()
    dateparts = []
    dateparts.append(now.year)
    dateparts.append(now.month)
    dateparts.append(now.day)
    return dateparts

def getweeknumber():
    dateparts = getdate()
    dt = datetime.date(dateparts[0], dateparts[1], dateparts[2])
    wk = dt.isocalendar()[1]
    return str(wk)

def getnextweek(suspendmode):
    nextweek = int(getweeknumber()) + 1 + suspendmode
    return str(nextweek)

def getyear():
    dateparts = getdate()
    dt = datetime.date(dateparts[0], dateparts[1], dateparts[2])
    yr = dt.isocalendar()[0]
    return str(yr)

def construct_url(student, student_id, base_url, suspendmode):
    url = base_url + '/parent/' + student_id + '/' + student + 'item/weeklyplansandhomework/item/class/' + getnextweek(suspendmode) + '-' + getyear()
    return url

def construct_planfile(student_id, suspendmode):
    planfile = os.path.dirname(os.path.abspath(__file__)) + '/plans/' + student_id + '_'+ str(getnextweek(suspendmode)) + '_' + str(getyear()) + '_plan.txt'
    return planfile

# print construct_url(getweeknumber(),getyear(),'Nora','460', 'https://skovlundeskole.m.skoleintra.dk')
def request_plan(student_id, student, site_url, userid, pwd, suspendmode):

    platform = get_platform()
    try:
        if platform == 'Windows':
            chromedriver = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver_win'
        if platform == 'Linux':
            chromedriver = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'
        options = webdriver.ChromeOptions();
        options.add_argument('headless');
        try:
            browser = webdriver.Chrome(chromedriver, chrome_options=options)
            #browser = webdriver.Chrome(chromedriver)

            browser.get(site_url)
            html_source = browser.page_source

            parsed_html = BeautifulSoup(html_source)

            # print(parsed_html.prettify())

            pagefile = os.path.dirname(os.path.abspath(__file__)) + '/pagefile.txt'
            try:
                os.remove(pagefile)
            except OSError:
                pass

            # Open a file
            fo = open(pagefile, "wb")
            fo.write(parsed_html.prettify());

            # Close opend file
            fo.close()

            with open(pagefile) as f:
                for line in f:
                    if 'type="submit" value="Login"' in line:
                        o = xmltodict.parse(line)
                        jsonobject = json.dumps(o)
            try:
                button_id = o['input']['@id']

                username = browser.find_element_by_name('UserName')
                username.send_keys(userid)
                password = browser.find_element_by_name('Password')
                password.send_keys(pwd)
                browser.find_element_by_id(button_id).click()

                try:
                    browser.get(construct_url(student, student_id, site_url, suspendmode))

                    html_source = browser.page_source

                    parsed_html = BeautifulSoup(html_source)
                    try:
                        plan_container = parsed_html.find("div", {"class": "sk-weekly-plan-container"})

                        text = ''.join(ET.fromstring(str(plan_container)).itertext())

                        clean_text = "".join([s for s in text.splitlines(True) if s.strip("\r\n")])

                        pagefile = construct_planfile(student_id, suspendmode)

                        try:
                            os.remove(pagefile)
                        except OSError:
                            pass

                        fo = open(pagefile, "wb")
                        fo.write(str(clean_text.encode('utf-8').strip()));
                        fo.close()
                        return 'OK'
                    except:
                        return 'Unable to parse file'
                except:
                    return 'Unable to get plan or plan not ready'
            except:
                return 'Unable to log in with user ' + str(userid)
        except:
            return 'Unable to get site url :' + str(site_url)
    except:
        return 'Unable to get Chromedriver'
