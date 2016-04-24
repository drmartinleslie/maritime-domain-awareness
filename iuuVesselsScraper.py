from pymongo import MongoClient
from selenium import webdriver

mc = MongoClient()
db = mc.vesselDB
db.iuu.drop()
iuuTable = db.iuu
driver = webdriver.Chrome('/Users/martinleslie/chromedriver') # need to download this and put it in right place

driver.get('http://iuu-vessels.org/iuu/iuu/search')
vesselTable = driver.find_element_by_id('vesselTable')
vesselTableBody = vesselTable.find_element_by_tag_name('tbody')
rows = vesselTableBody.find_elements_by_tag_name('tr')
front_page_info = []
link_info = []
for row in rows:
    cells = row.find_elements_by_tag_name('td')
    if len(cells) == 6:
        textList = [cell.text for cell in cells]
        urlList = [link.get_attribute('href') for cell in cells for link in cell.find_elements_by_tag_name('a')]
        infoRow = {"RFMO Vessel Name": textList[0], "IMO Number": textList[1], "IRCS": textList[2]}
        front_page_info.append(infoRow)
        link_info.append(urlList[0])
driver.quit()

for i in xrange(len(link_info)):
    link = link_info[i]
    newDriver = webdriver.Chrome('/Users/martinleslie/chromedriver')
    newDriver.get(link)
    overviewTableSpan = newDriver.find_element_by_id('overview')
    overviewTable = overviewTableSpan.find_element_by_tag_name('tbody')
    rows = overviewTable.find_elements_by_tag_name('tr')
    dataDict = {}
    for row in rows:
        dataCells = row.find_elements_by_tag_name('td')
        headerCells = row.find_elements_by_tag_name('th')
        dataTexts = [cell.text for cell in dataCells]
        headerTexts = [cell.text for cell in headerCells]
        dict = {"link": link}
        for i in xrange(len(dataTexts)):
            dict[headerTexts[i]] = dataTexts[i]
        for k in dict:
            kNoPeriods = k.replace('.','')
            dataDict[kNoPeriods] = dict[k]
    iuuTable.insert_one(dataDict)

    newDriver.quit()



