import threading
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_card_data(card, condition_filter, output_box):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    card_query = card.replace(" ", "+")
    url = f"https://www.tcgplayer.com/search/all/product?q={card_query}&view=grid&ProductTypeName=Cards"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        link_element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid^="product-card__image--"]'))
        )
        driver.get(link_element.get_attribute("href"))

        card_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-details__name"))
        ).text

        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "price-points__upper__price"))
        ).text

        output_box.insert(tk.END, f"Card Name: {card_name}\n")
        output_box.insert(tk.END, f"Market Price: {price}\n\n")

        viewMoreButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modal__activator")))
        viewMoreButton.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "latest-sales-table__tbody")))
        WebDriverWait(driver, 20).until(
            lambda d: all(
                "$0.00" not in row.text and "12/12/12" not in row.text
                for row in d.find_elements(By.CSS_SELECTOR, ".latest-sales-table__tbody tr")
            )
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select("tbody.latest-sales-table__tbody tr")

        global sales_data
        sales_data = []

        for row in rows:
            try:
                date = row.select_one(".latest-sales-table__tbody__date").text.strip()
                condition = row.select_one(".latest-sales-table__tbody__condition div").text.strip().split(" ", 1)[0]
                price = row.select_one(".latest-sales-table__tbody__price").text.strip()
                sales_data.append({"date": date, "condition": condition, "price": price})
            except:
                continue
        
        count = 0
        if condition_filter == '':
            for entry in sales_data:
                output_box.insert(tk.END, f"Date: {entry['date']} | Condition: {entry['condition']} | Price: {entry['price']}\n")
                count += 1
                if count > 8:
                    break
        else:
            for entry in sales_data:
                if entry['condition'].upper() == condition_filter.upper()   :
                    output_box.insert(tk.END, f"Date: {entry['date']} | Condition: {entry['condition']} | Price: {entry['price']}\n")
                    count += 1
                if count > 8:
                    break
        

    except Exception as e:
        messagebox.showerror("Error", f"Scraping failed: {e}")
    finally:
        driver.quit()


def change_condition(condition, output_box):
    output_box.delete(4.0, tk.END)
    output_box.insert(tk.END, "\n")
    global card_condition
    card_condition = condition
    count = 0
    if condition == '':
        for entry in sales_data:
            output_box.insert(tk.END, f"Date: {entry['date']} | Condition: {entry['condition']} | Price: {entry['price']}\n")
            count += 1
            if count > 8:
                break
    else:
        for entry in sales_data:
            if entry['condition'].upper() == condition:
                output_box.insert(tk.END, f"Date: {entry['date']} | Condition: {entry['condition']} | Price: {entry['price']}\n")
                count += 1
            if count > 8:
                break


def on_submit(card_entry, output_box):
    output_box.delete(1.0, tk.END)
    card = card_entry.get()
    global sales_data
    sales_data = []
    global card_condition
    threading.Thread(target=scrape_card_data, args=(card, card_condition, output_box), daemon=True).start()

sales_data = []
card_condition = ''

root = tk.Tk()
root.title("TCGPlayer Card Price Checker")
root.geometry("600x500")

tk.Label(root, text="Card Name:").pack(pady=(10, 0))
card_entry = tk.Entry(root, width=50)
card_entry.pack()

tk.Label(root, text="Condition:").pack(pady=(10, 0))

condition_frame = tk.Frame(root)
condition_frame.pack(pady=10)

condition_btn0 = tk.Button(condition_frame, text="All", command=lambda: change_condition('', output_box))
condition_btn0.pack(side=tk.LEFT, padx=5)
condition_btn1 = tk.Button(condition_frame, text="NM", command=lambda: change_condition('NM', output_box))
condition_btn1.pack(side=tk.LEFT, padx=5)
condition_btn2 = tk.Button(condition_frame, text="LP", command=lambda: change_condition('LP', output_box))
condition_btn2.pack(side=tk.LEFT, padx=5)
condition_btn3 = tk.Button(condition_frame, text="MP", command=lambda: change_condition('MP', output_box))
condition_btn3.pack(side=tk.LEFT, padx=5)
condition_btn4 = tk.Button(condition_frame, text="HP", command=lambda: change_condition('HP', output_box))
condition_btn4.pack(side=tk.LEFT, padx=5)
condition_btn5 = tk.Button(condition_frame, text="DMG", command=lambda: change_condition('DMG', output_box))
condition_btn5.pack(side=tk.LEFT, padx=5)


# tk.Label(root, text="Condition (NM, LP, MP, HP, DMG):").pack(pady=(10, 0))
# condition_entry.pack()

submit_btn = tk.Button(root, text="Search", command=lambda: on_submit(card_entry, output_box))
submit_btn.pack(pady=10)

output_box = tk.Text(root, wrap=tk.WORD, height=20, width=70)
output_box.pack(pady=10)

scrollbar = tk.Scrollbar(root, command=output_box.yview)
output_box.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
