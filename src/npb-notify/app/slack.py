import urllib3, json, os, re

http = urllib3.PoolManager()
url = os.getenv('NPB_WEBHOOK_URL_SLACK_DEV', '')
if not url:
    url = os.environ['WEBHOOK_URL']


def push(title, message, rgb):
    # post to slack without attachments
    if message:
        text = f'{title}\n\n{message}'
    else:
        text = f'{title}\n\n'
    msg = {
        'attachments': [
            {
                'title': '',
                'color': rgb,
                'text': text
            }
        ]
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    print({'title': title, 'message': message, 'status_code': resp.status, 'response': resp.data, })
