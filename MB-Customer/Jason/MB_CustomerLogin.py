from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from MB_CustomerLocators import MB_Customer_Login_Objects
from MB_CustomerLocators import MB_Customer_Home_Objects
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import string
import time

#https://selenium-python.readthedocs.io/getting-started.html#simple-usage

class MB_CustomerLogin():


    def __init__(self, driver = "default"):

        if(driver=="default"):
            self.driver = webdriver.Chrome()
        else:
            self.driver = driver


    def Launch_Login_Page(self):
        self.driver.get("http://megabytes-customer-frontend.s3-website-us-east-1.amazonaws.com/login")


    def login(self, reporter, ssPath, username, password):
        print("***Logging into MegaBytes Customer's Page***")
        driver = self.driver
        #wait for page to load
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((MB_Customer_Login_Objects.By_username_field)))
        #set username field
        userFieldObj = driver.find_element(*MB_Customer_Login_Objects.By_username_field)
        userFieldObj.send_keys(username)
        if userFieldObj.get_attribute('value') == username:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username successfully placed in dialog box",True,"username = " + username, userFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username successfully placed in dialog box")
        else:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username not place in dialog box",False,"username = " + username, userFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username not place in dialog box")
            print("Stopping test")
            return
        #set password field
        passwordFieldObj = driver.find_element(*MB_Customer_Login_Objects.By_password_field)
        passwordFieldObj.send_keys(password)
        if passwordFieldObj.get_attribute('value') == password:
            reporter.reportStep("Put password in dialog box","Password should appear in the dialog box","Password successfully placed in dialog box",True,"", passwordFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password successfully placed in dialog box")
        else:
            reporter.reportStep("Put password in dialog box","Password should appear in the dialog box","Password not place in dialog box",False,"", passwordFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password not place in dialog box")
            print("Stopping test")
            return
        #click sign in button
        signinObj = driver.find_element(*MB_Customer_Login_Objects.By_sign_in)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*MB_Customer_Login_Objects.By_sign_in))
        time.sleep(1)
        signinObj.click()

        print("Clicking sign in button")
        #wait for login to load
        try:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((MB_Customer_Home_Objects.By_signout)))
            reporter.reportStep("Press submit and login","Customer dashboard should appear","Login successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Login successful")
        except:
            reporter.reportStep("Press submit and login","Customer dashboard should appear","Login unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Login unsuccessful")
            return
        self.username=username
        self.password=password

    def logout(self, reporter, ssPath):
        driver = self.driver
        #click sidebar in case of responsiveness
        error = ""
        located = False
        print("Looking for logout button button")
        if len(driver.find_elements(*MB_Customer_Home_Objects.By_signout))>0:
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((MB_Customer_Home_Objects.By_signout)))
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*MB_Customer_Home_Objects.By_signout))
                time.sleep(1)
                located = True
                print("Logout button located")
            except Exception as e:
                #print(e)
                #error = e
                print("Logout button not located")
                pass     
            
        #check for existence of setting dropdown required to click signout button
        if located:
            #driver.find_element(*MB_Admin_Home_Objects.By_settings_menu).click()
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((MB_Customer_Home_Objects.By_signout)))
            #time.sleep(1)
            try:
                driver.find_element(*MB_Customer_Home_Objects.By_signout).click()
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MB_Customer_Login_Objects.By_username_field)))
            except:
                pass
            #check for login page objects to confirm signout success
            if len(driver.find_elements(*MB_Customer_Login_Objects.By_username_field))>0:
                reporter.reportStep("Press logout button","Login page should appear","Logout successful",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Logout successful")
            else:
                reporter.reportStep("Press logout button","Login page should appear","Logout unsuccessful",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Logout unsuccessful, forced navigation required")
                driver.get("http://megabytes-customer-frontend.s3-website-us-east-1.amazonaws.com/login")
        else:
            reporter.reportStep("Press logout button","Login page should appear","Unable to locate logout button",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            driver.get("http://megabytes-customer-frontend.s3-website-us-east-1.amazonaws.com/login")
            print("Logout unsuccessful, forced navigation required")
        self.username=""
        self.password=""


    def bad_login(self, reporter, ssPath, username, password):
        driver = self.driver

        if username is None:
            username = ""
        if password is None:
            password = ""


        print("***Logging into MegaBytes Customer's Page - Negative Testing***")

        #wait for page to load
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((MB_Customer_Login_Objects.By_username_field)))
        #set username field
        userFieldObj = driver.find_element(*MB_Customer_Login_Objects.By_username_field)
        userFieldObj.send_keys(username)
        if userFieldObj.get_attribute('value') == username:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username successfully placed in dialog box",True,"username = " + username, userFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username successfully placed in dialog box")
        else:
            reporter.reportStep("Put username in dialog box","Username should appear in the dialog box","Username not place in dialog box",False,"username = " + username, userFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Username not placed in dialog box")
        #set password field
        passwordFieldObj = driver.find_element(*MB_Customer_Login_Objects.By_password_field)
        passwordFieldObj.send_keys(password)
        if passwordFieldObj.get_attribute('value') == password:
            reporter.reportStep("Put password in dialog box","Password should appear in the dialog box","Password successfully placed in dialog box",True,"", passwordFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password successfully placed in dialog box")
        else:
            reporter.reportStep("Put password in dialog box","Password should appear in the dialog box","Password not place in dialog box",False,"", passwordFieldObj.screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            print("Password not placed in dialog box")
        #click sign in button

        signinObj = driver.find_element(*MB_Customer_Login_Objects.By_sign_in)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(*MB_Customer_Login_Objects.By_sign_in))
        time.sleep(1)
        signinObj.click()

        print("Clicking sign in button")
        #wait for error to load
        if username=="" or password=="":
            time.sleep(1)
            try:  
                #WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((MB_Customer_Login_Objects.By_sign_in_error), "Please enter credentials."))
                reporter.reportStep("Press submit and login","A login error should appear","Login unsuccessful and an error appeared",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
            except:
                reporter.reportStep("Press submit and login","A login error should appear","Login error did not appear",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("No error message appeared")
        else:
            try:
                WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((MB_Customer_Login_Objects.By_sign_in_error), "Invalid Credentials"))
                reporter.reportStep("Press submit and login","A login error should appear","Login unsuccessful and an error appeared",True,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("Login error detected - Invalid Credentials")
            except:
                reporter.reportStep("Press submit and login","A login error should appear","Login error did not appear",False,"", driver.find_element(By.TAG_NAME, "body").screenshot, ssPath + ''.join(random.choices(string.ascii_lowercase, k=20)))
                print("No error message appeared")
                return
        
