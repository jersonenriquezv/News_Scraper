# News_Scraper

This project is a web scraping tool that extracts the latest news articles from a specific website and stores them in a MongoDB database. The scraper runs periodically, ensuring the database is always updated with fresh articles. The project demonstrates the use of Selenium for web scraping, pymongo for database interaction, and scheduling tasks on Windows Task Scheduler.

Features
Scrapes news articles from a predefined news site.
Extracts article details such as title, body, category, publication date, and source.
Saves the scraped data in MongoDB.
Scheduled to run automatically every five hours to ensure the data remains up-to-date.
Challenges Faced
1. MongoDB Setup
One of the early challenges was configuring MongoDB locally and ensuring the database service runs consistently. Installing MongoDB and MongoDB Compass for data visualization was straightforward, but configuring the environment variables and ensuring that MongoDB could be accessed from the script required extra effort.

2. Integrating Web Scraping with the Database
While writing the scraper was relatively smooth, integrating it with MongoDB posed some complexities. Understanding how to insert JSON data into MongoDB collections and avoid circular imports during development was a key learning point.

3. Task Scheduling
Scheduling the script to run every 5 hours via Task Scheduler on Windows required trial and error. Initially, I had challenges with cron jobs using Git Bash, but ultimately, the Windows Task Scheduler proved to be the more reliable solution. Ensuring that the task would run when the computer is in sleep mode was another challenge that I successfully tackled by configuring the Task Scheduler settings.

How It Works
Scraper:

The news scraper is written in Python using Selenium to navigate the news website and extract relevant article data.
The data is saved as scraped_articles.json and contains fields like title, body, category, and publication date.
MongoDB:

The data is then inserted into a MongoDB collection using pymongo.
Each article is stored in a document inside the articles collection within the NewsDB database.
Task Scheduler:

The script is scheduled to run automatically every 5 hours using Windows Task Scheduler, ensuring fresh data is always collected.
Requirements
Python 3.7+
Selenium: for scraping
pymongo: for database connection
MongoDB: for storing the scraped data
Windows Task Scheduler: for scheduling the script to run periodically
Installation


Future Improvements
Extend the scraper to work with multiple news sites.
Improve error handling to gracefully manage site structure changes.
Implement a more flexible scheduling method, possibly using a dedicated job scheduler like Celery.

![NewsDB](https://github.com/user-attachments/assets/83283079-2b6f-4223-be3a-e471b01ef950)
![VSCODE](https://github.com/user-attachments/assets/1811adaf-89f6-4fa0-b4fd-73ad84d7575e)





