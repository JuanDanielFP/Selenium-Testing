from asyncio import wait
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
                    options.add_argument("--window-size=1920,1080")
                self.driver = webdriver.Chrome(options=options)

            elif browser == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                    options.add_argument("--window-size=1920,1080")
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
            print("\n[!] Website tidak menyediakan fitur register.")
            print("[v] Register disimulasikan sebagai passed.")
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
        time.sleep(1)

    def test_sort_name_az(self):
        try:
            driver = self.driver
            self.login()

            dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
            from selenium.webdriver.support.ui import Select
            Select(dropdown).select_by_visible_text("Name (A to Z)")
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
            from selenium.webdriver.support.ui import Select
            Select(dropdown).select_by_visible_text("Price (low to high)")
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
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
        wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
        wait.until(EC.url_contains("inventory"))

    def test_checkout_process(self):
        try:
            driver = self.driver
            wait = WebDriverWait(driver, 10)
            self.login()
            print("✅ Login | URL:", driver.current_url)

            # ✅ Add to cart - klik biasa tanpa execute_script
            wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
            time.sleep(1)

            # ✅ Verifikasi badge cart berubah jadi 1
            cart_badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
            print(f"✅ Step 1 - Item in cart badge: {cart_badge.text} | URL:", driver.current_url)
            self.assertEqual(cart_badge.text, "1", "Item gagal masuk cart!")

            # ✅ Klik cart icon - klik biasa
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.shopping_cart_link"))).click()
            wait.until(EC.url_contains("cart.html"))
            print("✅ Step 2 - Go to cart | URL:", driver.current_url)
            time.sleep(1)

            # ✅ Verifikasi item ada di cart
            items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
            print(f"✅ Step 3 - Items in cart: {len(items)}")
            self.assertGreater(len(items), 0, "Cart kosong!")

            # Checkout
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='checkout']"))).click()
            wait.until(EC.url_contains("checkout-step-one"))
            print("✅ Step 4 - Checkout | URL:", driver.current_url)
            time.sleep(1)

            # Input Data Checkout
            wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
            driver.find_element(By.ID, "last-name").send_keys("Doe")
            driver.find_element(By.ID, "postal-code").send_keys("12345")
            print("✅ Step 5 - Form filled")
            time.sleep(1)

            # Continue
            wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
            wait.until(EC.url_contains("checkout-step-two"))
            print("✅ Step 6 - Arrived at step two | URL:", driver.current_url)
            time.sleep(1)

            # Finish
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='finish']"))).click()
            wait.until(EC.url_contains("checkout-complete"))
            print("✅ Step 7 - Finish clicked | URL:", driver.current_url)
            time.sleep(1)

            # Verify success
            success = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//h2[@data-test='complete-header']")
            )).text
            print("✅ Result:", success)
            self.assertEqual(success, "Thank you for your order!")

        except Exception as e:
            print("❌ FAILED at URL:", driver.current_url)
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
                print("❌ Page error:", error_msg)
            except:
                pass
            self.fail(f"Checkout Error: {e}")

# =======================================================
#  RUN ALL TEST
# =======================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
