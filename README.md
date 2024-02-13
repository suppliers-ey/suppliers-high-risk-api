# High-Risk Entity Search Tool

This project is an automated tool designed for financial institutions that need to conduct online searches to identify entities in high-risk lists, such as international sanctions, watchlists, and other relevant databases. The tool utilizes web scraping techniques to extract the necessary information from online sources and presents it in a readable format for review.

## Sources
- Offshore Leaks Database: `https://offshoreleaks.icij.org` 
    Attributes: Entity, Jurisdiction, Linked To, Data From
- The World Bank: `https://projects.worldbank.org/en/projectsoperations/procurement/debarred-firms`
    Attributes: Firm Name, Address, Country, From Date (Ineligibility Period), To Date (Ineligibility Period), Grounds
- OFAC: `https://sanctionssearch.ofac.treas.gov/`
    Attributes: Name, Address, Type, Program(s), List, Score

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.7+
- pip (Python package manager)
- Google Chrome browser
- ChromeDriver

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/suppliers-ey/suppliers-high-risk-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd suppliers-high-risk-api
    ```

3. (Optional) Create and activate a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

6. Open your web browser and go to `http://localhost:8000/docs` to interact with the API documentation.

## Usage

- Once the server is running, you can access the API endpoints using tools like cURL, Postman, or any web browser.
- Refer to the API documentation (`http://localhost:8000/docs`) for detailed information about available endpoints and how to use them.
