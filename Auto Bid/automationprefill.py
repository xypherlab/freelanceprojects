from selenium import webdriver
import time
from pyautogui import write
import pyautogui
option = webdriver.ChromeOptions()
#option.add_argument("-incognito")
#option.add_argument("--headless")
#option.add_argument("disable-gpu")

email=["a@gmail.com","b@gmail.com","C@gmail.com"]
name=["Andres","Rizal","Juan Tamad"]
address=["Banawe","Ilocos","Bicol"]
platenumber=["ABA123","DAD367","DOG123"]
biddertype=["1","0","0"] #Individual=0 or Company=1
gender=["1","2","2"] #Male=1 or Female=2
carselect=["1","3","2"] #3 Cars
number=["+639065554255","+639065554256","+639065554257"]

#for j in range(len(email)):
for i in range(1):
    browser = webdriver.Chrome(executable_path="C:\\Users\\USER\Desktop\\scrapdata\\chromedriver.exe", options=option)

    browser.get('https://docs.google.com/forms/d/e/1FAIpQLSeG6MLgdIsFkVuLU4I97CF74_NHVNT3ArC-HhqekkfICFqORg/viewform?usp=pp_url&emailAddress=xypher@gmail.com&entry.23249824=Yes&entry.1882979912=Male&entry.1447596059=a&entry.411635796=a&entry.216445732=a&entry.892874713=I+agree&entry.1683885721=Individual&entry.441696145=Car+1&entry.1266154365=lot123')

    submit=browser.find_element_by_class_name("appsMaterialWizButtonPaperbuttonContent")

    browser.find_element_by_class_name("quantumWizMenuPaperselectOptionList").click()

    submit.click()
    time.sleep(0.1)
    #Page 2
    for i in range(4):
        try:
            
            button = browser.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span/span')
            button.click()
            time.sleep(0.1)
        except:
            print("Bypass")
    x, y = pyautogui.locateCenterOnScreen('submit.png')
    pyautogui.click(x, y)
    print("Submit")        
    time.sleep(1)
#browser.close()
