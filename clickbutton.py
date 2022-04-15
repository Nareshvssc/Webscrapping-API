#import driver_launcher
from selenium.webdriver.common.action_chains import ActionChains

def click_button(driver_mod,button_to_click):
        #driver = driver_launcher.driver_launchfun(driver_url)
        action = ActionChains(driver_mod)
        action.click(button_to_click)
        action.perform()
        return driver_mod

def no_click(driver_mod):
        return driver_mod