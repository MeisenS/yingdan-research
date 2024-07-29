import json

# Initial data
data = {
    "user_id_list": [],
    "only_crawl_original": 0,
    "remove_html_tag": 1,
    "since_date": 365,
    "write_mode": ["csv"],
    "original_pic_download": 1,
    "retweet_pic_download": 1,
    "original_video_download": 1,
    "retweet_video_download": 0,
    "download_comment":1,
    "comment_max_download_count":1000,
    "download_repost": 1,
    "repost_max_download_count": 1000,
    "user_id_as_folder_name": 0,
    "cookie": "SCF=AhVr4U-KPHluOpRVKOU85t5-QZ9-2Uvdi_U8GJM8td8BDy0wi1wef_hygyR6eltQ7ha3H1xlHkiyDG1phG2qX-s.; SUB=_2A25Lmz6JDeRhGeFG7FsR9S_Jyj-IHXVo2T5BrDV6PUJbktANLVDVkW1NeN4rh18tmD0UzoTItt8LvKRZJ34mcdaC; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ndOxPPaaCajK-vZliNjcV5NHD95QN1hM4eh-pSK20Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0nN1K5feK-pe7tt; SSOLoginState=1721716441; ALF=1724308441; _T_WM=84314103091; XSRF-TOKEN=ebf3d4; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"
}

# List of user IDs to add
f = open('need.txt','r')

# Loop to add user IDs to the user_id_list
for user_id in f.readlines():
    data["user_id_list"].append(user_id[0:-1])

# Specify the file name
file_name = 'config1.json'

# Write the data to a json file
with open(file_name, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data has been written to {file_name}")
