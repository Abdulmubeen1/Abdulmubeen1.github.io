import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_penny_stocks():
    # The URL for penny stocks with current price <= 1
    url = 'https://www.screener.in/screen/raw/?sort=current+price&order=asc&source_id=6994&query=Current+price+%3C%3D1'
    
    # Make a request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing stock data
    table = soup.find('table')  # Adjust this based on the actual structure of the page
    
    # Check if the table was found
    if table is None:
        print("Table not found!")
        return pd.DataFrame()  # Return an empty DataFrame if the table is not found
    
    # Extract table rows
    rows = table.find_all('tr')[1:]  # Skip the header row
    
    # Initialize lists to store the data
    data = []

    # Loop through the rows and extract data
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 0:
            stock_data = [col.get_text(strip=True) for col in columns]
            data.append(stock_data)
    
    # Create a DataFrame from the extracted data
    # Update the column names according to the actual data structure
    df = pd.DataFrame(data, columns=['Company', 'Current Price', 'Market Cap', 'P/E Ratio', 'Other Metrics'])  
    
    return df

# Call the function and print the DataFrame
penny_stocks = scrape_penny_stocks()
print(penny_stocks.head(20))  # Print the first 20 entries
