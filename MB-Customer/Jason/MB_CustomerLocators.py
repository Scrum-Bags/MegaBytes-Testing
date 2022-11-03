from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class MB_Customer_Login_Objects(object):
    #objects on login page
    By_username_field = (By.XPATH, "//*[@id='mat-input-0']")
    By_password_field = (By.XPATH, "//*[@id='mat-input-1']")
    By_sign_in = (By.XPATH, "/html/body/app-root/app-login/div/div/mat-card/mat-card-content/div/button")
    By_register_link = (By.XPATH, "/html/body/app-root/app-header/nav/ul/li[1]/button")


class MB_Customer_Home_Objects(object):
    #Page menu
    By_signout = (By.XPATH, "/html/body/app-root/app-header/nav/ul/li[4]/button")


