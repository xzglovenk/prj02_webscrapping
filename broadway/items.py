# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BroadwayItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	showname = Field()
	title = Field()
	full_text = Field()
	rating = Field()
	date = Field()
	user = Field()
	contribution = Field()
	helpful = Field()