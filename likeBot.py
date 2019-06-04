# -*- coding: utf-8 -*-
#IMPORTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import os

print('Author:       IG @Hboss2')
print('Last Update:  06/03/2019')
print('\n')
time.sleep(3)

email = 'ENTER EMAIL'#                                      <<<<<<<<<<<<<< This will be the email receiving Like Cycle Update

def main():
    """
    Selenium bot logins to users Instagram and will loop through given Hashtags and like pictures within the hashtags. 
    At the end of a Like Cycle, the user will receive an email with how many followers the user has gained. 
    Variables with "<<<<<<<<<<<<" need to be replaced. Explanation of each variable will be provided next to arrows.
    """
    totalLiked = 0
    urlsCollected = []
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    chromedriver = desktop + '/chromedriver'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chromedriver, chrome_options=options)
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)

    try:
        login = driver.find_elements_by_tag_name('input')
        login[0].send_keys('USERNAME')#                     <<<<<<<<<<<<<<< Instagram Username
        login[1].send_keys('PASSWORD', Keys.ENTER)#         <<<<<<<<<<<<<<< Instagram Password
    except NoSuchElementException:
        print('No input to log in')

    time.sleep(3)

    try:
        driver.find_element_by_css_selector('body > div > div > div > div > button').click()
    except NoSuchElementException:
        print('No notification pop up')
    time.sleep(10)
    driver.get('https://www.instagram.com/USERNAME/')#      <<<<<<<<<<<<<<< Append Instagram Username to URL
    startFollower = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').text    
    #Append any additional hashtags. Hashtags provided are top 2019 hashtags
    hashtags = [
        'https://www.instagram.com/explore/tags/love/',
        'https://www.instagram.com/explore/tags/instagood/',
        'https://www.instagram.com/explore/tags/photooftheday/',
        'https://www.instagram.com/explore/tags/fashion/',
        'https://www.instagram.com/explore/tags/beautiful/',
        'https://www.instagram.com/explore/tags/happy/',
        'https://www.instagram.com/explore/tags/cute/',
        'https://www.instagram.com/explore/tags/tbt/',
        'https://www.instagram.com/explore/tags/like4like/',
        'https://www.instagram.com/explore/tags/followme/',
        'https://www.instagram.com/explore/tags/picoftheday/',
        'https://www.instagram.com/explore/tags/follow/',
        'https://www.instagram.com/explore/tags/me/',
        'https://www.instagram.com/explore/tags/selfie/',
        'https://www.instagram.com/explore/tags/summer/',
        'https://www.instagram.com/explore/tags/art/',
        'https://www.instagram.com/explore/tags/instadaily/',
        'https://www.instagram.com/explore/tags/friends/',  
        'https://www.instagram.com/explore/tags/repost/',  
        'https://www.instagram.com/explore/tags/nature/',  
        'https://www.instagram.com/explore/tags/girl/',  
        'https://www.instagram.com/explore/tags/fun/',  
        'https://www.instagram.com/explore/tags/style/',                                                
        'https://www.instagram.com/explore/tags/smile/',   
        'https://www.instagram.com/explore/tags/food/',             
        'https://www.instagram.com/explore/tags/throwback/'  
        ]

    print('Going through ' + str(len(hashtags)) + ' hashtags')
    counter = 1

    for i in hashtags:
        print('')
        print('Hashtag #' + str(counter))
        if counter % 2 == 0:
            time.sleep(120)
        time.sleep(90)
        print(i)
        print('')
        driver.get(i)
        time.sleep(5)
        for x in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        profiles = driver.find_elements_by_css_selector('#react-root > section > main > article > div > div > div > div > a')
        picURL = []
        for pro in profiles:       
            picURL.append(pro.get_attribute('href'))
        print('')
        counterLike = 1
        print('Liking ' + str(len(picURL)))
        for y in picURL:
            totalLiked += 1
            print('Like #' + str(counterLike))
            if counterLike % 2 == 0:
                time.sleep(120)
            driver.get(y)
            time.sleep(60)
            try:
                driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div > section > span > button').click()
                urlsCollected.append(i)    
            except NoSuchElementException:
                print('Broken Link')
            counterLike += 1
        counter += 1
            
    #This feature is added for future program that will take all the pictures that program liked through Like Cycles and dislike the pictures
    with open('C:/Users/UserName/Desktop/Instagram/dislikeUrls.csv', 'a') as f:#    <<<<<<<<<<<<<<<<< Change file destination
        wr = csv.writer(f, dialect='excel')
        wr.writerow(urlsCollected)
    
    #Time Block
    nowP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").split(' ')
    hour = now[1].split(':')
    if int(hour[0]) >= 12:
        normal = int(hour[0]) - 12
        hour[0] = str(normal)
        normalTime = ':'.join(hour)
        now[1] = normalTime
        nTime = ' '.join(now)
        timestamp = ["Last Like Cycle || Timestamp: " + str(nTime) + ' PM']
    else:
        timestamp = ["Last Like Cycle || Timestamp: " + str(nowP) + ' AM']

    driver.get('https://www.instagram.com/USERNAME/')#              <<<<<<<<<<<< Instagram Username
    endFollowers = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').text          
    msg = MIMEMultipart()
    msg['From'] = 'User Email' #                                    <<<<<<<<<<<< Email Address that you have a password for
    msg['To'] = email                                              
    msg['Subject'] = timestamp
    body = 'You started with ' + str(startFollower) + '. After the script was done running you ended with, ' + str(endFollowers) + '</br>\n The script liked a total of: ' + str(totalLiked)
    #attach the body to the message as html
    msg.attach(MIMEText(body, 'html'))
    print(msg)
    #initilize the sever
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)#               <<<<<<<<<<<<<< This is Gmail server, replace to your email provider if you do not user Gmail
    server.login('User Email', 'User Email Password')#              <<<<<<<<<<<<<< Same as From variable, add your password. Its okay to send yourself emails!
    #send the email
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    #close the server
    server.quit()


if __name__ == '__main__':
    main()
