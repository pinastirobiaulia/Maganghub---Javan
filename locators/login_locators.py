from selenium.webdriver.common.by import By

class LoginLocators:
    INPUT_USERNAME = (By.ID, "username") 
    INPUT_PASSWORD = (By.ID, "password")   
    BTN_LOGIN      = (By.ID, "kc-login") 
    NOTIF_GAGAL    = (By.CSS_SELECTOR, "#kc-content-wrapper > div.mb-6.bg-red-50.text-red-700.border.border-red-200")
    FORGOT_PASSWORD         = (By.XPATH, "//a[normalize-space()='Forgot Password?']")
    INPUT_RESET_USERNAME    = (By.ID, "username")
    BTN_SUBMIT_RESET        = (By.ID, "kc-form-buttons")