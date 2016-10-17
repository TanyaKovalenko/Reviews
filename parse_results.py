# coding=utf-8
import csv

with open('/Users/ruslan/Tanya/MailSpider/MailSpider/spiders/ulmart_result.csv', 'r') as res_file:
	reader = csv.reader(res_file, delimiter=',', quotechar='"')
	
	for comment in reader:
		
		with open('sitilink_in_ulmart.csv', 'a') as ulmart_in_sitilink_file:
			
			writer = csv.writer(ulmart_in_sitilink_file, delimiter=',', quotechar='"')
			com = str(comment[0]).decode('utf-8')			
			
			if u"ситилинк".upper() in com.upper():
				
				comment_text = com.split('.')
				
				for sentence in comment_text:
					
					if u"ситилинк".upper() in sentence.upper():
						writer.writerow([sentence.encode('utf-8') + '. ', comment[1], comment[2], comment[3]])
					
