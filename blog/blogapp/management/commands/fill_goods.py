from django.core.management.base import BaseCommand
from blogapp.models import Merchandise

from edadeal import ED
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
goods_path = (BASE_DIR / 'goods.xlsx').__str__()

class Command(BaseCommand):
    def handle(self, *args, **options):
        Merchandise.objects.all().delete()

        lenta = ED(CITY="moskva", SHOP="lenta-super")  # создаем экземпляр класса
        lenta.load_xlsx(goods_path)  # загружаем интересующие нас товары из файла
        lenta.save_goods_to_base()  # сохраняем список интересующих нас товаров в базу через ORM
        lenta.get_df_discount()  # запрашиваем список товаров со скидками с сайта
        lenta.search_and_refrash()  # сопоставляем искомые товары с перечнем скидок и сохраняем в базу

        pyterochka = ED(CITY="moskva", SHOP="5ka")  # создаем экземпляр класса
        pyterochka.load_xlsx(goods_path)  # загружаем интересующие нас товары из файла
        pyterochka.save_goods_to_base()  # сохраняем список интересующих нас товаров в базу через ORM
        pyterochka.get_df_discount()  # запрашиваем список товаров со скидками с сайта
        pyterochka.search_and_refrash()  # сопоставляем искомые товары с перечнем скидок и сохраняем в базу

        perekrestok = ED(CITY="moskva", SHOP="perekrestok")  # создаем экземпляр класса
        perekrestok.load_xlsx(goods_path)  # загружаем интересующие нас товары из файла
        perekrestok.save_goods_to_base()  # сохраняем список интересующих нас товаров в базу через ORM
        perekrestok.get_df_discount()  # запрашиваем список товаров со скидками с сайта
        perekrestok.search_and_refrash()  # сопоставляем искомые товары с перечнем скидок и сохраняем в базу











