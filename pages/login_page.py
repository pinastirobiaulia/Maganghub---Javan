from pages.base_page import BasePage
from locators.login_locators import LoginLocators as L
from config.config import URLS

class LoginPage(BasePage):
    def buka_halaman(self):
        self.buka_url_(URLS["login"])
    
    def login(self, username, password):
        self.fill(L.INPUT_USERNAME, username)
        self.fill(L.INPUT_PASSWORD, password)
        self.click(L.BTN_LOGIN)

    def notifikasi_gagal_visible(self):
        return self.is_visible(L.NOTIF_GAGAL, timeout=2)

    def request_reset_password(self, username):
        self.click(L.FORGOT_PASSWORD)
        self.fill(L.INPUT_RESET_USERNAME, username)
        self.click(L.BTN_SUBMIT_RESET)