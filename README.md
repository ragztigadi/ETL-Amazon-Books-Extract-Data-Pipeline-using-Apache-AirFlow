```markdown
# ETL Amazon Books Data Pipeline using Apache Airflow

## Project Overview

This project is a fully automated **ETL (Extract, Transform, Load) pipeline** that extracts book data from **Amazon**, transforms it into a structured format, and loads it into a **PostgreSQL database**. The pipeline is orchestrated using **Apache Airflow** and containerized using **Docker**.

**Key Features:**
- Web scraping Amazon books data using `requests` and `BeautifulSoup`
- Data transformation and deduplication with `pandas`
- Automatic loading into a Postgres database
- Task orchestration using Apache Airflow DAGs
- Containerized setup for seamless deployment with Docker Compose
- Web UI for monitoring via Airflow and pgAdmin

---

## Architecture

```

+----------------+        +-----------------+       +-----------------+
\|                |        |                 |       |                 |
\| Airflow DAG    | -----> | Extract & Transform| --> | Postgres DB     |
\| (PythonOperator)|        |  Scraping Logic |       | (Books Table)   |
\|                |        |                 |       |                 |
+----------------+        +-----------------+       +-----------------+
\|                                                  ^
\|                                                  |
v                                                  |
Airflow Scheduler & Webserver --------------------------+

````

**Services in Docker Compose:**

| Service                | Purpose                                 | Port / Access        |
|------------------------|-----------------------------------------|--------------------|
| `postgres`             | PostgreSQL DB to store book data        | 5432               |
| `pgadmin4_container`   | GUI to manage PostgreSQL                | 5050               |
| `redis`                | Message broker (for Celery tasks, optional) | 6379 (internal) |
| `airflow-apiserver`    | Airflow REST API                        | 8081               |
| `airflow-webserver`    | Airflow Web UI for DAG monitoring       | 8080               |

---

## Technologies Used

- **Python 3.10**: Core language for ETL logic
- **Apache Airflow**: Orchestration of DAG tasks
- **PostgreSQL**: Relational database for storing book data
- **pgAdmin**: Web-based GUI for Postgres
- **BeautifulSoup & Requests**: Web scraping
- **Pandas**: Data transformation
- **Docker & Docker Compose**: Containerization and deployment
- **WSL2 (Ubuntu)**: Development environment on Windows

---

## Setup & Installation

### Prerequisites
- Docker Desktop with WSL2 enabled
- Python 3.10 installed
- Virtual environment setup (optional, recommended)
- Access to terminal/bash

### Steps

1. Clone the repository:
```bash
git clone <your-repo-link>
cd ETL-Amazon-Books-Extract-Data-Pipeline-using-Apache-AirFlow
````

2. Create and activate Python virtual environment:

```bash
python3.10 -m venv airflow310
source airflow310/bin/activate
```

3. Start Docker Compose services:

```bash
docker compose up -d
```

4. Verify containers:

```bash
docker ps
```

5. Access services:

* **Airflow Web UI:** [http://localhost:8080](http://localhost:8080)
* **Airflow API Server:** [http://localhost:8081](http://localhost:8081)
* **pgAdmin:** [http://localhost:5050](http://localhost:5050)
  Use credentials from `docker-compose.yaml`:

  * Email: `admin@admin.com`
  * Password: `root`
  * Host (Postgres): `postgres`
  * Port: `5432`
  * DB: `airflow`
  * Username/Password: `airflow/airflow`

---

## DAG Workflow

**DAG Name:** `fetch_and_store_amazon_books`
**Schedule:** Daily (`timedelta(days=1)`)

**Tasks:**

1. **Fetch Book Data**

   * Scrapes Amazon for top 50 data engineering books
   * Extracts title, author, price, rating
   * Cleans duplicates and pushes to XCom

2. **Create Books Table**

   * Creates `books` table in Postgres if not exists

3. **Insert Book Data**

   * Pulls book data from XCom
   * Inserts into Postgres `books` table

**Task Dependencies:**

```
fetch_book_data_task >> create_table_task >> insert_book_data_task
```

---

## Example Output

After running the DAG successfully, the Postgres table `books` contains:

| id  | title                        | authors    | price | rating |
| --- | ---------------------------- | ---------- | ----- | ------ |
| 1   | Data Engineering with Python | John Doe   | 45    | 4.5    |
| 2   | Practical Data Engineering   | Jane Smith | 50    | 4.7    |
| ... | ...                          | ...        | ...   | ...    |

You can **view this output via pgAdmin** at [http://localhost:5050](http://localhost:5050) or query it directly in Airflow tasks.

---

## Notes & Best Practices

* Make sure Docker Desktop WSL integration is enabled for Ubuntu
* If running for the first time, check Postgres container health before starting pgAdmin
* Avoid running multiple Docker contexts simultaneously to prevent socket errors
* Airflow tasks use **XCom** for passing scraped data between operators

---

## License

This project is for educational purposes and personal use.
Do not deploy scraping logic to production without respecting Amazon's **Terms of Service**.

---

## Author

**Raghav Tigadi**

* LinkedIn: \[Your LinkedIn]
* GitHub: [https://github.com/ragztigadi](https://github.com/ragztigadi)

```

