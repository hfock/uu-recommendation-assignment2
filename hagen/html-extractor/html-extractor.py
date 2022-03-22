import glob
import pandas as pd
from bs4 import BeautifulSoup
import json


def extract_data(files):
    extracted_data = []
    for index, file in enumerate(files):
        if './data/show' not in file:
            soup = BeautifulSoup(open(file), 'html.parser')
            print(file)

            if soup.find('meta', attrs={'property': 'og:description'}):
                description = soup.find('meta', attrs={'property': 'og:description'})['content']
            else:
                description = ''

            if soup.find('meta', attrs={'name': 'keywords'}):
                keywords = soup.find('meta', attrs={'name': 'keywords'})['content']
            else:
                keywords = ''

            # Extract Json
            if soup.find(id="tvip-script-app-store"):
                json_raw = soup.find(id="tvip-script-app-store")
                json_raw = json_raw.get_text()
                json_raw = json_raw.partition("__IPLAYER_REDUX_STATE__ = ")
                stripped_text = json_raw[2][:len(json_raw[2]) - 1]
                jsonfile = json.loads(stripped_text)

                episode_ = jsonfile['episode']
                title = episode_['title']

                synopses_ = episode_['synopses']
                if 'large' in synopses_:
                    synops_long = synopses_['large']
                else:
                    synops_long = ''
                if 'medium' in synopses_:
                    synops_med = synopses_['medium']
                else:
                    synops_med = ''
                if 'small' in synopses_:
                    synops_small = synopses_['small']
                else:
                    synops_small = ''

                if 'images' in episode_:
                    image = episode_['images']['standard']
                else:
                    image = ''

                category = ''
                if 'labels' in episode_:
                    labels_ = episode_['labels']
                    if 'category' in labels_:
                        category = labels_['category']

                channel = episode_['masterBrand']['id']
                versions_ = jsonfile['versions'][0]
                language = versions_['guidance']
                if 'firstBroadcast' in versions_:
                    release_date = versions_['firstBroadcast']
                else:
                    release_date = ''
                duration_sec = versions_['duration']['seconds']
            else:
                title = ''
                synops_long = ''
                synops_med = ''
                synops_small = ''
                category = ''
                channel = ''
                language = ''
                release_date = ''
                duration_sec = ''
                image = ''

            article = {
                'id': index,
                'title': title,
                'description': description,
                'image': image,
                'keywords': keywords,
                'synopses_small': synops_small,
                'synops_med': synops_med,
                'synops_long': synops_long,
                'category': category,
                'channel': channel,
                'language': language,
                'release_date': release_date,
                'duration_sec': duration_sec,
                'topic': file.split('/', 5)[4]
            }
            # append the article to the data
            extracted_data.append(article)
    return extracted_data


if __name__ == '__main__':
    files = []

    # load html files
    ROOT = "./../../data/BBC/*"
    folders = glob.glob(ROOT)
    for folder in folders:
        files.append(glob.glob(f'{folder}/*.html'))
    files = [item for sublist in files for item in sublist]

    data = extract_data(files)

    df = pd.DataFrame.from_records(data, index='id')

    df.to_csv('./../bbc_data.csv', sep=';')
