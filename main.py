from SteamBasicCralwer import SteamBasicCralwer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['DEFAULT']['API_KEY']


def main():
    steam_crawler = SteamBasicCralwer(API_KEY=API_KEY)

    with open('user_list.txt', 'r') as user_list_file, open("user_info.csv", "a+") as user_info_file:
        user_id_list = list()

        for each_id in user_list_file:
            user_id_list.append(each_id)

        user_idx = 0
        for each_line in user_id_list:
            try:
                result = steam_crawler.getUserGameDetail(each_line)
            except KeyboardInterrupt:
                print("Go to next user")


            if result is not None:
                for each_key, each_item in result.items():
                    content = '{},{},play,{}\n'.format(each_line.strip(), each_key, each_item)
                    user_info_file.write(content)
                    user_info_file.flush()
                print("{} of {}".format(user_idx, len(user_id_list)))
                user_idx += 1



if __name__ == '__main__':
    main()
