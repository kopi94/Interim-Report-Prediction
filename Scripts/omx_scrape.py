from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.options import Options


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": r"C:\Users\patri\Desktop\Python\AtomPython\SEB",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True,
  "download_restrictions": 3,
})


with webdriver.Chrome("C:/Users/patri/Desktop/Python/AtomPython/chromedriver.exe", chrome_options=options) as driver:
    try:


        wait = WebDriverWait(driver, 10)
        driver.get("http://www.nasdaqomxnordic.com/nyheter/foretagsmeddelanden")
        wait1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='market']/option[text()='Nasdaq Stockholm']")))
        driver.find_element_by_xpath("//select[@id='market']/option[text()='Nasdaq Stockholm']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//select[@id='categories']/option[@title='Interimsrapport']").click()
        driver.find_element_by_xpath("//input[@id='FromDate']").send_keys('2019-01-01')
        driver.find_element_by_xpath("//input[@id='ToDate']").send_keys('2019-12-31')
        driver.find_element_by_xpath("//div[@id='newsSearchButton']").click()

        elems = []
        company = []
        time_stamp = []
        news = []

        try:
            results = driver.find_element_by_id("data")
            results = results.find_elements_by_tag_name("a")
            table = driver.find_element_by_id("data").find_elements_by_tag_name("tr")
            for tr in table:
                td = tr.find_elements_by_tag_name("td")
                link = td[3].find_element_by_tag_name("a").get_attribute("href")
                if "viewDisclosure" in link and link not in elems and "lang=en" in link:
                    company.append(td[1].text)
                    time_stamp.append(td[0].text)
                    elems.append(link)


        except:
            results = driver.find_element_by_id("data")
            results = results.find_elements_by_tag_name("a")
            table = driver.find_element_by_id("data").find_elements_by_tag_name("tr")
            for tr in table:
                td = tr.find_elements_by_tag_name("td")
                link = td[3].find_element_by_tag_name("a").get_attribute("href")
                if "viewDisclosure" in link and link not in elems and "lang=en" in link:
                    company.append(td[1].text)
                    time_stamp.append(td[0].text)
                    elems.append(link)

        el = driver.find_element_by_xpath("//div[@class='prevNext']/a[text()='Nästa']")
        ActionChains(driver).move_to_element(el).click(el).perform()
        elm = driver.find_element_by_tag_name("html")
        elm.send_keys(Keys.END)


        while len(driver.find_element_by_id("data").find_elements_by_tag_name("a")) > 0:
            time.sleep(1)
            try:
                results = driver.find_element_by_id("data")
                results = results.find_elements_by_tag_name("a")
                table = driver.find_element_by_id("data").find_elements_by_tag_name("tr")
                for tr in table:
                    td = tr.find_elements_by_tag_name("td")
                    link = td[3].find_element_by_tag_name("a").get_attribute("href")
                    if "viewDisclosure" in link and link not in elems and "lang=en" in link:
                        company.append(td[1].text)
                        time_stamp.append(td[0].text)
                        elems.append(link)
            except:
                results = driver.find_element_by_id("data")
                results = results.find_elements_by_tag_name("a")
                table = driver.find_element_by_id("data").find_elements_by_tag_name("tr")
                for tr in table:
                    td = tr.find_elements_by_tag_name("td")
                    link = td[3].find_element_by_tag_name("a").get_attribute("href")
                    if "viewDisclosure" in link and link not in elems and "lang=en" in link:
                        company.append(td[1].text)
                        time_stamp.append(td[0].text)
                        elems.append(link)

            el = driver.find_element_by_xpath("//div[@class='prevNext']/a[text()='Nästa']")
            driver.execute_script("arguments[0].scrollIntoView();", el)
            ActionChains(driver).move_to_element(el).click(el).perform()
            wait1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='market']/option[text()='Nasdaq Stockholm']")))




        rows = []
        counter = 0

        for i in elems:
            driver.get(i)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='previewTable']")))
            try:
                txt = driver.find_element_by_xpath("//table[@id='previewTable']").find_elements_by_tag_name("tr")[1].text
                txt = txt.replace("\n", "")
                txt = txt.replace(";", "")
            except:
                print(i)
                txt = "empty"
            news.append(txt)

    
            if counter % 100 == 0 and counter != 0:
                cols = ["Company", "TimeStamp", "News"]
                df = pd.DataFrame({"Company" : company[:counter],
                                    "TimeStamp": time_stamp[:counter],
                                    "News": news[:counter]
                })
                df.to_csv(f"C:/Users/patri/Desktop/Python/AtomPython/SEB/Data/{counter}.csv", index=False)
            counter += 1
        cols = ["Company", "TimeStamp", "News"]
        df = pd.DataFrame({"Company" : company,
                            "TimeStamp": time_stamp,
                            "News": news
        })

        df.to_csv("C:/Users/patri/Desktop/Python/AtomPython/SEB/Data/News.csv", index=False)
    finally:

        driver.close()
