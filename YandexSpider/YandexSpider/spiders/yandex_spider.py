# coding=utf-8
import scrapy
import csv

class YandexSpider(scrapy.Spider):
	name = "yandex_spider"

	def start_requests(self):
		urls = set()
		#5508
		#5077
		for page_inx in range(1, 5508):
			if 'https://market.yandex.ru/shop/17436/reviews?page_num=' + str(page_inx) not in self.visited_urls:
				urls.add('https://market.yandex.ru/shop/17436/reviews?page_num=' + str(page_inx))
			#if 'https://market.yandex.ru/shop/18063/reviews?page_num=' + str(page_inx) not in self.visited_urls:
				#urls.add('https://market.yandex.ru/shop/18063/reviews?page_num=' + str(page_inx))

		urls_list = list(urls)
	
		for url in urls_list:
			yield scrapy.Request(url=url, callback=self.parse)

	def __init__(self, category=None, *args, **kwargs):
        	super(YandexSpider, self).__init__(*args, **kwargs)
		
		self.visited_urls = set()
		#with open('yandex_ulmart_visited_urls', 'r') as fin:
		with open('yandex_sitilink_visited_urls', 'r') as fin:
            		for line in fin:
                		url = line.strip()
                		self.visited_urls.add(url)
		
	def parse(self, response):
		if response.url in self.visited_urls:
            		return
	        #filename = 'ulmart_result.csv'
		filename = 'sitilink_result.csv'
		
		no_review_text = [sel.extract() for sel in response.xpath('//dd[re:test(@class, "n-product-default-offer__no-modifications_text")]')]

		if len(no_review_text) != 0:
			return

        	comments = [sel.extract() for sel in response.xpath('//div[re:test(@class, "product-review-item ")]')]
		
		if len(comments) != 0:
			 #with open('yandex_ulmart_visited_urls', 'a') as f:
			 with open('yandex_sitilink_visited_urls', 'a') as f:
                         	f.write(response.url + '\n')
        	
		with open(filename, 'a') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')		
                	for comment in comments:
				
				start_comment_mark = comment.find('data-rate="') + len('data-rate="')
				end_comment_mark = comment.find('"', start_comment_mark)
				comment_mark = comment[start_comment_mark:end_comment_mark].strip()

				start_review_voting_plus = comment.find('review-voting__plus')
                                end_review_voting_plus = comment.find('</div>', start_review_voting_plus)
                                review_voting_plus = comment[start_review_voting_plus:end_review_voting_plus].strip()

                                start_review_voting_plus_num = review_voting_plus.find('review-voting__num') + len('review-voting__num') + 2
                                end_review_voting_plus_num = review_voting_plus.find('</span>', start_review_voting_plus_num)
                                review_voting_plus_num = review_voting_plus[start_review_voting_plus_num:end_review_voting_plus_num].strip()

				start_review_voting_minus = comment.find('review-voting__minus')
                                end_review_voting_minus = comment.find('</div>', start_review_voting_minus)
                                review_voting_minus = comment[start_review_voting_minus:end_review_voting_minus].strip()
				
				start_review_voting_minus_num = review_voting_minus.find('review-voting__num') + len('review-voting__num') + 2
                                end_review_voting_minus_num = review_voting_minus.find('</span>', start_review_voting_minus_num)
                                review_voting_minus_num = review_voting_minus[start_review_voting_minus_num:end_review_voting_minus_num].strip()
				
				start_comment = 0
				comment_text = ''
                                
				while comment.find('product-review-item__text', start_comment) != -1:					
					start_comment_part = comment.find('product-review-item__text', start_comment) + len('product-review-item__text') + 2
                              		end_comment_part = comment.find('</div>', start_comment_part)
                                	
					if end_comment_part != -1:
						end_comment_part_ = comment.find('</dd>', start_comment_part)
						if end_comment_part_ != -1:
							end_comment_part = min(end_comment_part, end_comment_part_)
					else:
						comment_part_text = comment_part_text.replace('<br>', '')
						end_comment_part = comment.find('</dd>', start_comment_part)
					
					start_comment = end_comment_part + 5
					
					comment_part_text = comment[start_comment_part:end_comment_part].strip()
                                	comment_part_text = comment_part_text.replace('&lt;br /&gt;', '\n')
                               		comment_part_text = comment_part_text.replace('<br>', '')
                                	comment_part_text = comment_part_text.replace('\n', '')
                                	comment_part_text = comment_part_text.replace('\r', '')
                                	comment_part_text = comment_part_text.replace('\t', '')
					comment_part_text = comment_part_text.replace('!', '.')
					comment_part_text = comment_part_text.replace('?', '.')
                                	comment_part_text = comment_part_text.strip()
                                	
					if comment_part_text[len(comment_part_text) - 1] != '.':
						comment_part_text += "."

					comment_text += " " + comment_part_text

				spamwriter.writerow([comment_text.encode('utf-8'), comment_mark, review_voting_plus_num, review_voting_minus_num])	
		
		self.log('Saved file %s' % filename)
 
