# -*- coding: utf-8 -*-
import datetime
import scrapy
import re
from scrapy.http import Request
from scrapy.loader import ItemLoader
from urllib import parse
from Article_spider.items import JobBoleArticleItem, ArticleItemLoader
from Article_spider.utils.common import get_md5

#print('11')
class JobboleSpider(scrapy.Spider):
    """
    功能：爬取
    """
    # 爬虫名

    name = "jobbole"
    # 爬虫作用范围
    allowed_domains = ["blog.jobbole.com"]
    start_url = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取当前页面中所有文章列表的url，并交给scrapy下载，解析
        2. 获取下一页url 并交给scrapy下载，解析
        :param response:
        :return:
        """
        # extract()后为数组
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        # 效果一样  class='post floated-thumb'   .post .floated-thumb 不行
        # post_urls = response.css('#archive .post.floated-thumb .post-thumb a::attr(href)').extract()
        for post_node in post_nodes:
            # 可以取到每页的20个文章的图片的url
            image_url = post_node.css("img::attr(src)").extract_first("")
            # 可以取到每页的20个文章的url
            post_url = post_node.css("::attr(href)").extract_first("")

            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        # 数组为空时extract()[0]会报错index溢出,extract_first()不会，封装好了，空就返回none
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        """
        # 封面图  此字段必须为list
        front_image_url = response.meta.get("front_image_url", "")

        title = response.css('.entry-header h1::text').extract()[0]

        # 找到class=entry-meta-hide-on-mobile的p的内容,p 可省略
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        # 找到class=vote-post-up的span的内容,span 可省略
        praise_nums = int(response.css("span.vote-post-up h10::text").extract()[0])

        fav_nums = response.css("span.bookmark-btn::text").extract()[0]
        # fav_nums = ' 3 收藏'
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        # 正文
        content = response.css("div.entry").extract()[0]

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endwith('评论')]
        # tag_list = ['IT技术', 'Redis', '数据库']
        tags = ",".join(tag_list)
        # tags = 'IT技术,Redis,数据库'

        article_item["title"] = title
        article_item["front_image_url"] = [front_image_url]  # list

        # 将字符串 create_date 变成datetime类型
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now()
        article_item["create_date"] = create_date

        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["url_object_id"] = get_md5(response.url)
        article_item["content"] = content
        article_item["tags"] = tags
        """


        # 通过 item_loader 加载 item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", '.entry-header h1::text')
        item_loader.add_css("create_date", 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_css("praise_nums", 'span.vote-post-up h10::text')
        item_loader.add_css("fav_nums", 'span.bookmark-btn::text')
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])

        article_item = item_loader.load_item()
        # 将item传递到pipelines
        yield article_item
        # print('22')


print('33')

