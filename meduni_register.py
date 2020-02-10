#needs pip install selenium and python 3
from time import sleep
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

#your current semester
semester = 3
#enter your Studienplan just like in the dropdown when selecting your semester
studienPlan = 'Zahnmedizin'
#this is the group you wanna be in
gruppe = 3

#replace with you user and password
user = "user"
password = "password"

#leave this one alone if you don't know what you are doing
retryCount=75
driver = webdriver.Chrome()
wait = WebDriverWait(driver,5)

def switchFrame(frameName):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name(frameName))

def reloadDetailFrame():
    driver.execute_script('parent.frames["detail"].location.reload();')

def getDateFromSite():
    switchFrame("detail")
    startDate = findall("((?:[0-9]{2}\.){2}[0-9]{4}\ [0-9]{2}:[0-9]{2})", driver.find_element_by_css_selector("#pageContent > form > p").text.split('meldung: ')[1])[0]
    year = int(startDate.split('.')[2].split(' ')[0])
    month = int(startDate.split('.')[1])
    day = int(startDate.split('.')[0])
    hour = int(startDate.split('.')[2].split(' ')[1].split(':')[0])
    minute = int(startDate.split('.')[2].split(' ')[1].split(':')[1])
    return datetime(year,month,day,hour,minute,0,0)

def waitTillStart():
    to=getDateFromSite()
    print("start: "+str(to))
    to = to - timedelta(seconds = 10)
    print("start minus 10 seconds: "+str(to))
    now = datetime.now
    print("now: "+str(now()))
    #to = (now() + timedelta(days = 1)).replace(hour=1, minute=0, second=0)
    print("Waiting " + str((to-now()).seconds) +" seconds")
    sleep((to-now()).seconds)

driver.get("https://campus.meduniwien.ac.at/med.campus/webnav.ini")

switchFrame('menue')
wait.until(EC.visibility_of(driver.find_element_by_css_selector('img[name="key"]')))
driver.find_element_by_css_selector('img[name="key"]').click()

switchFrame('detail')
sleep(0.5)
wait.until(EC.visibility_of(driver.find_element_by_css_selector('input[type="TEXT"]')))
driver.find_element_by_css_selector('input[type="TEXT"]').send_keys(user)
driver.find_element_by_css_selector('input[type="PASSWORD"]').send_keys(password)
driver.find_element_by_css_selector('button[type="SUBMIT"]').click()


sleep(0.5)
wait.until(EC.visibility_of(driver.find_element_by_css_selector('a[title="Anmeldung zu Modulen"]')))
driver.find_element_by_css_selector('a[title="Anmeldung zu Modulen"]').click()


sleep(0.5)
studiumSelect = Select(driver.find_element_by_name('pStudiumNr'))
semesterSelect = Select(driver.find_element_by_name('pSemInStp'))


sleep(0.5)
studiumSelect.select_by_visible_text(studienPlan)
semesterSelect.select_by_value(str(semester))
driver.find_element_by_id('S1').click()

waitTillStart()

for x in range(retryCount):
    try:
        groupRow = driver.find_element_by_css_selector("tr:nth-of-type(" + str(gruppe + 1 ) + ")")
        groupRow.find_element_by_css_selector('button[title="Zur Planungsgruppe anmelden"]').click()
    except NoSuchElementException as e:
        print("Haven't found a free space " + str(x) + " times")
        reloadDetailFrame()
        sleep(0.2)
    
