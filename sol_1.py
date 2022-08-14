from scipy.io import wavfile
import numpy as np
import pandas as pd
import csv
import sys
import json
import struct
import binascii
#pathList = ['./q1_1.wav',
#            './q1_2.wav',
#            './q1_3.wav',
#            './q1_4.wav',
 #           './q1_5.wav']

def readMultipleFiles(pathList):
	dataList = []
	rateList = []
	for i in range(len(pathList)):
		fs, data = wavfile.read(pathList[i].strip()) 
		dataList.append(data)
		rateList.append(fs)
	return dataList, rateList

def checkTime(DataList, rateList):
	resultList = []
	for i in range(len(DataList)):
		times = len(DataList[i])/float(rateList[i])
		times = '{:.3f}'.format(times)
		times = float(times)
		resultList.append(times)
		print(times)
	return resultList

def readCSVFile(filePathList):
	list = []
	f = open(filePathList, 'r', encoding='utf-8')
	rdr = csv.reader(f)
	for line in rdr:
		list = line
	print(list)
	return list
	f.close()
    
def saveToJson(dataList):
	with open('./answer.json', encoding='utf-8') as f:
		json_object=json.load(f)
		for i in range(len(dataList)):
			json_object['Q1'][i]["duration"] = dataList[i]
	with open('./GB팀.json', 'w', encoding='utf-8') as fs:
		json.dump(json_object, fs, indent="\t",  ensure_ascii=False)

def readAsBinary(filePath):
	with open(filePath, 'rb') as f:
		l1 = f.readline()
		l2 = f.readline()
		print(l1)
		print(l2)
		print("---")
		return l1
        
def Little(data):
	if len(data) == 4:
		data = struct.pack('<I', int(binascii.b2a_hex(data), 16))
		return binascii.b2a_hex(data)
	elif len(data) == 2:
		data = struct.pack('<h', int(binascii.b2a_hex(data), 16))
		return binascii.b2a_hex(data)
def Big(data):
    return binascii.b2a_hex(data)

def analyzeFile(binary_data):
    l1 = binary_data
    blocks = [['Subchunk1ID', 'B', 4], ['Subchunk1', 'L', 4]]
    i = str(binascii.b2a_hex(l1))[2:].index(str(binascii.hexlify(b'fmt '))[2:-1])
    for blc in blocks:
        if blc[1] == 'B':
            print(blc[0], "=", Big(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
        else:
            print(blc[0], "=", Little(l1[i:i+blc[2]]), "(", l1[i:i+blc[2]], ")")
    
            
def main(csvfilePath):
	pathList = readCSVFile(csvfilePath)
	list_1, list_2=readMultipleFiles(pathList)
	result = checkTime(list_1, list_2)
	saveToJson(result)
    
if __name__ == "__main__":
	main(sys.argv[1])


