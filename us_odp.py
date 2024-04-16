import requests
import pandas as pd
import os
import string
import logging


def clean_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    cleaned_filename = cleaned_filename.replace(' ', '_')  # Replace spaces with underscore
    return cleaned_filename


# Set up logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(message)s')

# Make a GET request to the data.gov API
response = requests.get("https://catalog.data.gov/api/3/action/package_search")

# Convert the response to JSON
data = response.json()

# Create a directory for the datasets
path = "/Volumes/YING/Datasets/Feature_Discovery/us_odp"
os.makedirs(path, exist_ok=True)

# Download the CSV files
count = 0
for dataset in data['result']['results']:
    for resource in dataset['resources']:
        if resource['format'].lower() == 'csv':
            url = resource['url']
            filename = clean_filename(dataset['title']) + '.csv'
            logging.info(f'Downloading {url} to {filename}')

            try:
                data = pd.read_csv(url)
                data.to_csv(f'{path}/{filename}', index=False)
                count += 1
            except Exception as e:
                logging.info(f'Could not download {url} because {str(e)}')

            break  # only download the first CSV file for each dataset
    if count >= 10:  # limit the number of datasets for this demo
        break

logging.info('Finished downloading datasets')

# import requests
# import pandas as pd
# import os
# import string
#
#
# def clean_filename(filename):
#     valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
#     cleaned_filename = ''.join(c for c in filename if c in valid_chars)
#     cleaned_filename = cleaned_filename.replace(' ', '_')  # Replace spaces with underscore
#     return cleaned_filename
#
#
# # Make a GET request to the data.gov API
# response = requests.get("https://catalog.data.gov/api/3/action/package_search")
#
# # Convert the response to JSON
# data = response.json()
#
# # Create a directory for the datasets
# path = "/Volumes/YING/Datasets/Feature_Discovery/us_odp"
# os.makedirs(path, exist_ok=True)
#
# # Download the CSV files
# count = 0
# for dataset in data['result']['results']:
#     for resource in dataset['resources']:
#         if resource['format'].lower() == 'csv':
#             url = resource['url']
#             filename = clean_filename(dataset['title']) + '.csv'
#             print(f'Downloading {url} to {filename}')
#
#             try:
#                 data = pd.read_csv(url)
#                 data.to_csv(f'{path}/{filename}', index=False)
#                 count += 1
#             except Exception as e:
#                 print(f'Could not download {url} because {str(e)}')
#
#             break  # only download the first CSV file for each dataset
#     if count >= 1000:  # limit the number of datasets for this demo
#         break
#
# print('Finished downloading datasets')