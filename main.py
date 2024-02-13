from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = FastAPI()

chrome_options = Options()
#chrome_options.add_argument("--headless")


@app.get("/worldbank/{company_name}")
async def search_company(company_name: str):
    debarrd_firms = await get_debarred_firms()
    results = []
    for firm in debarrd_firms["results"]:
        if company_name.lower() in firm["firm_name"].lower():
            results.append(firm)
    return {"results": results}


@app.get("/offshore-leaks/{company_name}")
async def search_company(company_name: str):
    url = f"https://offshoreleaks.icij.org/search?q={company_name}"

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5) 
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

@app.get("/debarred-firms")
async def get_debarred_firms():
    url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)
        page_source = driver.page_source
        driver.quit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    
    soup = BeautifulSoup(page_source, 'html.parser')
    results = []

    div = soup.find('div', class_='k-grid-content k-auto-scrollable')
    if not div:
        raise HTTPException(status_code=404, detail="No results found")
    table = div.find('table')
    if table:
        print("Table found")
        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            print(columns)
            if len(columns) > 0: 
                firm_name = columns[0].text.strip()
                address = columns[1].text.strip()
                country = columns[3].text.strip()
                ineligibility_from = columns[4].text.strip()
                ineligibility_to = columns[5].text.strip()
                grounds = columns[6].text.strip()
                results.append({
                    "firm_name": firm_name,
                    "address": address,
                    "country": country,
                    "ineligibility_period": {
                        "from_date": ineligibility_from,
                        "to_date": ineligibility_to
                    },
                    "grounds": grounds
                })

    return {"results": results}