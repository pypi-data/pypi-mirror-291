# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class ValidationPipeline:
    def process_item(self, item, spider):
        print(" Nothing special for working")
        return item


class MongoPipeline:
    # 몽고 데이터 베이스에 저장하는 파이프라인
    def process_item(self, item, spider):
        """
        아이템 구조
            title = scrapy.Field()
            date = scrapy.Field()
            value = scrapy.Field()
        """
        print(f"\tIn the {self.__class__.__name__}...", end="")
        if spider.mongo_client is None:
            print(f"Skip for saving the data... date : {item['date']} / title : {item['title']} / value : {item['value']}")
        else:
            print(f"Saving the {spider.name} to mongoDB...date : {item['date']} / title : {item['title']} / value : {item['value']}")
            mongo.MI(spider.mongo_client, item['title']).save_dict({"date": item['date'], "value": item['value']})
        return item