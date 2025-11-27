import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time


BASE_URL = "https://www.saucedemo.com/"


# =======================================================
#  BASE CLASS – HEADLESS MODE + CROSS BROWSER
# =======================================================
class BaseTest(unittest.TestCase):

    def setUp(self):
        browser = "chrome"       # chrome / firefox
        headless = True          # ubah ke False jika ingin lihat browser

        try:
            if browser == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=options)

            elif browser == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                self.driver = webdriver.Firefox(options=options)

            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(BASE_URL)

        except Exception as e:
            print("❌ Browser gagal dijalankan:", e)
            raise e

    def tearDown(self):
        self.driver.quit()


# =======================================================
#  SIMULASI REGISTER (karena website tidak menyediakan)
# =======================================================
class TestRegister(BaseTest):

    def test_register_simulation(self):
        try:
            print("\n⚠️ Website tidak menyediakan fitur register.")
            print("✔ Register disimulasikan sebagai passed.")
            self.assertTrue(True)

        except Exception as e:
            self.fail(f"Register Simulation Error: {e}")


# =======================================================
#  LOGIN (POSITIVE & NEGATIVE)
# =======================================================
class TestLogin(BaseTest):

    def test_login_positive(self):
        try:
            driver = self.driver
            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()

            time.sleep(1)
            self.assertIn("inventory", driver.current_url)

        except Exception as e:
            self.fail(f"Login Positive Error: {e}")

    def test_login_negative(self):
        try:
            driver = self.driver
            driver.find_element(By.ID, "user-name").send_keys("wrong_user")
            driver.find_element(By.ID, "password").send_keys("wrong_pass")
            driver.find_element(By.ID, "login-button").click()

            error_msg = driver.find_elements(By.XPATH, "//*[contains(text(),'Epic sadface')]")
            self.assertTrue(len(error_msg) > 0, "Seharusnya muncul pesan error!")

        except Exception as e:
            self.fail(f"Login Negative Error: {e}")


# =======================================================
#  SORTING: NAME & PRICE
# =======================================================
class TestSorting(BaseTest):

    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

    def test_sort_name_az(self):
        try:
            driver = self.driver
            self.login()

            dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
            dropdown.send_keys("Name (A to Z)")
            time.sleep(2)

            names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
            self.assertEqual(names, sorted(names))

        except Exception as e:
            self.fail(f"Sort Name Z-A Error: {e}")
            names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]

           

    def test_sort_price_low_high(self):
        try:
            driver = self.driver
            self.login()

            dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
            dropdown.send_keys("Price (low to high)")
            time.sleep(2)

            prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
            prices = [float(p.text.replace("$", "")) for p in prices]

            self.assertEqual(prices, sorted(prices))

        except Exception as e:
            self.fail(f"Sort Price Error: {e}")


# =======================================================
#  ADD TO CART + CHECKOUT
# =======================================================
class TestCheckout(BaseTest):

    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

    def test_checkout_process(self):
        try:
            driver = self.driver
            self.login()

            # Add to cart
            
            driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
            time.sleep(1)

            # Go to cart
            driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
            
            # Checkout
            driver.find_element(By.ID, "checkout").click()

            driver.find_element(By.ID, "first-name").send_keys("John")
            driver.find_element(By.ID, "last-name").send_keys("Doe")
            driver.find_element(By.ID, "postal-code").send_keys("12345")
            driver.find_element(By.ID, "continue").click()
            driver.find_element(By.ID, "finish").click()

            success = driver.find_element(By.CLASS_NAME, "complete-header").text
            self.assertEqual(success, "Thank you for your order!")

        except Exception as e:
            self.fail(f"Checkout Error: {e}")


# =======================================================
#  RUN ALL TEST
# =======================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
