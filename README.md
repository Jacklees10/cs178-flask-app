# Ben's World Website

**CS178: Cloud and Database Systems — Project #1**
**Author:** Ben Jackels
**GitHub:** Jacklees10

---

## Overview

My project is a fully-functional website based on the world database. It features all CRUD operations, uses a SQL JOIN to join capitals to countries, and a favorites tab using DynamoDB.

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds.py      # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html        # Landing page
│   ├── add_country.html     # Add a country
│   ├── delete_country.html     # Delete a country
│   ├── update_country.html     # Update a country
│   ├── display_countries.html     # Display all countries
│   ├── countries_capitals.html     # View all countries and their capitals
│   ├── favorites.html     # View a favorites list of countries
│   ├── add_favorite.html     # Add a favorite country to the favorites list
│   ├── delete_favorite.html     # Delete a favorite country from the favorites list
├── .github/workflows/
│   ├── deploy.yml        # Deploys to GitHub
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Jackless10/cs178-flask-app.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://[your-ec2-public-ip]:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

The "world" database's main table is Country, with columns Code(PK), Name, Continent, and Population. 

- `[Country]` — stores statistics for 197 countries relating to geography, economics, and demographics; primary key is `[Code]`
- `[Capital]` — stores the city ID; foreign key links to `[City]` table
- `[Language]` — stores the names, status, and percentage of people who speak certain languages for different regions; foreign key links to the country code in the `[Country]` table

The JOIN query used in this project: 
I joined the City table to the Country table on Country's Capital column and City's ID column.

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `[your-table-name]`
- **Partition key:** `[key-name]`
- **Used for:** [description]

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/[route]` | [what it does] |
| Read      | `/[route]` | [what it does] |
| Update    | `/[route]` | [what it does] |
| Delete    | `/[route]` | [what it does] |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
