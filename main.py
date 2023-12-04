from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time

current_date = datetime.now().date()
days_until_next_monday = (7 - current_date.weekday()) % 7
next_monday_date = current_date + timedelta(days=days_until_next_monday)
next_week_date = current_date + timedelta(days=7)

url = f"https://www.eventbrite.es/d/spain--barcelona/free--events/?page=1&start_date={next_monday_date}&end_date={next_week_date}"
print(url)

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
time.sleep(10)

html_text = driver.page_source
driver.quit()

soup = BeautifulSoup(html_text, 'lxml')
titleHorizontal = soup.find_all('section', class_='discover-horizontal-event-card')

f = open("output.txt", "w")
for card in titleHorizontal:
    element = card.div
    link = element.a['href']
    title = element.h2.text
    paragraphsArray = list(element.find_all('p'))
    if 'EventCardUrgencySignal__label' in paragraphsArray[0]['class']:
        date = paragraphsArray[1].text
    else:
        date = paragraphsArray[0].text

    badge = element.select_one('.event-card-badge')

    badge_text = badge.text if badge else "No badge information"

    line = f"{title} {date} {link} Badge: {badge_text}.\n"
    f.write(line)

f.close()
