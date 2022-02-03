#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: praisemathewjohnson

"""

from requests_html import AsyncHTMLSession
from datetime import datetime
import nest_asyncio, re, numpy, pandas, csv

nest_asyncio.apply()

file = open("output.txt", "w")
output = r'output.txt'

for_sale = []
x_axis = []
y_axis = []

#create the session
asession = AsyncHTMLSession()

url = 'https://www.opendoor.com/homes'

async def getOpendoorMarkets():
   
    r = await asession.get(url)

    #Render JS content
    await r.html.arender(sleep=1, keep_page=True, scrolldown=1, timeout=10)

    #rendered html, find element by class
    locations = r.html.find('.css-11cxpkk')

    #find links for current markets
    for item in locations:
        file.write(str(item.absolute_links))
        file.close()
        
    r.close()

async def getOpendoorInventory():
    
    for i in url_array:
        
        start = datetime.now()
        r = await asession.get(i+'?opendoor=true')
        
        await r.html.arender(sleep=5, keep_page=True, scrolldown=1, timeout=20)
        
        inventory = r.html.find('.property-map-list-title__count')
        
        for item in inventory:
            for_sale.append([i, item.text])
            print('\n', str(len(for_sale))+'.', for_sale[len(for_sale)-1])
            break

        r.close()
        print('\nTime elapsed:', datetime.now()-start)

asession.run(getOpendoorMarkets)

#format text file
sub = re.sub(r"[{}']", '', open(output).read()).replace(' ', '')
open(output, 'w').write(sub)

#load urls to array
url_array = open(output).read().split(',')
# print(url_array)
print('\nOpendoor currently operates in', len(url_array), 'markets.')

asession.run(getOpendoorInventory)

#save array to text file
numpy.savetxt('inventory.txt', for_sale, fmt='%s')
for_sale = numpy.loadtxt('inventory.txt', dtype='str')    

#save array to csv file and format csv data
csv_file = 'inventory_'+str(datetime.now().strftime('%d-%m-%Y'))+'.csv'
pandas.DataFrame(for_sale).to_csv(csv_file, index=False)
data = pandas.read_csv(csv_file)
data.drop('2', inplace=True, axis=1)
data.drop('3', inplace=True, axis=1)
data.to_csv(csv_file, index=False)        

print('\n', for_sale)

