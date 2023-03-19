from selenium import webdriver
import time
from pyautogui import write

option = webdriver.ChromeOptions()
option.add_argument("-incognito")
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

for j in range(len(email)):
    browser = webdriver.Chrome(executable_path="C:\\Users\\USER\Desktop\\scrapdata\\chromedriver.exe", options=option)

    browser.get('https://docs.google.com/forms/d/e/1FAIpQLSeG6MLgdIsFkVuLU4I97CF74_NHVNT3ArC-HhqekkfICFqORg/viewform')

    textboxes = browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")

    checkboxes = browser.find_elements_by_class_name("quantumWizTogglePapercheckboxInnerBox")
    submit=browser.find_element_by_class_name("appsMaterialWizButtonPaperbuttonContent")

    #Page 1
    textboxes[0].send_keys(email[j])
    time.sleep(0.5)
    checkboxes[0].click()
    time.sleep(0.5)
    browser.find_element_by_class_name("quantumWizMenuPaperselectOptionList").click()
    time.sleep(0.5)
    option_number = int(gender[j])
    for _ in range(option_number):
        write(['down'])
    write(['enter'])

    textboxes[1].send_keys(name[j])
    textboxes[2].send_keys(address[j])
    textboxes[3].send_keys(number[j])
    submit.click()



    #Page 2
    checkboxes = browser.find_elements_by_class_name("quantumWizTogglePapercheckboxInnerBox")
    time.sleep(0.1)
    checkboxes[0].click()
   

    #Page 3
    button = browser.find_element_by_xpath("/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div[2]/span")
    button.click()
    radio_buttons = browser.find_elements_by_class_name("appsMaterialWizToggleRadiogroupOffRadio")
    radio_buttons[int(biddertype[j])].click()
    button = browser.find_element_by_xpath("/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div[2]/span")
    button.click()

    #Page 4
    time.sleep(0.5)
    browser.find_element_by_class_name("quantumWizMenuPaperselectOptionList").click()
    time.sleep(0.5)
    option_number = int(carselect[j])
    for _ in range(option_number):
        write(['down'])
    write(['enter'])

    textboxes = browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")
    textboxes[1].send_keys(platenumber[j])

    button = browser.find_element_by_xpath("/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div[2]/span")
    button.click()

    browser.close()
