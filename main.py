from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = FastAPI()

chrome_options = Options()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode

# Path to your Chrome WebDriver executable
chrome_path = "path/to/chromedriver.exe"

@app.get("/search")
async def search_company(company_name: str):
    url = f"https://offshoreleaks.icij.org/search?q={company_name}"

    try:
        # Use Selenium to load JavaScript content
        service = Service(chrome_path)
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)  # Adjust the delay time as necessary to ensure the page is fully loaded
        page_source = driver.page_source
        driver.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

    soup = BeautifulSoup(page_source, 'html.parser')
    results = []
    table = soup.find('table', class_='table-striped')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            entity = cols[0].text.strip()
            jurisdiction = cols[1].text.strip()
            linked_to = cols[2].text.strip()
            data_from = cols[3].text.strip()
            results.append({
                "entity": entity,
                "jurisdiction": jurisdiction,
                "linked_to": linked_to,
                "data_from": data_from
            })
    else:
        raise HTTPException(status_code=404, detail="No results found")

    return {"results": results}
