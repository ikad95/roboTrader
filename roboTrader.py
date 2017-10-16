import sys,json,urllib2
#all % are based on your buying cost!
#if the prices rise.. dont sell, keep, if they rise > 10 %, wait for them to fall below 8%, then sell

#if they rise above 20%, wait for them to fall below 16% then sell!
#30% -> 24%
#40% -> 36%
#50% -> 40%
#...
#max selling % = 80% of global max 
#similarly sell if they fall below -8%


#simulation

from random import randint
import time
# coi = []
# prof = []
# for i in range(10):
# 	coi.append(float(i*100))		#initializing with some values
# 	prof.append(float(0.1))
# initVal = []
# for i in coi:
# 	initVal.append(i)
# stable = 0
def calcProf(buy,sell):
	if buy == 0:
		return 0
	return float(sell-buy)/buy * 100
overallP = -1000
maxProf = 0.0
minProf = 1000000000000000000000000
cash = 1000.0
lastBuyRate = 0.0
lastSellRate = 1000000.0
btc = 0
neww=1
headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36' }
print "Buy/Sell ","\t\t\tCash ", "\t\t\tCoins", "\t\t\t\tdelta ", "\t\t\t\tOverall profit "
def sellAll(rate):
	global cash,btc,lastSellRate
	cash += float(btc) * rate
	btc = 0.0
	lastSellRate = rate
	print "Sell ",rate, "\t\t\t", cash, "\t\t\t",btc,"\t\t\t",delP, "\t\t\t",overallP

def buyAll(rate):
	global cash,btc,lastBuyRate
	btc += float(cash) / rate
	cash = 0.0
	lastBuyRate = rate

	print "Buy ",rate, "\t\t\t", cash, "\t\t\t",btc,"\t\t\t",delP, "\t\t\t",overallP

f = open("btcusd1.csv","r")
c=0
currRateS = 0
currRateB = 0
prof = 0
risk = 0
#for i in f:
while 1:
	req = urllib2.Request("https://www.bitstamp.net/api/ticker/")#"https://poloniex.com/public?command=returnTicker/",None,headers)
	conn = urllib2.urlopen(req)
	x = json.loads(conn.read())
	#print x
	buy = float(x["last"])
	sell = float(x["last"])
	#print "Buy ",buy,"Sell ",sell
	c+=1
	#if c == 10:
	#	c=0
	#	if cash != 0:
	#		lastBuyRate = 0
	delP = currRateS
	## make delP avg not instant
	lastRate = currRateS
#	ff = i#[1].split('"')[1]
	#print ff
	currRateS = sell#float(line[1].split('"')[1])
	currRateB = buy#float(line[1].split('"')[1])
	prof = calcProf(lastBuyRate,currRateS)
	lastRate+=0.0000000000000000000001
	delP = (currRateS - delP ) / lastRate
	if(currRateB <= lastSellRate and delP > 0 and cash!=0):
		buyAll(currRateB)
	if(currRateS > lastBuyRate and delP < 0 and btc!=0):
		sellAll(currRateS)
	maxProf = max(maxProf,prof)
	minProf = min(maxProf,prof)
	overallP = btc * currRateS + cash - 1000
	print "R ",currRateS, "\t\t\tC ", cash, "\t\t\tB ",btc, "\t\tlB ",lastBuyRate,"\tlS ",lastSellRate,"\tdelP ",delP, "\tOverall p ",overallP
#	time.sleep(0.001)

	###To take risks!
	if currRateB - lastSellRate > 30 and btc==0 and risk==0:
		print "Take risk manually!!!!"
		y = raw_input("Buy with loss??? y/n >>>> ")
		if y == "y":
			#reset
			maxProf = 0.0
			minProf = 1000000000000000000000000
			prof = 0
			lastBuyRate = 0.0
			lastSellRate = 1000000.0
		#risk=1
	#expectedLoss = cash / (lastSellRate - currRate)
	#if overallP > expectedLoss * 80 and btc==0:
	#	buyAll(currRate)
	conn.close()

print "B: R ",currRateS, "\t\t\tC ", cash, "\t\t\tB ",btc

