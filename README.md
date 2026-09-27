# Course Scraper

Modular scraper that monitors the course catalogs of three education providers and keeps them in a relational database, built to run as scheduled, single-purpose containers.

## Scope of this repository

This repository is a code sample from a professional monitoring project. The target sites, their real CSS selectors and the database credentials are not included, by agreement with the client — the URLs in `tasks/tasks.py` are placeholders. **The project is therefore not runnable as published.** Everything below describes how it was designed and deployed, and is not a setup guide.

Providers are labelled A, B and C for brevity.

## Context

Three institutions publish course catalogs that change without notice: new programs appear, descriptions are rewritten, pages go offline. Checking them by hand does not scale, and an occasional snapshot is not enough to tell what changed.

The work is therefore split in two halves that run daily against a database holding one table per provider: collect the catalog's course URLs, then visit each URL and extract that course's description.

## Architecture

Two tasks are defined per provider:

1. **URL scraping** — walk the provider's catalog page by page and store every course URL found.
2. **Course-info scraping** — read the stored URLs back from the database, visit each one and update its description.

Each provider gets one class per task, and each family inherits from a base class — `BaseScraper` and `BaseDetailScraper` — holding what does not change between sites: browser lifecycle, the pagination loop, database calls, throttling. Subclasses supply only the genuinely site-specific part: which elements hold a course, and how to reach the next page.

`tasks/tasks.py` registers the six resulting tasks by name, and `main.py` runs the one named by the `TASK` environment variable.

The two tasks are separate processes rather than one pipeline for failure isolation. Course-info scraping is the long, fragile half — hundreds of page loads, any of which can time out. When it fails halfway, the URL harvest is already committed, so only the failing half needs retrying, and a provider whose site is down that day does not hold back the other two.

## Project structure

```
project/
├── main.py
├── tasks/
│   └── tasks.py
├── url_scrapers/
│   ├── base_scraper.py
│   ├── provider_a.py
│   ├── provider_b.py
│   └── provider_c.py
├── course_info_scrapers/
│   ├── base_detail_scraper.py
│   ├── provider_a_detail.py
│   ├── provider_b_detail.py
│   └── provider_c_detail.py
├── database/
│   └── db_manager.py
├── Dockerfile
└── schema.sql
```

## Deployment model

One image, built once; one ephemeral container per task run. A container does a single job and exits, which keeps scheduling in the scheduler instead of in the application — no long-running process, no internal timer, no state carried between runs.

The base image is the official Playwright Python image, so Chromium and its system dependencies come with the base layer:

```bash
docker build -t scraper .
```

Each run selects its task through the environment:

```bash
docker run --rm \
  -e TASK="prov a" \
  -e DB_HOST="your_host" \
  -e DB_PORT="3306" \
  -e DB_USER="your_user" \
  -e DB_PASSWORD="your_password" \
  -e DB_NAME="your_db" \
  scraper
```

The six runs are meant to be scheduled daily, either with crontab on the server or through an automation tool such as N8N. The only ordering constraint is that a provider's URL task must have run at least once before its course-info task has anything to read.

## Data model

One table per provider, all three sharing the same shape (`schema.sql`):

| Column | Purpose |
| --- | --- |
| `id` | surrogate key |
| `curso` | course name as published |
| `url` | course page — `UNIQUE` |
| `informacion` | extracted description |
| `estado_url` | flags URLs that returned no usable content |

The unique constraint on `url` is what makes a run repeatable. URL scraping inserts with `INSERT IGNORE`, so re-running a task that already partly succeeded adds the new courses and skips the known ones instead of duplicating them; course-info scraping is an `UPDATE` keyed on the same column, so it is idempotent for the same reason. Nothing is ever deleted, so a course that disappears from a catalog leaves its record behind.

Targets MariaDB/MySQL. The database itself must exist before the tables are created from `schema.sql`.

## Environment variables

| Variable | Description |
| --- | --- |
| `TASK` | which task to run (see below) |
| `DB_HOST` | database host |
| `DB_PORT` | database port |
| `DB_USER` | database user |
| `DB_PASSWORD` | database password |
| `DB_NAME` | database name |

`TASK` accepts six values:

| Value | Action |
| --- | --- |
| `prov a` | collect provider A's course URLs |
| `prov a detail` | extract descriptions for provider A's stored URLs |
| `prov b`, `prov b detail` | the same, for provider B |
| `prov c`, `prov c detail` | the same, for provider C |

See `.env.example` for a template.

## Known limitations

These shaped how the project had to be operated, and are the parts I would take up first:

- **Database errors are logged, not propagated.** A failed write prints and the process still exits `0`, so the scheduler cannot distinguish a broken run from an empty one.
- **No retries.** A page load that times out loses that course until the next day's run.
- **No record of when a course was last checked.** The tables hold the latest known state but not its age, which leaves "what has not been refreshed this week" unanswerable.
- **Selectors are inherently brittle.** A redesign on the provider's side breaks that provider's scraper silently: it finds zero courses and reports a clean finish. Alerting on a zero-result run would cover this.
- **Provider B does not fit the shared abstraction.** It reaches course pages through its own category listing rather than a paginated index, so it overrides the base pagination entirely.

## Stack

Python 3.10+, Playwright 1.58, PyMySQL, and a MariaDB/MySQL instance. `requirements.txt` covers the Python side; the Dockerfile's base image supplies the browser.
