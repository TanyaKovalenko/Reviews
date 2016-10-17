# coding=utf-8
import scrapy
import csv

class MailSpider(scrapy.Spider):
        name = "mail_spider"

        def start_requests(self):
                urls = set()

                for page_inx in range(1, 3):
        
	                # ************* SITILINK **************
			#sitilink (all cities) #21 pages
			#urls.add('http://torg.mail.ru/review/shops/sitilink-cid1917/?page=' + str(page_inx))
			
			# ************* ULMART **************
			#ulmart Moscow #11 pages
			#urls.add('http://torg.mail.ru/review/shops/yulmart-cid3032/?page=' + str(page_inx))
                	#ulmart SPb #7 pages
			#urls.add('http://torg.mail.ru/review/shops/yulmart-spb-cid4448/?page=' + str(page_inx))
			#ulmart (other cities) # 3 pages
			#urls.add('http://torg.mail.ru/shop/yulmart-novorossijsk-cid10375/?page=' + str(page_inx))
			#urls.add('http://torg.mail.ru/review/shops/yulmart-tver-cid4967/?page=' + str(page_inx))
			#urls.add('http://torg.mail.ru/review/shops/yulmart-kazan-cid9519/?page=' + str(page_inx))
			#urls.add('http://torg.mail.ru/shop/yulmart-yaroslavl-cid6354/?page=' + str(page_inx))
			#urls.add('http://torg.mail.ru/shop/yulmart-nizhnij-novgorod-cid10376/?page=' + str(page_inx))
	
		urls_list = list(urls)

                for url in urls_list:
                        yield scrapy.Request(url=url, callback=self.parse)

        def __init__(self, category=None, *args, **kwargs):
                super(MailSpider, self).__init__(*args, **kwargs)

                self.visited_urls = set()

                with open('mail_ulmart_visited_urls', 'r') as fin:
                        for line in fin:
                                url = line.strip()
                                self.visited_urls.add(url)	


	def parse(self, response):
		if response.url in self.visited_urls:
                        return

                filename = 'ulmart_result.csv'
                
		comments = [sel.extract() for sel in response.xpath('//div[re:test(@class, "review_item")]')]		

		if len(comments) != 0:
                         with open('mail_ulmart_visited_urls', 'a') as f:
                                f.write(response.url + '\n')
		else: 
			return

		for comment in comments:
			start_rating_counter = comment.find('review-item__rating-counter') + len('review-item__rating-counter') + 2
                        end_rating_counter = comment.find('</span>', start_rating_counter)
			rating_counter = comment[start_rating_counter:end_rating_counter].strip()
			
			start_comment = 0
			button_counter_vote = set()
			
			for vote_inx in range (1, 3): 
                        	start_button_counter_vote = comment.find('button__counter button__counter_vote', start_comment) + len('button__counter button__counter_vote') + 2
                                end_button_counter_vote = comment.find('</span>', start_button_counter_vote)
				if vote_inx == 1:
					plus_button_counter_vote = int( comment[start_button_counter_vote:end_button_counter_vote].strip() )
				else:
					minus_button_counter_vote = int( comment[start_button_counter_vote:end_button_counter_vote].strip() )
				
				start_comment = end_button_counter_vote + 7
			
			with open(filename, 'a') as csvfile:
                        	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')

				start_comment = comment.find('review-item__paragraph') + len('review-item__paragraph') + 2
                               	end_comment = comment.find('</p>', start_comment)
                               	comment = comment[start_comment:end_comment].strip()
                               	comment = comment.replace('&lt;br /&gt;', '\n')
                               	comment = comment.replace('<br>', '')
                               	comment = comment.replace('\n', '')
                               	comment = comment.replace('\r', '')
                               	comment = comment.replace('\t', '')
                               	comment = comment.replace('!', '.')
                               	comment = comment.replace('?', '.')
                               	comment = comment.strip()
     
				spamwriter.writerow([comment.encode('utf-8'), rating_counter, plus_button_counter_vote, minus_button_counter_vote])					
		
		self.log('Saved file %s' % filename)
