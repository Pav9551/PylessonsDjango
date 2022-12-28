import requests
import re
import json
import pandas as pd
#http://google.github.io/proto-lens/installing-protoc.html
#https://habr.com/ru/post/680320/?ysclid=l6xpo6itvm552340478
from google.protobuf.json_format import MessageToJson#protobuf
import offers_pb2#

from django.core.management.base import BaseCommand
from blogapp.models import Category, Tag, Post, Good, Merchandise, Shop

def parse_page(city = "moskva", shop = "lenta-super", page_num = 25):
    """
    :param city: location of the shop
    :param shop: shop name
    :param page_num: parsed page number
    :return:  json.dumps
    """
    url = f"https://squark.edadeal.ru/web/search/offers?count=30&locality={city}&page={page_num}&retailer={shop}"
    data = requests.get(url, allow_redirects=True)  # data.content is a protobuf message
    offers = offers_pb2.Offers()  # protobuf structure
    offers.ParseFromString(data.content)  # parse binary data
    products: str = MessageToJson(offers)  # convert protobuf message to json
    products = json.loads(products)
    ret = json.dumps(products, indent=4, ensure_ascii=False, )
    return products
class ED:
    city = "moskva"
    shop = "lenta-super"
    GOODS = 'goods.xlsx'
    def __init__(self, CITY = city, SHOP = shop):
        self.city = CITY
        self.shop = SHOP
        self.excel_data_df = pd.DataFrame()
    def load_xlsx(self,search_goods=GOODS):
        self.search_goods = search_goods
        print(search_goods)
        self.excel_data_df = pd.read_excel(search_goods, sheet_name='Лист1')
        return self.excel_data_df
    def get_df_discount(self):
        i = 1;
        df_res = pd.DataFrame()
        ret = parse_page(city=self.city, shop=self.shop, page_num=i)
        print(f"запрос на сайт по магазину {self.shop}, ждите....")
        while (len(ret)>0):#перебор страниц
            df = pd.json_normalize(ret['offer'])
            df_res = pd.concat([df_res, df])
            i = i + 1
            ret = parse_page(city=self.city, shop=self.shop, page_num=i)
        df_res.reset_index(inplace=True, drop=True)
        #df_res.to_excel("output1.xlsx")
        self.df_res = df_res
        return df_res
    def search(self):
        order_columns = ['count','good', 'name']
        data_frame = pd.DataFrame()

        for good in self.excel_data_df.name:
            count = 0
            for good_discount in self.df_res.name:
                result = re.match(good, good_discount)
                if ((result is None) == False):
                    #print(count, good_discount)
                    df = pd.DataFrame({
                    'count': [count],
                    'good': [good],
                    'name': [good_discount]})
                    data_frame = pd.concat([data_frame, df])
                count = count + 1
        #data_frame.to_excel("output2.xlsx", index= False)
        data = data_frame.merge(self.df_res, on=['name'], how='left')
        data = data.drop_duplicates(subset=['name'])
        data.to_excel(f"{self.shop}.xlsx", index=False)
        print(f"Данные выгружены в файл {self.shop}.xlsx")
        return data
    def save_goods_to_base(self):
        for item in self.excel_data_df.name:
            good, created = Good.objects.get_or_create(name=item)
    def load_goods_from_base(self):
        goods = Good.objects.all()
        list_result = [entry.name for entry in goods]  # converts QuerySet into Python list
        data = {'name': list_result}
        self.excel_data_df = pd.DataFrame(data, columns=['name'])
        print(self.excel_data_df)
    def search_and_refrash(self):
        data_frame = pd.DataFrame()
        if self.df_res.empty:
            print(f'Магазин {self.shop} не предоставил скидки по данным товарам')
            return -1
        for good in self.excel_data_df.name:
            count = 0
            for good_discount in self.df_res.name:
                result = re.match(good, good_discount)
                if ((result is None) == False):
                    df = pd.DataFrame({
                    'count': [count],
                    'good': [good],
                    'name': [good_discount]})
                    data_frame = pd.concat([data_frame, df])
                count = count + 1
        data = data_frame.merge(self.df_res, on=['name'], how='left')
        data = data.drop_duplicates(subset=['name'])
        #data.to_excel(f"{self.shop}.xlsx", index=False)
        data = data.reset_index()
        #data_frame.to_excel("output2.xlsx", index=False)
        shop, created = Shop.objects.get_or_create(name=self.shop)
        for index, row in data.iterrows():
            print(row['good'],"-", row['name'])
            if (pd.isna(row['amount']) == True):
                row['amount'] = 0.0
            merch, created = Merchandise.objects.get_or_create(
                name=row['name'], good = row['good'], imageUrl = row['imageUrl'], priceBefore = row['priceBefore'],
                priceAfter=row['priceAfter'], amount=row['amount'], discount=row['discount'],
                startDate = row['startDate'], endDate = row['endDate'], market_name = self.shop, market = shop)
        print(f"Данные по {self.shop} выгружены в базу")
        return 0