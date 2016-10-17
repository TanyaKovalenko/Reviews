import csv
with open('eggs.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
     	#spamwriter = csv.writer(csvfile, delimiter=' ',
        #                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
     	spamwriter.writerow(['ra,bbit1', 'rabbit2', 'rabbit3'])
reader = csv.reader(open('eggs.csv'), delimiter=',', quotechar='"')
for row in reader:
	print (str(row[0]) + '\n')
