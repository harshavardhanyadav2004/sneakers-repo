# 👟 Sneakers Repo

A web scraping project to extract sneaker product information from [KicksCrew](https://www.kickscrew.com) and manage it for analysis or inventory processing.

## 📌 Overview

This project scrapes sneaker product data (such as product titles and URLs) from KicksCrew's website and saves the data in a CSV format. It also supports updating those products with unique product IDs for further processing.

## 📂 Project Structure

sneakers-repo/
├── pycache/ # Python cache directory
├── kickscrew_products_simple.csv # Scraped sneaker data (raw)
├── updated_kickscrew_products_simple.csv # Scraped data with product IDs
├── main.py # Main scraper script
├── update_product_id.py # Script to assign product IDs
├── requirements.txt # Python dependencies
└── README.md # Project documentation
### 1. Clone the Repository

```bash
git clone https://github.com/harshavardhanyadav2004/sneakers-repo.git
cd sneakers-repo

pip install -r requirements.txt
```
