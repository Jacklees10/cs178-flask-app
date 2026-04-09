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
I created a DynamoDB table called "Favorites" that stores any favorite countries users want to add to the database. The partition key is CountryName, and it has attributes Population and Primary Language. It connects to the rest of the app because it allows the user to add language

- **Table name:** `[Favorites]`
- **Partition key:** `[CountryName]`
- **Used for:** `[Adding favorite countries including their primary language]`

---

## CRUD Operations

| Operation | Route               | Description                     |
| --------- | ------------------- | ------------------------------- |
| Create    | `/[Add Country]`    | Adds a country to the list      |
| Read      | `/[Delete Country]` | Deletes a country from the list |
| Update    | `/[Update Country]` | Updates a country on the list   |
| Delete    | `/[Delete Country]` | Deletes a country from the list |

---

## Challenges and Insights

The hardest part about this project was getting the website to actually run. I got connection error after programming error after connection error, and I fixed it by changing the creds file so it was pointing to the right dataset with the right user. 

I learned so much about html in this project, so much so that now I can confidently say I understand how html goes from my VSCode environment to my running flaskapp website. 

I also learned that it is very important to commit and push changes to GitHub frequently in order to track progress. 

---

## AI Assistance

I used mainly Claude and a little bit of ChatGPT to help me write code for the flaskapp.py, dbCode.py, and all html files. I also relied heavily on Claude to troubleshoot any issues that came up.
