import requests
import re
import json
from bs4 import BeautifulSoup

def get_bilibili_video_url(bv_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.34103.61 Saf6 (KHTML, like Gecko) Chrome/83.0.ari/537.36',
        'Referer': f'https://www.bilibili.com/video/{bv_id}'
    }
    # 获取视频页面源代码
    url = f'https://www.bilibili.com/video/{bv_id}'
    response = requests.get(url, headers=headers)
    html = response.text

    # 解析页面源代码，提取视频的aid和cid
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', string=re.compile('window.__INITIAL_STATE__'))
    script_content = script_tag.string if script_tag else ''

    # 提取视频的aid和cid
    initial_state = re.search(r'window\.__INITIAL_STATE__=(.*?);\(function', script_content).group(1)
    initial_state_json = json.loads(initial_state)
    aid = initial_state_json['videoData']['aid']
    cid = initial_state_json['videoData']['cid']

    # 调用Bilibili API获取视频URL
    api_url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=80&otype=json&platform=html5&mid=3546655666211109'
    api_response = requests.get(api_url, headers=headers).json()

    if api_response['code'] != 0:
        return None

    # 选择最优的URL
    video_url = None
    for durl in api_response['data']['durl']:
        if 'upos' in durl['url']:
            video_url = durl['url']
            break

    if video_url is None:
        video_url = api_response['data']['durl'][0]['url']

    return video_url

# 示例Bilibili视频BV号,将bv_id改为目标视频的BV号，整个代码只需这一处修改
bv_id = 'BV14KzVY9Ebi'
video_url = get_bilibili_video_url(bv_id)

if video_url:
    print('Video URL:', video_url)
else:
    print('Failed to retrieve video URL')
