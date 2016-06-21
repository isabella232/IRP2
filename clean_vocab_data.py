
# -*- coding: utf-8 -*-
import json
from pprint import pprint

with open('artist.json') as data_file:
    data = json.load(data_file)

print data[0]


'''
#prints the first record for validation of dataset
print'name : '+ (data[0]['name']['value'])
print'label : '+ (data[0]['label']['value'])
'''

#for artist

for i in range(5000,20000):
    s = data[i]['label']['value']
    s = s.replace(",", " ")

    s_n = data[i]['name']['value']
    s_n = s_n.replace(",", " ")

    try:
     u = unicode(s,'utf-8')
     backToBytes_l = u.encode('utf-8')
    except:
     backToBytes_l =  s
    try:
     u = unicode(s_n,'utf-8')
     backToBytes = u.encode('utf-8')
    except:
     backToBytes =  s_n
    print '{ ' + '"id"  :'+ str(i) + ','+'"label" : ' +' " ' + backToBytes_l +' " '+' ,'+'"name" : ' + ' " ' + backToBytes  + ' " ' + '} ,'

'''
#for location

for i in range(5000,20000):
    s = data[i]['label']['value']
    s = s.replace(",", " ")

    s_n = data[i]['name']['value']
    s_n = s_n.replace(",", " ")

    try:
     u = unicode(s,'utf-8')
     backToBytes_l = u.encode('utf-8')
    except:
     backToBytes_l =  s
    try:
     u = unicode(s_n,'utf-8')
     backToBytes = u.encode('utf-8')
    except:
     backToBytes =  s_n
    print '{ ' + '"id"  :'+ str(i) + ','+'"label" : ' +' " ' + backToBytes_l +' " '+' ,'+'"name" : ' + ' " ' + backToBytes  + ' " ' + '} ,'
'''
