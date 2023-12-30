from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
current_date = datetime.now().date()
days_until_next_monday = (7 - current_date.weekday()) % 7
next_monday_date = current_date + timedelta(days=days_until_next_monday)
next_week_date = current_date + timedelta(weeks=1)
url = f"https://www.eventbrite.es/d/spain--barcelona/free--events/?page=1&start_date={current_date}&end_date={next_week_date}" if days_until_next_monday < 2 else f"https://www.eventbrite.es/d/spain--barcelona/free--events/?page=1&start_date={current_date}&end_date={next_monday_date}"
print(url)
"""
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get(url)
"""
html_text = requests.get(url, timeout=(20, 60)).text
soup = BeautifulSoup(html_text,'lxml')

titleHorizontal = soup.find_all('section', class_ = 'discover-horizontal-event-card')

f = open("output.txt", "w")
for card in titleHorizontal:
    element = card.div
    badge = element.find_all('div', 'event-card-badge')
    print(badge)
    link = element.a['href']
    title = element.h2.text
    paragraphsArray = list(element.find_all('p'))
    if 'EventCardUrgencySignal__label' in paragraphsArray[0]['class']:
        date = paragraphsArray[1].text
    else:
        date = paragraphsArray[0].text
    line = f"{title} {date} {link}.\n"
    f.write(line)
f.close()
