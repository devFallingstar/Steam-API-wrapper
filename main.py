from SteamBasicCralwer import SteamBasicCralwer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['DEFAULT']['API_KEY']


def main():
    steam_crawler = SteamBasicCralwer(API_KEY=API_KEY)

    # print(steam_crawler.getUserGameDetail('76561198045530158'))

    with open('user_list.txt', 'w') as file:
        users_list = steam_crawler.getGroupMembersID('tradingcards', start_page=1)

        for each_user_id in users_list:
            file.write(str(each_user_id)+'\n')


if __name__ == '__main__':
    main()
