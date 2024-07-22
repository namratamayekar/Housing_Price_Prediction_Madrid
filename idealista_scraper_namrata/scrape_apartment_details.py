import json
import requests
from bs4 import BeautifulSoup



def scrape_apartment_details(json_file_path, output_file, bad_output_file, min_value, max_value):
    prelim_data = []
    combined_data = []
    failed_data = []
    with open(json_file_path, 'r', encoding='utf-8') as f: 
        data = json.load(f)
        prelim_data.extend(data)
    scraper_api_key = 'enter_api_key'
    print(len(prelim_data))
    for index, item in enumerate(prelim_data):
        if index<=max_value and index>=min_value:
            print('Index:', index)
            print('Min_value:', min_value)
            print('Max_value:', max_value)
            payload = { 'api_key': scraper_api_key, 'url': f'https://www.idealista.com{item["Url"]}' }
            response = requests.get('https://api.scraperapi.com/', params=payload)
            print('Index', index, '-', 'Response HTTP Status Code: ', response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                div_with_comments = soup.find('div', class_='adCommentsLanguage')
                if div_with_comments:
                    full_description = div_with_comments.find('p').text.strip()
                else:
                    full_description = None
                item['Full description'] = full_description
                item['Short description'] = item['Description']
                del item['Description']
                property_details = soup.find('div', class_='details-property')
                features = []
                try:
                    feature_list = property_details.find_all('li')
                    for feature in feature_list:
                        features.append(feature.text.strip())
                except:
                    print('no features found')
                item['Features'] = features
                combined_data.append(item)
            else:
                failed_data.append(item)
    with open(f'{output_file}_{min_value}_{max_value}.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    with open(f'{bad_output_file}_{min_value}_{max_value}.json', 'w', encoding='utf-8') as f:
        json.dump(failed_data, f, ensure_ascii=False, indent=2)


start=0
end=9

while end <= 1100:
    scrape_apartment_details('failed_apartments_all_namrata.json', 'namrata_retry_apartments_final', 'namrata_retry_apartments_failed', start,end)
    start+=10
    end+=10


