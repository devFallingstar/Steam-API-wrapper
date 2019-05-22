import requests
import time
from requests.exceptions import Timeout, RequestException

import xml.etree.ElementTree as ET


class SteamBasicCralwer:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.gameID_name_dict = dict()

    def __del__(self):
        pass

    def getUserSteamID(self, nickname):
        nickname = str(nickname)
        API_NAME = "ResolveVanityURL"
        API_VERSION = "v1"
        API_URL = "http://api.steampowered.com/ISteamUser/{}/{}/" \
                  "?key={}&vanityurl={}".format(API_NAME, API_VERSION, self.API_KEY, nickname)

    def getUserGameDetail(self, steam_id, max=0):
        steam_id = str(steam_id)
        API_NAME = "GetOwnedGames"
        API_VERSION = "v1"
        API_FORMAT = "json"
        API_URL = "https://api.steampowered.com/IPlayerService/{}/{}/" \
                  "?key={}&steamid={}&format={}&include_appinfo=1&include_played_free_games=1".format(API_NAME, API_VERSION, self.API_KEY, steam_id, API_FORMAT)

        response_raw = requests.get(API_URL)

        result = dict()

        try:
            response_json = response_raw.json()
            response_game_detail = dict(response_json)['response']['games']
        except Exception as e:
            return None

        print("---- Colleting info for "+steam_id)
        added_number = 0
        total = len(response_game_detail)
        for each_game_detail in response_game_detail:
            game_appid = str(each_game_detail['appid'])
            game_name = str(each_game_detail['name'])
            game_playtime = float(each_game_detail['playtime_forever']) / 60.0

            result[game_name] = game_playtime

            added_number += 1
            if added_number % 100 is 0 or added_number is total:
                print(str(added_number + 1) + " of " + str(total))

            if max is not 0:
                if added_number > max:
                    break

        return result

    def getGroupMembersID(self, group_name, start_page=1, end_page=0):
        group_name = str(group_name)
        start_page = start_page
        end_page = end_page
        wait_second = 1
        ids = []

        if end_page is 0:
            current_page = start_page

            while True:
                API_URL = 'https://steamcommunity.com/groups/{}/memberslistxml?xml=1&p={}'.format(group_name,
                                                                                                  current_page)

                response = requests.get(API_URL)
                response_raw = response.text

                if response.status_code == 200:
                    print("[OK] from {}".format(API_URL))
                    root = ET.fromstring(response_raw)
                    members = root.find('members')

                    if members is not None:
                        for steamid in members.findall('steamID64'):
                            ids.append(int(steamid.text))

                    current_page += 1
                    wait_second = 1
                elif response.status_code == 429:
                    print("Too many requests... Wait for {} seconds".format(wait_second))
                    time.sleep(wait_second)
                    wait_second *= 2
        else:
            for current_page in range(start_page, end_page):
                API_URL = 'https://steamcommunity.com/groups/{}/memberslistxml?xml=1&p={}'.format(group_name,
                                                                                                  current_page)
                response = requests.get(API_URL)
                response_raw = response.text

                if response.status_code == 200:
                    print("[OK] from {}".format(API_URL))
                    root = ET.fromstring(response_raw)
                    members = root.find('members')

                    if members is not None:
                        for steamid in members.findall('steamID64'):
                            ids.append(int(steamid.text))

                    current_page += 1
                    wait_second = 1
                elif response.status_code == 429:
                    print("[FAIL] from {}".format(API_URL))
                    print("Too many requests... Wait for {} seconds".format(wait_second))
                    time.sleep(wait_second)
                    wait_second *= 2

        return ids