import pandas as pd

def get_product_id_from_url(url):
    try:
        last = url.strip().split("/")[-1]
        parts = last.split("-")
        if len(parts) >= 2:
            return f"{parts[-2]}-{parts[-1]}"
    except:
        pass
    return None

input_file = "kickscrew_products_simple.csv"   
output_file = "updated_kickscrew_products_simple.csv"      

df = pd.read_csv(input_file)

df['product_id'] = df['url'].apply(get_product_id_from_url)

df.to_csv(output_file, index=False)
print(f"Updated product_id values saved to {output_file}")
