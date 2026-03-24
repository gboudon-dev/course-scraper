**Modular scraping project designed for batch execution using ephemeral containers.**

The goal of this project is to monitor three websites that offer courses and perform scraping of the general content of the available courses.
It is designed to be executed using ephemeral Docker containers, which can be scheduled to run daily directly on the server or through automation tools such as N8N.


**Architecture**

Two main tasks were defined for each provider:

Collect the different URLs from the site associated with specific courses and store them in the database.
Visit each of those URLs, extract the course information and update the corresponding table in the database.

To achieve this, a class was created for each provider, along with a base class that contains the common logic for each type of task (URL scraping and course detail scraping).

Additionally, a tasks file was created, which allows executing any of the defined tasks, either scraping URLs from a provider or collecting detailed information. The main.py file is responsible for executing the specified task through environment variables.

The purpose of this subdivision is to allow tasks to be executed independently, instead of being part of a single process, providing more flexibility and better error handling.


**Project structure**


project/

├── main.py
├── tasks/
│   └── tasks.py
├── url\_scrapers/
│   ├── base\_scraper.py
│   ├── provider\_a.py
│   ├── provider\_b.py
│   └── provider\_c.py
├── course\_info\_scrapers/
│   ├── base\_detail\_scraper.py
│   ├── provider\_a\_detail.py
│   ├── provider\_b\_detail.py
│   └── provider\_c\_detail.py
├── database/
│   └── db\_manager.py


**Requirements**

Python
Docker
Playwright

**Database**

The project requires a MariaDB/MySQL DB, which must be created before execution.
A schema.sql file is included in the root folder of the project for this purpose.
You can use it with the following command: 

mysql -u root -p proyecto_monitoreo < schema.sql

**Execution**

The project is designed to run using ephemeral Docker containers, which can be scheduled using crontab on the server or through external tools such as N8N.

Docker execution

# Build image (While on the root folder)
docker build -t scraper .

# Run ephemeral container
docker run --rm \
  -e TASK="prov a" \
  -e DB_HOST="your_host" \
  -e DB_PORT="3306" \
  -e DB_USER="your_user" \
  -e DB_PASSWORD="your_password" \
  -e DB_NAME="your_db" \
  scraper

# Simple execution for testing

Install dependencies (including Playwright and browser):
pip install -r requirements.txt
playwright install
Run passing environment variables:

set "TASK=prov a" && set "DB_HOST=host_address" && set "DB_PORT=3306" \&\& set "DB_USER=username" && set "DB_PASSWORD=pass" && set "DB_NAME=database_name" && python main.py

**Environment variables**

The system is controlled through the TASK variable, along with the database connection variables.


**Available tasks**

TASKS = {
    "prov a": provider\_a\_scraper,
    "prov b": provider\_b\_scraper,
    "prov c": provider\_c\_scraper,
    "prov a detail": provider\_a\_detail\_scraper,
    "prov b detail": provider\_b\_detail\_scraper,
    "prov c detail": provider\_c\_detail\_scraper,
}

There are two tasks for each provider:

prov a: visits the provider’s site, retrieves course URLs and stores them in the database.

prov a detail: visits each stored URL and records the detailed course information in the database.

The rest follow the same logic.

