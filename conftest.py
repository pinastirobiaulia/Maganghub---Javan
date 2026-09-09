import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import BASE_URL, IMPLICIT_WAIT, USERS

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome:", driver.capabilities["browserVersion"])
    print("ChromeDriver:", driver.capabilities["chrome"]["chromedriverVersion"])
        
    driver.implicitly_wait(IMPLICIT_WAIT)

    driver.get(BASE_URL)

    yield driver    
    driver.quit()   

# @pytest.fixture(scope="function")
# def login_as(driver):
#     from pages.login_page import LoginPage
#     from config.config import USERS

#     def _login(role):
#         login =LoginPage(driver)
#         login.buka_halaman()
#         login.login(
#             USERS[role]["email"],
#             USERS[role]["password"]
#         )
#         return driver
#     return _login


@pytest.fixture(autouse=False)
def reset_ke_beranda(request):
    yield

    nav = None

    if hasattr(request.instance, "nav"):
        nav = request.instance.nav
    elif hasattr(request.cls, "nav"):
        nav = request.cls.nav

    if nav:
        nav.go_to_dashboard()
        nav.verivikasi_url("beranda")
        
#ini untuk navigasi
@pytest.fixture(scope="class")
def driver_class(request):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome:", driver.capabilities["browserVersion"])
    print("ChromeDriver:", driver.capabilities["chrome"]["chromedriverVersion"])

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.maximize_window()
    driver.get(BASE_URL)

    request.cls.driver = driver

    yield driver

    driver.quit()

#LOGIN KHUSUS CLASS
@pytest.fixture(scope="class")
def login_as_class(driver_class):
    from pages.login_page import LoginPage
    from config.config import USERS

    def _login(role):
        login = LoginPage(driver_class)
        login.buka_halaman()
        login.login(
            USERS[role]["username"],
            USERS[role]["password"]
        )
        return driver_class

    return _login