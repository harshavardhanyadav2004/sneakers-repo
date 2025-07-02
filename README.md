# 👟 Sneakers Repo

A web scraping project to extract sneaker product information from [KicksCrew](https://www.kickscrew.com) and manage it for analysis or inventory processing.

## 📌 Overview

This project scrapes sneaker product data (such as product titles and URLs) from KicksCrew's website and saves the data in a CSV format. It also supports updating those products with unique product IDs for further processing.

## 📂 Project Structure

```
sneakers-repo/
├── __pycache__/                           # Python cache files
├── main.py                                # Main scraping script
├── update_product_id.py                   # Script to add product IDs
├── kickscrew_products_simple.csv          # Initial scraped data
├── updated_kickscrew_products_simple.csv  # Data with product IDs
├── requirements.txt                       # Python dependencies
└── README.md                             # This file
```

## 🚀 Features

- **Web Scraping**: Extract sneaker product information from KicksCrew
- **Data Management**: Save scraped data in CSV format for easy analysis
- **Product ID Assignment**: Add unique identifiers to products
- **Simple Workflow**: Two-step process for complete data collection

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/harshavardhanyadav2004/sneakers-repo.git
cd sneakers-repo
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Step 1: Scrape Sneaker Data
```bash
python main.py
```
This will scrape sneaker data from KicksCrew and save it to `kickscrew_products_simple.csv`

### Step 2: Add Product IDs
```bash
python update_product_id.py
```
This will read the scraped data and add unique product IDs, saving the result to `updated_kickscrew_products_simple.csv`

### Complete Workflow
```bash
# 1. Scrape the data
python main.py

# 2. Add product IDs
python update_product_id.py

# 3. Your data is now ready in updated_kickscrew_products_simple.csv
```

## 📊 Output Files

### kickscrew_products_simple.csv
Initial scraped data containing basic sneaker information from KicksCrew.

### updated_kickscrew_products_simple.csv  
Enhanced dataset with unique product IDs added to each sneaker entry for better data management and analysis.

## 📋 Data Structure

The scraped data typically includes fields such as:

| Field | Description | Type |
|-------|-------------|------|
| `title` | Sneaker product title | String |
| `url` | Product page URL | String |
| `price` | Product price | String/Float |
| `image_url` | Product image URL | String |
| `product_id` | Unique identifier (added by update script) | String |

*Note: Actual fields may vary based on the scraping implementation*

## 📈 Examples

### Example 1: Running the Main Scraper
```python
# This is what main.py does
python main.py
# Output: kickscrew_products_simple.csv with scraped sneaker data
```

### Example 2: Adding Product IDs
```python
# This is what update_product_id.py does
python update_product_id.py
# Input: kickscrew_products_simple.csv
# Output: updated_kickscrew_products_simple.csv
```

### Example 3: Working with the Data
```python
import pandas as pd

# Load the updated data
df = pd.read_csv('updated_kickscrew_products_simple.csv')

# Display basic info
print(f"Total products: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the root directory (optional):
```env
# Scraping Settings
DELAY_BETWEEN_REQUESTS=1
MAX_RETRIES=3
TIMEOUT=30
```

### Settings Configuration
You can modify the scraping behavior by editing the scripts directly:

**main.py**: Adjust scraping parameters like:
- Number of pages to scrape
- Request delays
- Output filename
- CSS selectors for data extraction

**update_product_id.py**: Customize product ID generation:
- ID format and structure
- Input/output file names
- Data processing logic

## 🧪 Testing

Since this is a simple scraping project, you can test it by:

```bash
# Test the main scraper
python main.py

# Verify the CSV was created
ls -la kickscrew_products_simple.csv

# Test the product ID updater
python update_product_id.py

# Verify the updated CSV was created
ls -la updated_kickscrew_products_simple.csv
```

## 🛡️ Rate Limiting & Ethics

This scraper implements responsible scraping practices:
- Respects robots.txt
- Implements delays between requests
- Follows website terms of service
- Avoids overloading servers

## 🚫 Limitations

- Requires stable internet connection
- May break if website structure changes
- Rate limited to prevent server overload
- Dependent on KicksCrew website availability

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ConnectionError` or `Timeout`
```bash
# Solution: Check internet connection or increase timeout
# Modify delay settings in main.py
```

**Issue**: Empty CSV file
```bash
# Solution: Check if website structure has changed
# Update CSS selectors in main.py
```

**Issue**: Module not found
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Test your changes before submitting
- Update documentation if needed
- Ensure code is well-commented

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Users are responsible for:
- Respecting website terms of service
- Following applicable laws and regulations
- Not overloading servers with requests
- Using scraped data ethically

## 🤝 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contact: harshavardhanyadav2004@gmail.com

## 🎯 Future Enhancements

- [ ] Add support for more sneaker websites
- [ ] Implement database storage
- [ ] Add price tracking functionality
- [ ] Create data visualization dashboard
- [ ] Add automated scheduling
- [ ] Implement email notifications for new products

---

**Made with ❤️ by [Harsha Vardhan Yadav](https://github.com/harshavardhanyadav2004)**

> Dataset of sneakers available with images link without the sale prices
