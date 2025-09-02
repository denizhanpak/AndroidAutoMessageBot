from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def safe_click(driver, by, value, timeout=10):
    """Safely click an element with explicit wait"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return True
    except (TimeoutException, NoSuchElementException):
        print(f"Could not click element: {value}")
        return False

def safe_send_keys(driver, by, value, text, timeout=10, clear_first=True):
    """Safely send text to an element with explicit wait"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        if clear_first:
            element.clear()
        element.send_keys(text)
        return True
    except (TimeoutException, NoSuchElementException):
        print(f"Could not send keys to element: {value}")
        return False

def find_message_box(driver, timeout=10):
    """Find the message box with multiple fallback options"""
    selectors = [
        (By.XPATH, "//textarea[@placeholder='RCS message']"),
        (By.XPATH, "//textarea[@placeholder='Text message']"),
        (By.TAG_NAME, "textarea"),
        (By.CSS_SELECTOR, "textarea[placeholder*='message']"),
        (By.CSS_SELECTOR, "div[contenteditable='true']")
    ]
    
    for by, value in selectors:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except (TimeoutException, NoSuchElementException):
            continue
    
    return None



df = pd.read_excel("./texting_test.xlsx")
print(df)
# Extract first 10-digit number (ignoring non-digit characters)
df['phone_clean'] = df['Phone'].astype(str).str.extract(r'(\d{3}\D*\d{3}\D*\d{4})')[0].str.replace(r'\D', '', regex=True)


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

print("Error could not be reached:")

for name,number in zip(names, phones):
    if number[0] == "1":
        number = number[1:11]  # Take first 10 digits
    else:
        number = number[:10]  # Take first 10 digits
    message = f"Hey {name}! It's Denizhan with the IGWC! the 2025 union card went live monday and already over 200 workers have signed! sign even if you've signed before. https://indianagradworkers.org/card" #Enter the Message 
    
    # Your refactored code flow
    try:
        # Click on "Start chat" button
        if not safe_click(driver, By.LINK_TEXT, "Start chat"):
            print("Failed to click 'Start chat' button")
            # Handle this error appropriately
            
        # Wait for search box and enter number
        if not safe_send_keys(driver, By.XPATH, "//input[@placeholder='Type a name, phone number, or email']", 
                            number, clear_first=True):
            print("Failed to enter phone number")
            # Handle this error appropriately
            
        time.sleep(7)  # Consider replacing with explicit wait if possible
        
        # Click on first contact
        if not safe_click(driver, By.XPATH, "//mw-contact-selector-button/button"):
            print("Failed to click first contact")
            # Handle this error appropriately
            
        time.sleep(7)  # Consider replacing with explicit wait if possible
        
        # Find and use message box
        box = find_message_box(driver)
        if box:
            box.clear()
            box.send_keys(message)
            box.send_keys(Keys.RETURN)
            print(f"Message sent to {name} ({number})")
        else:
            print(f"Could not find message box for {name} ({number})")
            # Consider taking a screenshot for debugging
            # driver.save_screenshot(f"error_{number}.png")
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Failed to send message to {name} ({number})")

    # driver.find_element("link text","Start chat").click() #Click on Search contacts button
    # time.sleep(3)
    # driver.find_element("xpath","//input[@placeholder='Type a name, phone number, or email']").clear() #Locate and clear Searchbox
    # driver.find_element("xpath","//input[@placeholder='Type a name, phone number, or email']").send_keys(number) #Type contact name
    # time.sleep(7)
    # driver.find_element("xpath","//mw-contact-selector-button/button").click() #Click on first contact
    # time.sleep(7)
    # try:
    #     box = driver.find_element("xpath","//textarea[@placeholder='RCS message']") #Locate message box
    #     if box:
    #         box.clear() #Locate and clear message box
    #         box.send_keys(message) #Type the message in message box
    #         box.send_keys(Keys.RETURN) #Press Enter
    #     else:
    #         box = driver.find_element("xpath","//textarea[@placeholder='Text message']") #Locate message box
    #         box.clear() #Locate and clear message box
    #         box.send_keys(message) #Type the message in message box
    #         box.send_keys(Keys.RETURN) #Press Enter
    # except e: 
    #     print(e)
    #     print(name, number)
    #     continue
