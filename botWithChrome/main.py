import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


from tkinter import *
from tkinter import messagebox
# ######################################################################
username = ''  # fill your user name here
password = ''  # fill your password here
timeee = ''
# # ######################################################################
def login():
    username = entry1.get()
    password = entry2.get()
    timeee = entry3.get()
    root.quit()

root = Tk()
root.title("Shitty")
root.geometry("300x900")

global entry1
global entry2
global entry3
Label(root, text="Username").place(x=20, y=20)
Label(root, text="Password").place(x=20, y=70)
Label(root, text="Time").place(x=20, y=100)

entry1 = Entry(root,bd=5)
entry1.place(x=140,y=20)

entry2 = Entry(root,bd=5)
entry2.place(x=140,y=70)

entry3 = Entry(root,bd=5)
entry3.place(x=140,y=100)

# ################################################
entry4 = Entry(root,bd=5)
entry4.place(x=140,y=200)
entry5 = Entry(root,bd=5)
entry5.place(x=140,y=220)
entry6 = Entry(root,bd=5)
entry6.place(x=140,y=240)
entry7 = Entry(root,bd=5)
entry7.place(x=140,y=260)
entry8 = Entry(root,bd=5)
entry8.place(x=140,y=280)
entry9 = Entry(root,bd=5)
entry9.place(x=140,y=300)
entry10 = Entry(root,bd=5)
entry10.place(x=140,y=320)
entry11 = Entry(root,bd=5)
entry11.place(x=140,y=340)
entry12 = Entry(root,bd=5)
entry12.place(x=140,y=360)
entry13 = Entry(root,bd=5)
entry13.place(x=140,y=380)


################################################
Button(root,text="Login",command=login,height=3,width=13,bd=6).place(x=100,y=130)
root.mainloop()


#

# browser = webdriver.Chrome(executable_path="C:\\Users\\king\\PycharmProjects\\shittyChrome\\chromedriver.exe")
# browser = webdriver.Chrome(executable_path=r"C:\Users\king\PycharmProjects\shittyChrome\chromedriver.exe")
browser = webdriver.Chrome()
#
browser.get("https://banweb.cityu.edu.hk/pls/PROD/twgkpswd_cityu.P_WWWLogin")
try:
    element = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input")),
        ec.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[2]/div[2]/span/input")),
    )
finally:
    x = 1

browser.find_element(by=By.XPATH,
                     value='/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').send_keys(
    entry1.get())
browser.find_element(by=By.XPATH,
                     value='/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[2]/div[2]/span/input').send_keys(
    entry2.get())
browser.find_element(by=By.XPATH, value='/html/body/div[2]/main/div[2]/div/div/form/div[2]/input').click()
time.sleep(5)

try:
    element = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/form/button")),
    )
finally:
    print('REq')

try:
    browser.find_element(by=By.XPATH,value='/html/body/div[5]/form/button').click()
finally:
    print('')

try:
    element = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, "/html/body/div[3]/span/map/table/tbody/tr[1]/td/table/tbody/tr/td[5]/a")),
    )
finally:
    x = "add"


try:
    browser.find_element(by=By.XPATH,
                         value='/html/body/div[3]/span/map/table/tbody/tr[1]/td/table/tbody/tr/td[5]/a').click()  # course registration
    time.sleep(1)
    browser.find_element(by=By.XPATH,
                         value='/html/body/div[5]/table[1]/tbody/tr[5]/td[2]/a').click()  # Main Menu For add drop
    time.sleep(1)
    browser.find_element(by=By.XPATH,
                         value='/html/body/div[5]/table[1]/tbody/tr[2]/td[2]/a').click()  # add or drop classes
    time.sleep(1)
finally:
    print('Waiting For Refresh')


while True:
    x = 'add'
    if x == 'add':
        currentTime = False
        while not currentTime:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            if current_time == entry3.get():
                currentTime = True
    browser.find_element(by=By.XPATH, value='/html/body/div[5]/form/input').click()  # select semester
    try:
        element = WebDriverWait(browser, 10).until(
            ec.presence_of_element_located(
                (By.ID, "crn_id1")),
        )
    finally:
        x = 1

    browser.find_element(by=By.ID,
                         value='crn_id1').send_keys(entry4.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id2').send_keys(entry5.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id3').send_keys(entry6.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id4').send_keys(entry7.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id5').send_keys(entry8.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id6').send_keys(entry9.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id7').send_keys(entry10.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id8').send_keys(entry11.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id9').send_keys(entry12.get())  # send to box1
    browser.find_element(by=By.ID,
                         value='crn_id10').send_keys(entry13.get())  # send to box1

    browser.find_element(by=By.XPATH, value='/html/body/div[5]/form/input[19]').click()  # submit

# # browser.find_element(by=By.XPATH, value='/html/body/div[5]/form/table[1]/tbody/tr[3]/td[2]/select/option[2]').click() #web drop for the second row
# # browser.find_element(by=By.XPATH, value='/html/body/div[5]/form/table[1]/tbody/tr[2]/td[2]/select/option[2]').click() #web drop for the first row
#
#         # try:
#         #
#         # except:
#         #     while True:
#         #         browser.refresh()
#         #         try:
#         #             element = WebDriverWait(browser, 10).until(
#         #                 ec.presence_of_element_located(
#         #                     (By.XPATH, "/html/body/div[5]/form/table[3]/tbody/tr[2]/td[1]/input[2]")),
#         #             )
#         #         finally:
#         #             x = 1
#         #         browser.find_element(by=By.XPATH,
#         #                              value='/html/body/div[5]/form/table[5]/tbody/tr[2]/td[1]/input[2]').send_keys(
#         #             '10241')
#         #         browser.find_element(by=By.XPATH, value='/html/body/div[5]/form/input[19]').click()
