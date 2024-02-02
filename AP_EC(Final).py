from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import pandas as pd
import time

chrome_options = Options()
driver = webdriver.Chrome(executable_path=r"D:\Chrome Driver\chromedriver-win64\chromedriver.exe", options=chrome_options)
database = []

driver.get('http://rs.ap.gov.in/IGRS_RegnDeptLogin_website_main/FindSroMod.do?method=getDistrictsforUrban')

try:
    district_select = Select(driver.find_element(By.ID, 'districtCode'))
    for i in range(1, len(district_select.options)):
        dist_1 = district_select.options[i].get_attribute('innerHTML')
        district_select.select_by_index(i)
        time.sleep(2)

        teh_db = []
        tehsil_select = Select(driver.find_element(By.ID, 'mandalCode'))
        for j in range(1, len(tehsil_select.options)):
            teh_1 = tehsil_select.options[j].get_attribute('innerHTML')
            tehsil_select.select_by_index(j)
            time.sleep(3)

            try:
                alert = Alert(driver)
                alert_text = alert.text
                alert.accept()
            except:
                pass

            vil_db = []
            village_select = driver.find_elements_by_xpath("//select[@id='villageCode']/option")
            for k in range(1, len(village_select)):
                vil_1 = village_select[k].get_attribute('innerHTML')
                vil_db.append(vil_1)
                database.append(dist_1 + '--->' + teh_1 + '--->' + vil_1)
                print(dist_1 + '--->' + teh_1 + '--->' + vil_1)

    a = [i.split('--->') for i in database]
    df = pd.DataFrame(a, columns=['District', 'Mandal', 'Village'])
    df.to_excel('Ap_Ec_october_2023.xlsx', index=True, engine='xlsxwriter')
except Exception as e:
    print(str(e))
    a = [i.split('--->') for i in database]
    df = pd.DataFrame(a, columns=['District', 'Mandal', 'Village'])
    df.to_excel('Ap_Ec_october_2023(e).xlsx', index=True, engine='xlsxwriter')
