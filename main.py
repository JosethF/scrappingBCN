from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
from datetime import datetime, timedelta
from selenium import webdriver

def getUrl(page):
    current_date = datetime.now().date()
    days_until_next_monday = (7 - current_date.weekday()) % 7
    next_monday_date = current_date + timedelta(days=days_until_next_monday)
    next_week_date = current_date + timedelta(weeks=1)
    url = f"https://www.eventbrite.es/d/spain--barcelona/free--events/?page={page}&start_date={current_date}&end_date={next_week_date}" if days_until_next_monday < 2 else f"https://www.eventbrite.es/d/spain--barcelona/free--events/?page={page}&start_date={current_date}&end_date={next_monday_date}"
    return url


def setPagination(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    pagination_element = driver.find_element(By.CLASS_NAME, "eds-pagination__navigation-minimal").text
    global page
    page = int(' '.join(pagination_element.split(' ')[2:]))


def getInfoSections(url):
    html_text = requests.get(url, timeout=(20, 60)).text
    soup = BeautifulSoup(html_text, 'lxml')
    titleHorizontal = soup.find_all('section', class_='discover-horizontal-event-card')
    return titleHorizontal

   
def writeOutputFile(mode, titleHorizontal):
    with open("output.txt", mode) as f:
        for card in titleHorizontal:
            element = card.div
            link = element.a['href']
            title = element.h2.text
            paragraphsArray = list(element.find_all('p'))
            if 'EventCardUrgencySignal__label' in paragraphsArray[0]['class']:
                date = paragraphsArray[1].text
            else:
                date = paragraphsArray[0].text
            line = f"{title} {date} {link}.\n"
            f.write(line)

if __name__ == "__main__":
    
    page = 1
    url = getUrl(page)
    setPagination(url)

    for i in range(page):
        iteration = i+1
        url = getUrl(iteration)
        titleHorizontal = getInfoSections(url)
        if iteration == 1:
            writeOutputFile("w",titleHorizontal)
        else:
            writeOutputFile("a",titleHorizontal)
