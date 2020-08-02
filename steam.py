import requests
from bs4 import BeautifulSoup
import time
import re

def main():
    try:
        search_Url = "https://steamcommunity.com/market/search?norender=1&q="
        print("Введите url товара")
        url = input()
        r = requests.get(url).text
        soup = BeautifulSoup(r, "lxml")
        script_list = soup.find_all('script', {'type':'text/javascript'})
        assetIds = soup.find_all('div', class_="market_listing_buy_button")
        inspection_script = str(script_list[25]).strip()
        find_links = [m.start() for m in re.finditer("steam:", inspection_script)]
        api_url = "https://api.csgofloat.com/?url="
        link_list = []
        asset_list = []
        asset_href = []
        listingid_list = []
        info_list = []
        sticker_name_list = []
        stickers_info_list = []
        sticker_id_list = []
        print("Подключился к стиму")

        for i in range(len(find_links)):
            d=find_links[i]
            current_word = inspection_script[d]
            full_word = ""
            while current_word != '"':
                current_word = inspection_script[d]
                full_word += current_word 
                d += 1
            full_word = full_word.replace('"', "")
            full_word = full_word.replace('\\', "")
            link_list.append(full_word)
        del link_list[1::2]
        print("Скрипты найдены")

        for i in range(len(link_list)):
            if "listingid" in link_list[i]: 
                listingid_list.append(i)
        print("Ненужные ссылки найдены")

        for i in range(listingid_list[-1], listingid_list[0]-1, -1): 
            del link_list[i]
        print("Ненужные ссылки удалены")

        for assetId in assetIds:
            asset_href.append(assetId.find('a').get('href'))
        print("Ассеты получены")

        asset_href = str(asset_href).strip()
        find_asset = [m.start() for m in re.finditer("'\)", asset_href)]
        for i in range(len(find_asset)):
            d = find_asset[i]-1
            current_word = asset_href[d]
            full_word = ""
            while current_word != "'":
                current_word = asset_href[d]
                full_word += current_word 
                d -= 1
            full_word = full_word.replace("'", "")[::-1]
            asset_list.append(full_word)
        print("Ассеты отредактированы")

        for i in range(len(link_list)):
            link_list[i] = link_list[i].replace("%assetid%", asset_list[i])
            info_list.append(requests.get(api_url + link_list[i]).json())
        print("Инспект линки сгенирированы и получена json информация")

        for i in range(len(info_list)):
            if len(info_list[i]['iteminfo']['stickers']) != 0:
                sticker_group_list = []
                for d in range(len(info_list[i]['iteminfo']['stickers'])):
                    sticker_group_list.append("Sticker | " + info_list[i]['iteminfo']['stickers'][d]['name'])
                sticker_name_list.append(sticker_group_list)
            else:
                sticker_name_list.append(None)
        print("Список стикеров составлен")

        for i in range(len(sticker_name_list)):
            if sticker_name_list[i] != None:
                sticker_group_list = []
                print(f"=============\n{i}\n=============\n{len(sticker_name_list)}\n===============")
                for d in range(len(sticker_name_list[i])):
                    sticker_group_list.append(
                        {
                            'name':sticker_name_list[i][d],
                            'price':BeautifulSoup(requests.get(search_Url + sticker_name_list[i][d]).text, 'lxml').find(class_="market_table_value normal_price").find('span', class_="normal_price").get_text()
                        }
                    )
                stickers_info_list.append(sticker_group_list)
            else:
                stickers_info_list.append(None)
        print("Цена стикеров получена")
        print(stickers_info_list)
    except:
        print("Скорее всего стим заблочил")

if __name__ == "__main__":
    main()
