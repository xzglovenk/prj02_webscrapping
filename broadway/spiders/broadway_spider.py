from scrapy import Spider, Request
from broadway.items import BroadwayItem
import re

class BroadwaySpider(Spider):
	name = 'broadway_spider'
	allowed_urls = ['https://www.tripadvisor.com']
	start_urls = ['https://www.tripadvisor.com/Attraction_Review-g60763-d1383285-Reviews-Jersey_Boys-New_York_City_New_York.html']

	def parse(self, response):

#		num_reviews = response.xpath('//div[@class="rs rating"]/a[@class="more"]/span/text()').extract_first()

		num_reviews = response.xpath('//div[@class="listContainer responsive"]/p/b[3]/text()').extract_first()
		num_reviews = int(num_reviews.replace(',', ''))
		last_page = num_reviews//10
		last_page2 = (last_page + 1)*10
		# print('#'*50)
		# print(num_reviews, last_page, last_page2)
		# print('#'*50)

		pagelist_urls = ["https://www.tripadvisor.com/Attraction_Review-g60763-d1383285-Reviews-Jersey_Boys-New_York_City_New_York.html"] + ["https://www.tripadvisor.com/Attraction_Review-g60763-d1383285-Reviews-or{}-Jersey_Boys-New_York_City_New_York.html".format(i) for i in range(10, last_page2, 10)]

		for url in pagelist_urls:
			#print(url)
			yield Request(url = url, callback = self.parse_review_page)

	def parse_review_page(self, response):
		reviews_urls = response.xpath('//div[@class="prw_rup prw_reviews_basic_review_responsive"]//div[@class="wrap"]//a/@href').extract()

		# print('#'*50)
		# print(len(reviews_urls))
		# print('#'*50)
		

		for url in reviews_urls[::2]:
			
			yield Request(url = "https://www.tripadvisor.com"+url, callback = self.parse_detail_page)

	def parse_detail_page(self, response):
		showname = response.xpath('//div[@id="listing_main_sur"]//div[@class="surContent"]/a/text()').extract_first().strip()
		title = response.xpath('//div[@class="wrap"]//span[@class="noQuotes"]/text()').extract_first()
		text_temp = response.xpath('//div[@class="listContainer responsive"]')[0]
		full_text = " ".join(text_temp.xpath('.//div[@class="entry"]/p/text()').extract())
		rating = response.xpath('//div[@id="HEADING_GROUP"]//div[@class="rating"]/span/span/@alt').extract_first()
		rating = re.search('\d+', rating).group()
		date = text_temp.xpath('.//span[@class="ratingDate relativeDate"]/@title').extract_first()
		user = text_temp.xpath('//div[@class="username mo"]/span[@class="expand_inline scrname"]/text()').extract_first()
		contribution, helpful = text_temp.xpath('//div[@class="memberBadgingNoText"]/span[@class="badgetext"]/text()').extract()[:2]



		# print('#'*50)
		# print(title)
		# print(full_text)
		# print(rating)
		# print(date)
		# print(user)
		# print(contribution)
		# print(helpful)
		# print('#'*50)

		item = BroadwayItem()
		item['showname'] = showname
		item['title'] = title
		item['full_text'] = full_text
		item['rating'] = rating
		item['date'] = date
		item['user'] = user
		item['contribution'] = contribution
		item['helpful'] = helpful
		# item['user_answers'] = user_answers
		# item['user_questions'] = user_questions
		# item['user_join'] = user_join
		yield item

	
		# vote = response.xpath('//div[@class="vote"]/span[@itemprop="upvoteCount"]/text()').extract_first()
		# user = response.xpath('//div[@class="question"]//div[@class="post-signature owner grid--cell fl0"]//div[@class="user-info "]//a/text()').extract_first()
		# answer = response.xpath('//div[@id="answers"]//h2/@data-answercount').extract_first()
		# viewed = response.xpath('//div[@class="module question-stats"]/table//tr[2]/td[2]/p/b/text()').extract_first()
		# date = response.xpath('//div[@class="module question-stats"]/table//tr[1]/td[2]/p/@title').extract_first()
		# viewed = re.search('\d+', viewed.replace(',', '')).group()
		# date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', date).group()
		# user_url = response.xpath('//div[@class="question"]//div[@class="post-signature owner grid--cell fl0"]//div[@class="user-info "]//a/@href').extract_first()
		# user_urlfull = "https://stackoverflow.com/"+user_url

