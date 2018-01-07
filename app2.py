import requests
from lxml import html
import csv
import pandas as pd
import time
from random import randint
# package = ['adractive.com.adractive',
# 'aflatoon.apps.aflatoonapps.mahilasharir',
# 'air.com.epic.hinducalendarpanchang',
# 'all.latest.hindinews',
# 'alvin.hair.manhairstylephoto',
# 'am.zee.recipebookinhindi',
# 'angel.azanmp3app',
# 'aplicacion.tiempo',
# 'app.by.ronnie.dard.shayari.app',
# 'app.emulatorsoft.rapidpsp',
# 'app.isletdevelopers.com.indiacapitalcities',
# 'app.vedio.hdfreeapp',
# 'app36526.vinebre',
# 'app68806.uaehd',
# 'apps.sailstudios.licpolicyreminder',
# 'basic.android.basic',
# 'batterydoctor.fastcharger.batterysaver',]

df = pd.read_csv('/home/ashish/Dropbox/scrape/Play Store Data/Package List/package_list_till_201707.csv')
package = df['package']
count = 0 
for i in package:
	count += 1
	if count > 210025:
		# tim9e.sleep(randint(0,2))
		print count
		try:
			page = requests.get('https://play.google.com/store/apps/details?id=%s' % i, verify = True) 
			if page.status_code == 200:
				tree = html.fromstring(page.content)
				
				app_title = tree.xpath("//div[@class='id-app-title']/text()")
				app_title = [item.encode('ascii','ignore') for item in app_title]
				
				app_developer = tree.xpath("//a[@class='document-subtitle primary']/span/text()")
				app_developer = [item.encode('ascii','ignore') for item in app_developer]
				
				sector = tree.xpath("//a[@class='document-subtitle category']/span/text()")
				sector = [item.encode('ascii','ignore') for item in sector]
				
				ad = tree.xpath("//div[@class='show-more-content text-body']/div/text()")
				
				avg_rate = tree.xpath("//div[contains(@aria-label,'stars out of five stars')]/text()")
				five_star = tree.xpath("//div[contains(@class,'five')]//span[contains(@class,'bar-number')]/text()")
				four_star = tree.xpath("//div[contains(@class,'four')]//span[contains(@class,'bar-number')]/text()")
				three_star = tree.xpath("//div[contains(@class,'three')]//span[contains(@class,'bar-number')]/text()")
				two_star = tree.xpath("//div[contains(@class,'two')]//span[contains(@class,'bar-number')]/text()")
				one_star = tree.xpath("//div[contains(@class,'one')]//span[contains(@class,'bar-number')]/text()")
				install = tree.xpath("//div[contains(@itemprop,'numDownloads')]/text()")
				
				try:
					raw_data = {'num': count, 'package' : i, 'title':app_title[0],'sector': sector[0],'developer': app_developer[0], 'detail':[ad], 'avg_rate':avg_rate[2], 'five_star':five_star[0], 'four_star':four_star[0], 'three_star':three_star[0], 'two_star':two_star[0], 'one_star':one_star[0], 'install' : install[0]}
					print "From try: " + str(i)
					file = open('/home/ashish/Dropbox/scrape/Play Store Data/Play Store Aug 2017/playstore_data_201708.csv', 'a')
				
					df = pd.DataFrame(raw_data, columns = ['num', 'package', 'title', 'sector', 'developer', 'detail', 'avg_rate', 'five_star', 'four_star', 'three_star', 'two_star', 'one_star', 'install'])
					if count == 1:
						df.to_csv(file, header = True)
					else:
						df.to_csv(file, header = False)
				except Exception:
					raw_data = {'num': count, 'package' : i}
					print "From exeption: " + str(i)
					# file = open('data.csv', 'a')
				
					# df = pd.DataFrame(raw_data, columns = ['num', 'package'])
					# if count == 1:
					# 	df.to_csv(file, header = True)
					# else:
					# 	df.to_csv(file, header = False)
			else:
				file1 = open('/home/ashish/Dropbox/scrape/Play Store Data/Play Store Aug 2017/not_found.csv','a')
				writer = csv.writer(file1)
				writer.writerow([i])
		except requests.exceptions.ConnectionError:
			    r.status_code = "Connection refused"
			    print r.status_code
	else:
		pass
		

# 'title':[item for item in app_title if ord(item)<128][0]
# data = ['a', 'dsadsa']
# data1 = [item for item in data if ord(item) < 128]
