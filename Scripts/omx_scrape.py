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

# chrome_options = Options()
#
# print(help(chrome_options))
#
# # this is the preference we're passing
# prefs = {'profile.default_content_setting_values.automatic_downloads': 0}
# chrome_options.add_experimental_option("prefs", prefs)
#

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
        # elm = driver.find_element_by_tag_name("html")
        # elm.send_keys(Keys.END)
        # time.sleep(10)
        # wait1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "matchFixtureContainer")))
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

            # for i in results:
            #     if "viewDisclosure" in i.get_attribute("href") and i.get_attribute("href") not in elems and "lang=en" in i.get_attribute("href"):
            #         elems.append(i.get_attribute("href"))
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



    #     for el in results:
    #         link = el.find_element_by_tag_name("div").get_attribute("data-href")
    #         link = "https:" + link
    #         elems.append(link)
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

    #         home = driver.find_element_by_class_name("scoreboxContainer").find_elements_by_class_name("long")[0].text
    #         away = driver.find_element_by_class_name("scoreboxContainer").find_elements_by_class_name("long")[1].text
    #         if "United" in home:
    #             home = home.replace("United", "Utd")
    #         if "United" in away:
    #             away = away.replace("United", "Utd")
    #         if "Leicester" in home:
    #             home = "Leicester"
    #         if "Leicester" in away:
    #             away = "Leicester"
    #         if "Manchester" in home:
    #             home = home.replace("Manchester", "Man")
    #         if "Manchester" in away:
    #             away = away.replace("Manchester", "Man")
    #         if "Hotspur" in home:
    #             home = "Spurs"
    #         if "Hotspur" in away:
    #             away = "Spurs"
    #         if "Wanderers" in home:
    #             home = "Wolves"
    #         if "Wanderers" in away:
    #             away = "Wolves"
    #         if "Newcastle" in home:
    #             home = "Newcastle"
    #         if "Newcastle" in away:
    #             away = "Newcastle"
    #         if "Brighton" in home:
    #             home = "Brighton"
    #         if "Brighton" in away:
    #             away = "Brighton"
    #         if "West Ham" in home:
    #             home = "West Ham"
    #         if "West Ham" in away:
    #             away = "West Ham"
    #         if "Norwich" in home:
    #             home = "Norwich"
    #         if "Norwich" in away:
    #             away = "Norwich"
    #         if "Huddersfield" in home:
    #             home = "Huddersfield"
    #         if "Huddersfield" in away:
    #             away = "Huddersfield"
    #         if "Cardiff" in home:
    #             home = "Cardiff"
    #         if "Cardiff" in away:
    #             away = "Cardiff"
    #         if "Stoke City" in home:
    #             home = "Stoke"
    #         if "Stoke City" in away:
    #             away = "Stoke"
    #         if "Swansea City" in home:
    #             home = "Swansea"
    #         if "Swansea City" in away:
    #             away = "Swansea"
    #         if "West Bromwich Albion" in home:
    #             home = "West Brom"
    #         if "West Bromwich Albion" in away:
    #             away = "West Brom"
    #         if "Hull City" in home:
    #             home = "Hull"
    #         if "Hull City" in away:
    #             away = "Hull"
    #         if "Norwich City" in home:
    #             home = "Norwich"
    #         if "Norwich City" in away:
    #             away = "Norwich"
    #         if "Queens Park Rangers" in home:
    #             home = "QPR"
    #         if "Queens Park Rangers" in away:
    #             away = "QPR"
    #
    #         home_score = driver.find_element_by_css_selector(".score.fullTime").text.split("-")[0]
    #         away_score = driver.find_element_by_css_selector(".score.fullTime").text.split("-")[1]
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "matchCentreSquadLabelContainer")))
    #         try:
    #             driver.find_element_by_class_name("matchCentreSquadLabelContainer").click()
    #         except:
    #             print("Except")
    #             continue
    #         try:
    #             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "matchLineupTeamContainer")))
    #         except:
    #             print("except")
    #             continue
    #
    #
    #         teams = driver.find_elements_by_class_name("matchLineupTeamContainer")
    #         players = teams[0].find_elements_by_class_name("name")
    #         al_pl = []
    #         for i in players:
    #             al_pl.append(i.text.split("\n")[0])
    #
    #         home_team = al_pl[0:11]
    #
    #         players = teams[1].find_elements_by_class_name("name")
    #         al_pl = []
    #         for i in players:
    #             al_pl.append(i.text.split("\n")[0])
    #
    #         away_team = al_pl[0:11]
    #         row = home_team + away_team
    #         row.append(home)
    #         row.append(away)
    #         row.append(home_score)
    #         row.append(away_score)
    #
    #         date = driver.find_element_by_css_selector(".matchDate.renderMatchDateContainer").text
    #
    #         driver.find_element_by_css_selector(".mcNavButton.matchWeekTableButton").click()
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[@class='points']")))
    #         week = driver.find_element_by_class_name("standingEntriesContainer").find_elements_by_tag_name("tr")
    #         for w in week:
    #             if w.find_element_by_class_name("team").text == home:
    #                 home_games = w.find_elements_by_tag_name("td")[2].text
    #                 home_points = w.find_element_by_class_name("points").text
    #             elif w.find_element_by_class_name("team").text == away:
    #                 away_games = w.find_elements_by_tag_name("td")[2].text
    #                 away_points = w.find_element_by_class_name("points").text
    #             else:
    #                 continue
    #
    #         row.append(home_games)
    #         row.append(home_points)
    #         row.append(away_games)
    #         row.append(away_points)
    # #         row.append(date)
    #         rows.append(row)
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
