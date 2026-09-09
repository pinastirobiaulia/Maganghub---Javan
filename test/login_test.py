import pytest
from pages.login_page import LoginPage
from config.config import USERS, URLS
#untuk menunggu buka halaman beranda
from selenium.webdriver.support.wait import WebDriverWait      
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = LoginPage(driver)
        self.page.buka_halaman()
    
    def test_login_berhasil(self):
        self.page.login(
            USERS["userb"]["username"],
            USERS["userb"]["password"]
        )
        WebDriverWait(self.page.driver, 15).until(
            EC.url_contains("app.alurkerja.com")
        )
        assert URLS["beranda"] in self.page.url_sekarang()

    def test_login_username_salah(self):
        """Login dengan email yang salah akan muncul pesan eror"""
        self.page.login("pinasti@gmail.com", "Ainun5678")
        assert self.page.notifikasi_gagal_visible() or \
        URLS["login"] in self.page.url_sekarang()

    def test_login_password_salah(self):
        """Login dengan password yang salah akan muncul pesan eror"""
        self.page.login("pinasti@gmail.com", "Ainun123")
        assert self.page.notifikasi_gagal_visible(), \
        "Harus muncul pesan eror jika password salah"

    def test_login_username_kosong(self):
        """Login tanpa password -> form tidak tersubmit"""
        self.page.login("", "Ainun5678")
        assert self.page.notifikasi_gagal_visible() or \
        URLS["login"] in self.page.url_sekarang()

    def test_login_password_kosong(self):
        """Login tanpa password -> form tidak tersubmit"""
        self.page.login("pinastiaul@gmail.com", "")
        assert self.page.notifikasi_gagal_visible() or \
        URLS["login"] in self.page.url_sekarang()

    def test_login_username_format_salah(self):
        """Login dengan email format salah dan password valid -> user tidak dapat login"""
        username_invalid = [
            "pinastiaulgmail.com",          #tanpa @
            "pinastiaul@",                  #tanpa domain
            "@gmail.com",                   #tanpa admin
            "pinasti@gmail",                #tanpa TLD
            "pinasti aul@gmail.com"         #pakai spasi
        ]

        for username in username_invalid:
            self.page.buka_halaman()    #reset halaman setiap iterasi
            self.page.login(username, "Ainun5678")
            assert self.page.notifikasi_gagal_visible() or \
            URLS["login"] in self.page.url_sekarang(), \
            f"Gagal login dengan email: {username}"

    def test_login_usernamepass_kosong(self):
        """Login tanpa email dan password-> form tidak tersubmit"""
        self.page.login("", "")
        assert self.page.notifikasi_gagal_visible() or \
        URLS["login"] in self.page.url_sekarang()

    def test_forgot_password(self):
        self.page.request_reset_password(
            USERS["userb"]["username"]
        )