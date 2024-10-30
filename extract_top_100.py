

import requests
from bs4 import BeautifulSoup
import json

# url = 'https://nrf.com/research-insights/top-retailers/top-100-retailers/top-100-retailers-2024-list'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

with open('NRF _ Top 100 Retailers 2024 List.html') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find the table and iterate over its rows
table = soup.find('table')
rows = table.find_all('tr')

data = []

for i, row in enumerate(rows):
    columns = row.find_all('td')
    if len(columns) > 0:
        retailer_data = {
            'Rank': int(columns[0].get_text(strip=True)),
            'Company': columns[1].get_text(strip=True),
            'Headquarters': columns[2].get_text(strip=True),
            'YOY Growth (%)': float(columns[3].get_text(strip=True)[:-1]),
            'US Sales ($B)': float(columns[4].get_text(strip=True)[1:]),
            'World Sales ($B)': float(columns[5].get_text(strip=True)[1:]),
            'US % of World': float(columns[6].get_text(strip=True)[:-1]),
            'US Stores': 'N/A' if columns[7].get_text(strip=True) == 'N/A' else int(columns[7].get_text(strip=True).replace(',', '')),
            'Store Growth (%)': 'N/A' if columns[8].get_text(strip=True) == 'N/A' else float(columns[8].get_text(strip=True)[:-1]),
            'Notes': columns[9].get_text(strip=True)
        }
        data.append(retailer_data)

# Convert to JSON
json_data = json.dumps(data, indent=4)

# Write to a file
with open('top_100_retailers.json', 'w') as json_file:
    json_file.write(json_data)

print("Data saved to top_100_retailers.json")







# import requests
# from bs4 import BeautifulSoup
# import json
#
# url = 'https://nrf.com/research-insights/top-retailers/top-100-retailers/top-100-retailers-2024-list'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
#
# # Find the table and iterate over its rows
# table = soup.find('table')  # Adjust this selector based on inspection
# rows = table.find_all('tr')
#
# data = []
#
# for row in rows:
#     # Extract basic row data
#     columns = row.find_all('td')
#     if len(columns) > 0:
#         retailer_data = {
#             'Rank': columns[0].get_text(),
#             'Company': columns[1].get_text(),
#             # Add other fields here based on your needs
#         }
#
#         # You might need to extract additional data from expanded sections, if available
#         # Example of fetching additional information
#         expanded_row = row.find_next_sibling()  # Adjust logic based on HTML structure
#         if expanded_row and 'expanded' in expanded_row.get('class', []):
#             additional_info = expanded_row.get_text()  # Parse accordingly
#             retailer_data['AdditionalInfo'] = additional_info
#
#         data.append(retailer_data)
#
# # Convert to JSON
# json_data = json.dumps(data, indent=4)
#
# # Write to a file
# with open('top_100_retailers.json', 'w') as json_file:
#     json_file.write(json_data)
#
# print("Data saved to top_100_retailers.json")
