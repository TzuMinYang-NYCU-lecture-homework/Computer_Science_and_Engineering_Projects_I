# -*- coding: UTF-8 -*-
import requests, time
from xml.etree import ElementTree
import table

ENDPOINT = 'http://61.221.168.226/portal/GraphicController'
batNumber = 5 #單次欲取得資料ID數量,單次數量大於10個時server將不理會
TIMEOUT = 5

def SendRequest(body):
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(ENDPOINT, data=body, headers=headers, timeout=TIMEOUT)
        return response
    except Exception as e:
        print(e)
        return None

def fetchAllData(idList=None):
    if not idList: idList = list(table.node.keys())
    idString=""
    for index in range(len(idList)):
        idString = idString + "<tag id='" + idList[index] + "'/>"
        if index % batNumber == 0 or index == len(idList)-1:
            xml = "<?xml version='1.0' encoding='UTF-8'?><request xmlns='http://chttl.com/iengc/core' method='getTagValue' customerid='1' querylevel='1'>"+ idString +"</request>"
           
            response = SendRequest(xml)
            if not response: continue

            tree = ElementTree.fromstring(response.content)
            for child in tree.iter('*'):
                if child.attrib.get('id'):
                    table.node[child.attrib.get('id')][0] = child.attrib.get('value')    

            idString=""
            #print(index)
            time.sleep(1)  #小於一秒間隔的連續通訊將會導致IP被ban

def fetchIDvalue(idString):
    xml = "<?xml version='1.0' encoding='UTF-8'?><request xmlns='http://chttl.com/iengc/core' method='getTagValue' customerid='1' querylevel='1'><tag id='" + idString + "'/></request>"
    response = SendRequest(xml)
    if not response: return None
    tree = ElementTree.fromstring(response.content)
    return tree.getchildren()[0].attrib.get('value') 

if __name__ == '__main__':

    '''
    fetchAllData()  #取得全部node的資料,資料將寫在table.node中
    for node in table.node.keys():
        print(table.node[node])

    time.sleep(1) #小於一秒間隔的連續通訊將會導致IP被ban

    ID = 'a9895e570f9fa4ee5a4a89ca76c7c435'
    value = fetchIDvalue(ID)   #取得指定ID的node資料
    print(table.node[ID][1], value)
    
    time.sleep(1) #小於一秒間隔的連續通訊將會導致IP被ban
    '''
    
    idList = ['705cd51992dc1faf544441c7dbb6e8bf', 'a9895e570f9fa4ee5a4a89ca76c7c435']
    fetchAllData(idList)
    for ID in idList:
        print(table.node[ID][1], table.node[ID][0])    
    
