from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time

def scrape_page(driver, url):
    driver.get(url)
    time.sleep(10)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')
    title_horizontal = soup.find_all('section', class_='discover-horizontal-event-card')
    return title_horizontal

def main():
    current_date = datetime.now().date()
    days_until_next_monday = (7 - current_date.weekday()) % 7
    next_monday_date = current_date + timedelta(days=days_until_next_monday)
    next_week_date = current_date + timedelta(days=7)

    base_url = "https://www.eventbrite.es/d/spain--barcelona/free--events/?page={}&start_date={}&end_date={}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    page_number = 1
    while True:
        url = base_url.format(page_number, next_monday_date, next_week_date)
        
        title_horizontal = scrape_page(driver, url)

        if not title_horizontal:
            break  # No more pages

        with open("output.txt", "a") as f:
            for card in title_horizontal:
                element = card.div
                link = element.a['href']
                title = element.h2.text
                paragraphs_array = list(element.find_all('p'))
                date = paragraphs_array[1].text
                if ':' in date.lower():
                    line = f"{title} {date} {link}\n"
                    f.write(line)
                """
                if 'EventCardUrgencySignal__label' in paragraphs_array[0]['class']:
                    date = paragraphs_array[1].text
                else:
                """

        #page_number += 1

    driver.quit()

if __name__ == "__main__":
    main()