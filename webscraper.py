from bs4 import BeautifulSoup
# source tutorial-env/bin/activate 
# Use this code to activate python enviroment
# Using marketbeat.com and archived information
from pprint import pprint
import requests 
import json
urllist = []
urllist.append("https://web.archive.org/web/20190207054621/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20190712233332/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20190419221906/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20180906165025/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20181129115935/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20180621105245/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20180331073045/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20170120051653/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20160426181656/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20150607025311/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20150915011615/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20151207143101/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20160326063453/https://www.marketbeat.com/ipos/lockup-expirations/")
urllist.append("https://web.archive.org/web/20160630013100/https://www.marketbeat.com/ipos/lockup-expirations/")

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
urlcount = 0
for url in urllist:
	response = requests.get(url, timeout=5)
	content = BeautifulSoup(response.content, "html.parser") 
	tickerArr = []
	lockupArr = []
	switch = True
	table = content.find('table')
	for ticker in table.findAll('a'):
		tickerArr.append(ticker.text)
	for lockup in table.findAll('td'):
		check = True
		for letter in alphabet:
			if lockup.text.find(letter) != -1:
				#Makes sure it is a date and doesn't contain any characters
				check = False;
				break
		if lockup.text.find('/') != -1 and check:
			if switch:
				switch = not switch;
				lockupArr.append(lockup.text.replace("/", "-",2))
			else:
				switch = not switch;
	i = 0
	data = {}
	data["stocks"] = []
	while i<len(tickerArr):
		# data[tickerArr[i]] = {"date":lockupArr[i]}
		jsonObj = {
			"ticker" : tickerArr[i],
			"LockUpExpirationDate" : lockupArr[i]
		}
		data["stocks"].append(jsonObj)

		i = i + 1
	filename = "data_url" + str(urlcount) + ".json"
	with open("./data/"+filename, 'w+') as outfile:
		print("Scraping data from " + url + " to " + filename)
		json.dump(data, outfile, indent=4)
	urlcount = urlcount + 1