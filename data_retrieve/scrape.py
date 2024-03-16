# https://valuesider.com/
import requests
from bs4 import BeautifulSoup
import pandas as pd

# The URL of the page you want to scrape
url = "https://valuesider.com/guru/michael-burry-scion-asset-management/portfolio?sort=-percent_portfolio&page=1"
# Send a GET request to the webpage
response = requests.get(url)

# Initialize BeautifulSoup to parse the response content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the container that holds all the rows
container = soup.find('div', class_='guru_table_body')

# Initialize a list to store the scraped data
data = []

# Check if the container is found
if container:
    # Find all row divs within the container
    rows = container.find_all('div', class_='guru_table_row', recursive=False)

    for row in rows:
        # Extract the data from the cells
        cells = row.find_all('div', class_='guru_table_column')
        
        # The structure of the cells would need to be consistent with the webpage for accurate extraction
        if len(cells) > 5:  # Adjust based on the number of columns in the table
            ticker = cells[1].get_text(strip=True)  # Replace indices as needed
            stock = cells[2].get_text(strip=True)
            percent_portfolio = cells[3].get_text(strip=True)
            shares = cells[4].get_text(strip=True)
            reported_price = cells[5].get_text(strip=True)
            
            data.append([ticker, stock, percent_portfolio, shares, reported_price])

    # Convert the list to a DataFrame
    df = pd.DataFrame(data, columns=['Ticker', 'Stock', '% of Portfolio', 'Shares', 'Reported Price'])

    # Save the DataFrame to a CSV file
    df.to_csv('michael_burry_portfolio.csv', index=False)

    print(f"Data scraped and saved to 'miachel_burry.csv' successfully with {len(data)} records!")
else:
    print("The container with the specified class was not found.")