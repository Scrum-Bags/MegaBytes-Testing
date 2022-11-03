from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class MB_Admin_Login_Objects(object):
    #objects on login page
    By_username_field = (By.NAME, "username")
    By_password_field = (By.NAME, "password")
    By_sign_in = (By.XPATH, "//*[@id='root']/div/div/div/form/button")
    By_forgot_password_link = (By.LINK_TEXT, "/forgotPassword")


class MB_Admin_Home_Objects(object):
    #Page menu
    By_signout = (By.XPATH, "//*[@id='root']/div/div/div[1]/button[3]")


