from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class MB_Driver_Login_Objects(object):
    #objects on login page
    By_username_field = (By.NAME, "username")
    By_password_field = (By.NAME, "password")
    By_sign_in = (By.XPATH, "//*[@id='root']/div/div[2]/div/form/button")
    By_forgot_password_link = (By.LINK_TEXT, "/forgotPassword")
    By_sign_up_link = (By.LINK_TEXT, "/signUp")
    #By_sign_in_error = (By.ID, "LoginError")


class MB_Driver_Home_Objects(object):
    #Page menu
    By_menu_dropdown = (By.ID, "//*[@id='root']/div/div[2]/header/div/div/div/button[1]")
    By_home_link = (By.XPATH, "//*[@id='menu-appbar']/div[3]/ul/li[1]")
    By_available_orders_link = (By.XPATH, "//*[@id='menu-appbar']/div[3]/ul/li[2]")
    By_current_orders_link = (By.XPATH, "//*[@id='menu-appbar']/div[3]/ul/li[3]")
    #User menu
    By_user_dropdown = (By.XPATH, "//*[@id='root']/div/div[2]/header/div/div/div/button[2]")
    By_profile_link = (By.XPATH, "//*[@id='profile-menu-appbar']/div[3]/ul/li[1]")
    By_signout = (By.XPATH, "//*[@id='profile-menu-appbar']/div[3]/ul/li[2]")


