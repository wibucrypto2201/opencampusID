from selenium import webdriver as uc
from time import sleep
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import random
import csv
from random_username.generate import generate_username
from faker import Faker
import pycountry
from bs4 import BeautifulSoup
from simplegmail import Gmail
from simplegmail.query import construct_query

def getcode(email):
    # url = []
    gmail = Gmail()

    query_params = {
        "recipient": f"{email}",
    }
    messages = gmail.get_messages(query=construct_query(query_params))

    soup = BeautifulSoup(messages[0].html, 'html.parser')
    url  = soup.find_all("a")
    link = url[0]["href"].replace("&amp;", "&")
    return link


def load_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.readlines()
    proxies = [proxy.strip() for proxy in proxies]
    return proxies

def load_links(file_path):
    with open(file_path, "r") as file:
        links = file.readlines()
    links = [link.strip() for link in links]
    return links

def addchrome(proxy):
    global web

    ua = UserAgent()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    options = ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_extension("OKX.crx")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--enable-chrome-browser-cloud-management")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    options.add_argument('--disable-blink-features=AutomationControlled')  

    username, password_host_port = proxy.split('@')[0], proxy.split('@')[1]
    username, password = username.split(':')
    host, port = password_host_port.split(':')

    proxy_url = f"http://{username}:{password}@{host}:{port}"

    proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy_url)
    proxy_helper.enrich_chrome_options(options)

    web = uc.Chrome(chrome_options=options)
    current = web.current_window_handle

    max_attempts = 30
    attempts = 0
    while len(web.window_handles) < 3 and attempts < max_attempts:
        sleep(1)
        attempts += 1

    if len(web.window_handles) >= 3:
        web.switch_to.window(web.window_handles[-1])
        for handle in web.window_handles:
            if handle != current:
                web.switch_to.window(handle)
                web.close()
                sleep(0.5)

def task(private_keys, link_ref):
    web.switch_to.window(web.window_handles[0])
    web.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html#initialize/welcome")
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div[2]/button"
    ))).click()
    sleep(0.5)
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div"
    ))).click()
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]"
    ))).click()
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div/form/div[2]/div/textarea"
    ))).send_keys(private_keys)
    button = wait(web, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'okui-btn') and contains(@class, 'btn-lg') and contains(@class, 'btn-fill-highlight') and contains(@class, 'block') and not(contains(@class, 'btn-disabled')) and not(@disabled)]")))

    button.click()
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/button"
    ))).click()
    wait(web, 200).until(EC.presence_of_element_located((By.XPATH, 
    "//*[text()[contains(.,'Set password')]]")))
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[1]/div[2]/div/div/div/div/input"
    ))).send_keys("WibuCryto6996")
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div/div/div/input"
    ))).send_keys("WibuCryto6996")
    sleep(0.5)
    wait(web, 5).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[5]/div/div[2]/div/div/div/button"
    ))).click()
    wait(web, 10).until(EC.presence_of_element_located((By.XPATH, 
    "//*[text()[contains(.,'Set now')]]"))) 
    print("Import ví thành công")
    web.get(link_ref)
    wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
    "//*[text()[contains(.,'Create Your On-Chain')]]"))) 
    wait(web, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/main/div/div/div[2]/div[2]/div/div[4]/div/button",
            )
        )
    ).click()
    wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
    "//*[text()[contains(.,'Connect a Wallet')]]")))
    sleep(1)
    wait(web, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/button",
            )
        )
    ).click()
    max_attempts = 30
    attempts = 0
    while len(web.window_handles) < 2 and attempts < max_attempts:
        sleep(1)
        attempts += 1

    if len(web.window_handles) >= 2:
        web.switch_to.window(web.window_handles[-1])
        wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Connect account')]]"))) 
        sleep(1)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div/div/div[5]/div[2]/button[2]",
                )
            )
        ).click()
    sleep(0.5)
    web.close()
    web.switch_to.window(web.window_handles[0])
    wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
    "//*[text()[contains(.,'Verify your account')]]"))) 
    wait(web, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[3]/div/div/div[2]/div/div/div/div/div[2]/div[2]/button[1]",
            )
        )
    ).click()
    max_attempts = 30
    attempts = 0
    while len(web.window_handles) < 2 and attempts < max_attempts:
        sleep(1)
        attempts += 1

    if len(web.window_handles) >= 2:
        web.switch_to.window(web.window_handles[-1])
        wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Signature request')]]"))) 
        sleep(1)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div/div/div/div[5]/div/button[2]",
                )
            )
        ).click()
        sleep(0.5)
    web.switch_to.window(web.window_handles[0])
    try:
        try:
            wait(web, 6).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid Request')]")))
            raise Exception("Invalid Request xuất hiện!")
        except:
            pass
        wait(web, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Create your ID')]")))
        print("Connect ví thành công")
        EDU_ID =  str(generate_username(1)[0])[:6] + str(random.randrange(1, 999))
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Create your ID')]]"))) 
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/input",
                )
            )
        ).send_keys(EDU_ID)
        print("Tạo EDU ID",EDU_ID)
        sleep(2)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]",
                )
            )
        ).click()
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Referral code is valid')]]"))) 
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[1]/div[2]/div[3]/button",
                )
            )
        ).click()

        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Create your profile')]]"))) 

        fake = Faker()

        first_name = fake.first_name()
        last_name = fake.last_name()
        domains = ["@domain"]
        random_domain = random.choice(domains)
        email = EDU_ID.lower() + random_domain
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/input",
                )
            )
        ).send_keys(first_name)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]/input",
                )
            )
        ).send_keys(last_name)
        #email
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/input",
                )
            )
        ).send_keys(email)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/input",
                )
            )
        ).send_keys(email)
        print("Điền Firstname , Lastname và Email thành công")
        sleep(0.5)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[2]/div[2]/div[2]/div[3]/button[2]",
                )
            )
        ).click()
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Complete your profile')]]"))) 
        #country
        countries = list(pycountry.countries)
        random_country = random.choice(countries)
        element = web.execute_script(
            "return document.querySelector('#__next > div > div.AppLayout_content__KyXtM.AppLayout_withPadding__oXz4_ > main > div > div > div > div > div.OnboardingQuizzes_right__mNttS > div.Quiz_quiz__TPB_I.Quiz_active__32fPd > div.Quiz_wrapper__IAqa5 > div.Quiz_formGroup__v14Q2 > div:nth-child(1) > div.css-b62m3t-container > div')"
        )
        actions = ActionChains(web)
        actions.move_to_element(element).click().send_keys(random_country.name).perform()
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[2]/div/div/div[2]/div[2]/div/div",
                )
            )
        ).click()
        #Province
        element = web.execute_script(
            "return document.querySelector('#__next > div > div.AppLayout_content__KyXtM.AppLayout_withPadding__oXz4_ > main > div > div > div > div > div.OnboardingQuizzes_right__mNttS > div.Quiz_quiz__TPB_I.Quiz_active__32fPd > div.Quiz_wrapper__IAqa5 > div.Quiz_formGroup__v14Q2 > div:nth-child(2) > div.css-b62m3t-container > div')"
        )
        actions = ActionChains(web)
        actions.move_to_element(element).click().perform()
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[2]/div/div[2]/div[2]/div[2]/div/div",
                )
            )
        ).click()
        #City
        element = web.execute_script(
            "return document.querySelector('#__next > div > div.AppLayout_content__KyXtM.AppLayout_withPadding__oXz4_ > main > div > div > div > div > div.OnboardingQuizzes_right__mNttS > div.Quiz_quiz__TPB_I.Quiz_active__32fPd > div.Quiz_wrapper__IAqa5 > div.Quiz_formGroup__v14Q2 > div:nth-child(3) > div.css-b62m3t-container > div')"
        )
        actions = ActionChains(web)
        actions.move_to_element(element).click().perform()
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[3]/div[2]/div[2]/div/div",
                )
            )
        ).click()
        #Education
        element = web.execute_script(
            "return document.querySelector('#__next > div > div.AppLayout_content__KyXtM.AppLayout_withPadding__oXz4_ > main > div > div > div > div > div.OnboardingQuizzes_right__mNttS > div.Quiz_quiz__TPB_I.Quiz_active__32fPd > div.Quiz_wrapper__IAqa5 > div.Quiz_formGroup__v14Q2 > div.InputSelect_select__s_0PX > div.css-b62m3t-container > div')"
        )
        actions = ActionChains(web)
        actions.move_to_element(element).click().perform()
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[4]/div[2]/div[2]/div/div",
                )
            )
        ).click()
        #Primary
        element = web.execute_script(
            "return document.querySelector('#__next > div > div.AppLayout_content__KyXtM.AppLayout_withPadding__oXz4_ > main > div > div > div > div > div.OnboardingQuizzes_right__mNttS > div.Quiz_quiz__TPB_I.Quiz_active__32fPd > div.Quiz_wrapper__IAqa5 > div.Quiz_formGroup__v14Q2 > div:nth-child(5) > div.css-b62m3t-container > div')"
        )
        actions = ActionChains(web)
        actions.move_to_element(element).click().perform()
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[5]/div[2]/div[2]/div/div",
                )
            )
        ).click()
        #Second
        element = web.execute_script(
            "return document.querySelector('#__next > div > div.AppLayout_content__KyXtM.AppLayout_withPadding__oXz4_ > main > div > div > div > div > div.OnboardingQuizzes_right__mNttS > div.Quiz_quiz__TPB_I.Quiz_active__32fPd > div.Quiz_wrapper__IAqa5 > div.Quiz_formGroup__v14Q2 > div.LanguagesSelect_select__UuAc5.LanguagesSelect_multi__7eCxC')"
        )
        actions = ActionChains(web)
        actions.move_to_element(element).click().perform()
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[6]/div[2]/div[2]/div/div",
                )
            )
        ).click()
        sleep(0.5)
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div/div/div[2]/main/div/div/div/div/div[2]/div[3]/div[2]/div[3]/button[2]",
                )
            )
        ).click()
        print("Hoàn thành profile")
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Check your email')]]"))) 
        sleep(10)
        web.get(getcode(email))
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Email verified!')]]"))) 
        print("Verify mail thành công")
        web.get(link_ref)
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Refer a friend')]]"))) 
        print("REF Thành Công")
        for i in range(2, 12):
            xpath_selector = f"/html/body/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[{i}]/div[1]"
            # Chờ cho đến khi phần tử xuất hiện
            element = wait(web, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_selector))
            )
            
            # Lấy văn bản của phần tử
            text_content = element.text
            
            # Tạo link ref
            ref_link = f"https://auth.opencampus.xyz?ref={text_content}"
            
            # In ra link đã tạo
            fieldnames = ['privatekeys', 'ref', 'user', 'email']
            rows = [{'privatekeys': private_keys, 'ref': ref_link, 'user':EDU_ID, 'email':email}]
            with open('SuccessDATA.csv', 'a', encoding='UTF8', newline='') as f1:
                writer = csv.DictWriter(f1, fieldnames=fieldnames)
                writer.writerows(rows)


    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

    finally:
        # Đóng trình duyệt
        web.quit()

if __name__ == '__main__':
    proxy_file = "proxy.txt"
    proxies = load_proxies(proxy_file)
    
    while True:
        try:
            proxy = random.choice(proxies)
            addchrome(proxy)
            
            with open("private_keys.txt", "r+", encoding="utf-8") as pk_file, open("linkref.txt", "r+", encoding="utf-8") as link_file:
                pk_lines = pk_file.readlines()
                link_lines = link_file.readlines()
                
                if not pk_lines or not link_lines:
                    break  # Exit the loop if no more lines left in the file
                
                private_keys = pk_lines[0].strip()  # Process only the first line of private keys
                link_ref = link_lines[0].strip()  # Process only the first line of link refs

                try:
                    task(private_keys, link_ref)
                    with open("linkref.txt", "a", encoding="utf-8") as success_file:
                        success_file.write(f"{link_ref}\n")
                        link_file.seek(0)
                        link_file.writelines(link_lines[1:])
                        link_file.truncate()
                except Exception as e:
                    print(f"Error occurred: {e}")
                # Remove the processed key and link from their respective files
                pk_file.seek(0)
                pk_file.writelines(pk_lines[1:])
                pk_file.truncate()


        except Exception as e:
            print(f"Error occurred: {e}")
            web.quit()
