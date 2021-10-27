import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import *
import time


#when using the real website we will have to use requests to access and login:
#payload = {'UserName': 'USERNAME', 'Password': 'PASSWORD'}
#url = 'http://www.website.com'
#requests.post(url, data=payload)
#Then we can use BeautifulSoup to extract data from it. 

#just giving more space to make it easier to read on command prompt 
print('')
print('')

#creating lists:
account=[]
tags=[]
security=[]
company=[]
trade=[]
settle=[]
CUSIP=[]

#Today's date:
date=datetime.today()
#getting 7 days ago AKA 5 business days
date_7 = datetime.now() - timedelta(days=7)



#accessing the website:
with open('article2.html') as html_file:
    soup = BeautifulSoup(html_file, 'html.parser')

#getting all links:
for tag in soup.find_all('a', href=True):
    #print('href:', tag['href'])
    tags.append(tag['href'])
    
#opening all links:
for links in tags:
    with open(links) as html:
        link=BeautifulSoup(html, 'html.parser')
        for tag in link.find_all('div', class_='account'):
            print('Account#')
            print(tag.text)
            account.append(tag.text)
        for tag in link.find_all('div', class_='security'):
            security.append(tag.text)
        for tag in link.find_all('div', class_='company'):
            company.append(tag.text)
        for tag in link.find_all('div', class_='trade'):
            tradeDate=tag.box.text
            date_trade= datetime.strptime(tradeDate, '%d/%m/%Y')
            #checking if date older than 5 business days
            if date_trade < date_7:
                #if this shows on cmd prompt means that the account number above have a trade date of more than 5 business days ago.
                go=input('**** WARNING -> OLDER than 5 business days**** Press Enter to continue')
                print('')  
                print('')                
            trade.append(tag.text)
        for tag in link.find_all('div', class_='settle'):
            settle.append(tag.text)
        for tag in link.find_all('div', class_='CUSIP'):
            CUSIP.append(tag.text)

#creating new lists 
accounts = []
securities =[]
companies = []
trades=[]
settles=[]
CUSIPS=[]

#creating loop to delete "\n" from strings
for string in account:
    new_string = string.replace("\n", "")
    accounts.append(new_string)
for string in security:
    new_string = string.replace("\n", "")
    securities.append(new_string)
for string in company:
    new_string = string.replace("\n", "")
    companies.append(new_string)
for string in trade:
    new_string = string.replace("\n", "")
    trades.append(new_string)
for string in settle:
    new_string = string.replace("\n", "")
    settles.append(new_string)
for string in CUSIP:
    new_string = string.replace("\n", "")
    CUSIPS.append(new_string)    
    
    
#adding info to dataframe using pandas
df=pd.DataFrame(list(zip(accounts,securities,companies,trades,settles,CUSIPS)),columns=['Account#', 'Security Name:', 'Company:', 'Trade Date:','Settle Date:','CUSIP#:'])
#print(df)
#**********add code to send dataframe to excel************