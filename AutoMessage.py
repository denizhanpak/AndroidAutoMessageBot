from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

df = pd.read_excel("./cs.xlsx")

# Extract first 10-digit number (ignoring non-digit characters)
df['phone_clean'] = df['Phone'].str.extract(r'(\d{3}\D*\d{3}\D*\d{4})')[0].str.replace(r'\D', '', regex=True)
df['phone_clean'] = df['phone_clean'].str[:10]  # Take first 10 digits

# Assuming your DataFrame has a 'name' column
names = df.dropna(subset=['phone_clean'])['First Name']
phones = df.dropna(subset=['phone_clean'])['phone_clean']

for n,p in (zip(names, phones)):
    print(n, p)

driver = webdriver.Firefox()
driver.get("https://messages.google.com/web/")

input("Press anything after QR scan")
time.sleep(5)

# names = []
# numbers = []
# with open("./test_list.txt") as f:
#     for line in f:
#         l = line.split()
#         names.append(l[0].strip())

#         if len(l) > 2:
#             numbers.append(l[1].strip())
#             names.append(l[0].strip())
#             numbers.append(l[2].strip())
#         else:
#             numbers.append(l[1].strip())


for name,number in zip(names, phones):
    if type(number) is tuple:
        print(number)
    message = f"Hey {name}! It’s Denizhan from the IGWC. We’re holding a Labor Day Rally to launch our new card drive this Monday, 12pm at Sample Gates. Please fill out this RSVP (it’s okay if you can’t make it, we can still send you the new card): http://igwc.work/labor-day" #Enter the Message 

    driver.find_element("link text","Start chat").click() #Click on Search contacts button
    time.sleep(3)
    driver.find_element("xpath","//input[@placeholder='Type a name, phone number, or email']").clear() #Locate and clear Searchbox
    driver.find_element("xpath","//input[@placeholder='Type a name, phone number, or email']").send_keys(number) #Type contact name
    time.sleep(7)
    driver.find_element("xpath","//mw-contact-selector-button/button").click() #Click on first contact
    time.sleep(7)
    try:
        box = driver.find_element("xpath","//textarea[@placeholder='RCS message']") #Locate message box
        if box:
            box.clear() #Locate and clear message box
            box.send_keys(message) #Type the message in message box
            box.send_keys(Keys.RETURN) #Press Enter
        else:
            box = driver.find_element("xpath","//textarea[@placeholder='Text message']") #Locate message box
            box.clear() #Locate and clear message box
            box.send_keys(message) #Type the message in message box
            box.send_keys(Keys.RETURN) #Press Enter
    except: 
        print(name, number)
        continue
