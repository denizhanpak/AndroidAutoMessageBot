from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("https://messages.google.com/web/")

input("Press anything after QR scan")
time.sleep(5)

names = []
numbers = []
with open("./informatics_list_test") as f:
    for line in f:
        l = line.split()
        names.append(l[0].strip())

        if len(l) > 2:
            numbers.append(l[1].strip())
            names.append(l[0].strip())
            numbers.append(l[2].strip())
        else:
            numbers.append(l[1].strip())


for name,number in zip(names,numbers):
    if type(number) is tuple:
        print(number)
    message = f"Hey {name}, thank you for signing your union card. This is a reminder that on Friday at 4pm we will have a town hall with card signers in Luddy to answer any questions and plan how to spread the word. Hope to see you there! https://tinyurl.com/SICE-UE" #Enter the Message 
    print(message)

    driver.find_element_by_xpath("//span/div[2]").click() #Click on Search contacts button
    time.sleep(3)
    driver.find_element_by_xpath("//input[@placeholder='Type a name, phone number, or email']").clear() #Locate and clear Searchbox
    driver.find_element_by_xpath("//input[@placeholder='Type a name, phone number, or email']").send_keys(number) #Type contact name
    time.sleep(7)
    driver.find_element_by_xpath("//mw-contact-selector-button/button").click() #Click on first contact
    time.sleep(7)
    driver.find_element_by_xpath("//textarea[@placeholder='Text message']").clear() #Locate and clear message box
    driver.find_element_by_xpath("//textarea[@placeholder='Text message']").send_keys(message) #Type the message in message box
    driver.find_element_by_xpath("//mws-message-compose/div/mws-message-send-button/button/span").click() #Click on Send button
