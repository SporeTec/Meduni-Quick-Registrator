#needs pip install selenium and python 3
from time import sleep
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import pause

#your current semester
semester = 3
#enter your Studienplan just like in the dropdown when selecting your semester
studienPlan = 'Zahnmedizin'
#this is the group you wanna be in
gruppe = 3
#copy the anmeldedatum straight from the website
startDate="16.09.2019 00:18"

#replace with you user and password
user = "user"
password = "password"

#leave this one alone if you don't know what you are doing
retryCount=200
driver = webdriver.Chrome()
wait = WebDriverWait(driver,3)

def switchFrame(frameName):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name(frameName))

def reloadDetailFrame():
    driver.execute_script('parent.frames["detail"].location.reload();')

def waitTillStart(startDate):
    year = int(startDate.split('.')[2].split(' ')[0])
    month = int(startDate.split('.')[1])
    day = int(startDate.split('.')[0])
    hour = int(startDate.split('.')[2].split(' ')[1].split(':')[0])
    minute = int(startDate.split('.')[2].split(' ')[1].split(':')[1])
    to = datetime(year,month,day,hour,minute,0,0)
    print(to)
    to = to - timedelta(seconds = 10)
    print(to)
    now = datetime.now
    print(now())
    #to = (now() + timedelta(days = 1)).replace(hour=1, minute=0, second=0)
    print("Waiting " + str((to-now()).seconds) +" seconds")
    sleep((to-now()).seconds)

driver.get("https://campus.meduniwien.ac.at/med.campus/webnav.ini")

switchFrame('menue')
wait.until(EC.visibility_of(driver.find_element_by_css_selector('img[name="key"]')))
driver.find_element_by_css_selector('img[name="key"]').click()

switchFrame('detail')
driver.find_element_by_css_selector('input[type="text"]').send_keys(user)
driver.find_element_by_css_selector('input[type="password"]').send_keys(password)
driver.find_element_by_css_selector('button[type="submit"]').click()

wait.until(EC.visibility_of(driver.find_element_by_css_selector('a[title="Anmeldung zu Modulen')))
driver.find_element_by_css_selector('a[title="Anmeldung zu Modulen"]').click()

studiumSelect = Select(driver.find_element_by_name('pStudiumNr'))
semesterSelect = Select(driver.find_element_by_name('pSemInStp'))

studiumSelect.select_by_visible_text(studienPlan)
semesterSelect.select_by_value(str(semester))
driver.find_element_by_id('S1').click()

waitTillStart(startDate)

for x in range(retryCount):
    try:
        groupRow = driver.find_element_by_css_selector("tr:nth-of-type(" + str(gruppe + 1 ) + ")")
        groupRow.find_element_by_css_selector('button[title="Zur Planungsgruppe anmelden"]').click()
    except NoSuchElementException as e:
        print("Haven't found a free space " + str(x) + " times")
        sleep(0.1)
        reloadDetailFrame()
    