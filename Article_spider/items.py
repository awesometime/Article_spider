# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
import datetime
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader


def date_convert(value): # value 即item 的每个字段，如 title create_date
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now()
    return create_date


def get_nums(values):  # value 即item 的每个字段，如 title create_date
    match_re = re.match(".*?(\d+).*", values)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    # 去掉tags中提取的评论
    if "评论" in value:
        return  ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
        output_processor = TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    #  front_image_url 须为 list
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)
    )

    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(input_processor = MapCompose(get_nums))
    comment_nums = scrapy.Field(input_processor = MapCompose(get_nums))
    fav_nums = scrapy.Field(input_processor = MapCompose(get_nums))
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor = Join(",")
    )
    content = scrapy.Field()

