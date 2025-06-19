# 🃏 TCGPlayer Card Price Checker

This is a Python desktop GUI tool that uses **Selenium** and **BeautifulSoup** to scrape [TCGPlayer](https://www.tcgplayer.com) for card market prices and recent sales data. The app allows you to search for a card and optionally filter recent sales by condition (e.g., `NM`, `LP`, `MP`, `HP`, `DMG`).

---

## 📦 Features

- GUI built with **Tkinter**
- Pulls **market price** and **recent sales history**
- Optional condition filtering for dynamic sales history
- Automatically limits results to 15 rows
- Multithreaded scraping to keep GUI responsive

---

## 🛠 Requirements

Install the required Python libraries:

```bash
pip install selenium beautifulsoup4
```
- Make sure you have **Chrome** installed
- Make sure your ChromeDriver matches your Chrome version: [ChromeDriver](https://sites.google.com/chromium.org/driver)

## ▶️ How to Run the App
Save the script as tcg_checker.py  
Open a terminal or command prompt  
Then cd into the tcg_checker.py folder  
Run the script using Python 3:  

```bash
python tcg_checker.py
```
- The GUI window will appear:
- Enter the card name (e.g. Pikachu EX 179/131)
- Optionally enter a condition (NM, LP, etc.)
- Click Search
- Wait for the results to load in the output box

## 💡 Example Output
Card Name: Glaceon V (Alternate Full Art) - SWSH07: Evolving Skies (SWSH07)  
Market Price: $105.28  
  
Date: 6/17/25 | Condition: NM | Price: $123.20  
Date: 6/16/25 | Condition: NM | Price: $111.00  
Date: 6/15/25 | Condition: NM | Price: $111.00  
Date: 6/14/25 | Condition: NM | Price: $123.20  
Date: 6/13/25 | Condition: NM | Price: $114.99  
Date: 6/11/25 | Condition: NM | Price: $123.29  
Date: 6/6/25 | Condition: NM | Price: $115.99  
Date: 6/4/25 | Condition: NM | Price: $116.53  
Date: 6/3/25 | Condition: NM | Price: $59.89  
...

