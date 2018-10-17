from bs4 import BeautifulSoup
import requests
from datetime import date
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
	
	tickerlist = []
	stocktotaltextlist = []
	#opening txt file with tickernames
	file = "tickername.txt"
	with open (file) as fobj:
		tickerall  = fobj.read()
	tickerall = tickerall.split(", ")
	
	#Date comparision
	today = date.today()

	#Correcting formating to compare dates
	daynumber = today.strftime("%d")
	if (daynumber[0]) == "0":
		daynumber = daynumber.replace("0","")

	# convert into string date
	datecomparetoday = today.strftime("%A") + ", " + today.strftime("%B") + " " + daynumber + ", " + today.strftime("%Y")

	def scrapper(ticker):
		page_link = "https://web.tmxmoney.com/news.php?qm_symbol=" + ticker
		data = requests.get(page_link, timeout = 1)
		soup = BeautifulSoup(data.text, 'html.parser')

		#Current Stock Price
		pricediv = soup.find('div', "quote-price priceLarge")
		pricespan = pricediv.find('span')
		stockprice = "Current market price is " + pricespan.text + "\n"

		content = soup.find('div', "quote-tabs-content")
		headliner = content.find('div', "pages")
		newsinfo = headliner.find('span', "article")
		
		#used to compare to daily date later
		dateinfo = (headliner.find('div', "dateGroup")).text

		#Today and lastest news seperation
		if datecomparetoday == dateinfo:
			stocktitle = "Today's News for {:5}".format(ticker)
			#Title of article
			newstitle = newsinfo.text

			#Url of the article
			newslink = headliner.find('a')
			urlnews = "https://web.tmxmoney.com/" + (newslink.get('href'))
		else:
			stocktitle = "Latest News for {:5}".format(ticker)

			#Title of article
			newstitle = newsinfo.text
			#Url of the article
			newslink = headliner.find('a')
			urlnews = "https://web.tmxmoney.com/" + (newslink.get('href'))
		stocktextlist = "{}{}\n{}{}{} \n \n".format(stocktitle, dateinfo, stockprice, newstitle, urlnews)
		return(stocktextlist)

	#Email sender
	def email(emailtext):
		fromaddr = ''		#add your email here where you want to send from!
		toaddr = ''  #add your email here where you want email to be sent!
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "TMX Stock News for " + datecomparetoday

		body = emailtext
		msg.attach(MIMEText(body, 'plain'))
 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, '')		#password of the sent email
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
	
	for astock in tickerall:
		stocktotaltextlist.append(scrapper(astock.upper()))

	bodytext = "".join(stocktotaltextlist)
	
		
if __name__=="__main__":
	main()

