from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    def __init__(self, driver):                            
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)
 
    def click_parent_then_click(self, parent_locator, child_locator):
        children = self.driver.find_elements(*child_locator)

        print("jumlah child:", len(children))
        for i, c in enumerate(children):
            print(i, c.is_displayed(), c.is_enabled(), c.text)

        if not children or not children[0].is_displayed():
            parent = self.wait.until(
                EC.element_to_be_clickable(parent_locator)
            )
            parent.click()

        child = self.wait.until(
            EC.element_to_be_clickable(child_locator)
        )
        child.click()

    def buka_url_(self, url):                               
        self.driver.get(url)
    
    def verivikasi_url(self, url_keyword, timeout=10):      
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_keyword)
        )
        assert url_keyword in self.url_sekarang().lower()      
    
    def judul_halaman(self):                                
        return self.driver.title

    def url_sekarang(self):                                 
        return self.driver.current_url
    
    def click(self, locator):                              
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    
    def fill(self, locator, text):                         
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
    
    def get_txt(self, locator):                                                 
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text
    
    def pilih_dropdown(self, locator, nilai):            
        el = self.wait.until(EC.visibility_of_element_located(locator))
        Select(el).select_by_visible_text(nilai)
    
    def upload_file(self, locator, path_file):          
        el = self.wait.until(EC.presence_of_element_located(locator))
        el.send_keys(path_file)
    
    #cek elemen
    def is_visible(self, locator, timeout = 10):       
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
        
    def hitung_baris_tabel(self, locator):              #hitung jumlah baris/elemen yang cocok dengan locator berguna untuk verivkasi data di tabel
        return len(self.driver.find_elements(*locator))
    
    def ambil_semua_teks(self, locator):                #ambil semua elemen sekaligus berupa return list misal "admin", "user1", "user2"
        els = self.driver.find_elements(*locator)
        return [el.text for el in els]
    
    def scroll_ke_bawah(self):                          #scroll halaman sampai paling bawah
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)"
        )

    def screenshot(self, nama_file):                    #lakuin screenshot saat gagal dan simpan ke folder reports/
        self.driver.save_screenshot(f"reports/{nama_file}.png")

    def isi_tanggal(self, locator, tanggal):            #ini buat isi tanggalan
        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1]",
            element,
            tanggal
        )
#parent class dari semua page berisikan method umum yang dipakai semua halaman agar tidak menulis ulang kode yang sama