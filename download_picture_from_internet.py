import requests

# URL test 
url = 'https://photos.google.com/photo/AF1QipOpbVCfTJPc9EEKVR-DNzcj0LriBMqQHkRTIigb'
FILE_NAME = 'net_pic.jpg'

def main(url):
    """
    Use content manager to download picture,
    chunk prevent more memory usage.
    """
    r = requests.get(url, stream=True, timeout=3)
    if r.ok:
        with open(FILE_NAME, 'wb') as file:
            for chunk in r.iter_content(1024 * 100):
                file.write(chunk)
        print('Download complete')
    else:
        print('Error acquire')


if __name__ == '__main__':
    main(url)
