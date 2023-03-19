import webbrowser
import pyautogui
import time
for i in range(2):
    url = 'https://docs.google.com/forms/d/e/1FAIpQLSeG6MLgdIsFkVuLU4I97CF74_NHVNT3ArC-HhqekkfICFqORg/viewform?usp=pp_url&emailAddress=xypher@gmail.com&entry.23249824=Yes&entry.1882979912=Male&entry.1447596059=a&entry.411635796=a&entry.216445732=a&entry.892874713=I+agree&entry.1683885721=Individual&entry.441696145=Car+1&entry.1266154365=lot123'
    webbrowser.register('chrome',
            None,
            webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(url)
    time.sleep(0.5)
    pyautogui.click(500, 500)
   
    flag=0
    while flag==0:
        pyautogui.scroll(-10000)
        try:
            x, y = pyautogui.locateCenterOnScreen('next.png', grayscale=True, confidence=0.7)
            pyautogui.click(x, y)
        except:
            print("Next not found")
        time.sleep(0.05)
        try:
                
                x, y = pyautogui.locateCenterOnScreen('submit.png', grayscale=True, confidence=0.7)
                pyautogui.click(x, y)
                flag=1
        except:
                print("Submit not found")
    time.sleep(1)     
    #pyautogui.keyDown('ctrl')
    #pyautogui.press('w')
    #pyautogui.keyUp('ctrl')
    
