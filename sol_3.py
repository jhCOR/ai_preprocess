import pandas as pd
import librosa
import math
import sys
import csv
import numpy as np
import json

from scipy.io import wavfile

def readCSVFile(filePathList):
	list = []
	f = open(filePathList, 'r', encoding='utf-8')
	rdr = csv.reader(f)
	for line in rdr:
		list = line
	print(list)
	return list
	f.close()
    
def readMultipleFiles(pathList):
	dataList = []
	rateList = []
	for i in range(len(pathList)):
		data, fs  = librosa.load(pathList[i])
		dataList.append(data)
		rateList.append(fs)
	return dataList, rateList

def calculatePower(data):
    stftResult=librosa.stft(data, n_fft=4096,win_length=4096,hop_length=1024)
    D=np.abs(stftResult)
    S_dB=librosa.power_to_db(D, ref=np.max)
    db_df = pd.DataFrame(data=S_dB)
    des = db_df.describe()
    db_mean = des.loc['max'].mean()
    return db_mean

def calculateRealTime(data, rate):
    real_time = len(data)/rate
    return real_time

def trimTime(data, db_mean, real_time):
    log_rate = 10 * math.log10(db_mean/ -8.5)
    topDB = 12 + log_rate
    print(topDB)
    clip = librosa.effects.trim(data, top_db=topDB)#14, 4
    start = clip[1][0]/len(data)*real_time
    end = clip[1][1]/len(data)*real_time
    start = '{:.3f}'.format(start)
    end = '{:.3f}'.format(end)
    start = float(start)
    end = float(end)
    print(start, end)
    return start, end

def subMain(dataList, rateList):
    startList = []
    endList = []
    for i in range(len(dataList)):
        mean = calculatePower(dataList[i])
        totalTime = calculateRealTime(dataList[i], rateList[i])
        startpoint, endpoint = trimTime(dataList[i], mean, totalTime)
        startList.append(startpoint)
        endList.append(endpoint)
    return startList, endList

def saveToJson(list_a, list_b):
	with open('./answer.json', encoding='utf-8') as f:
		json_object=json.load(f)
		for i in range(len(list_a)):
			json_object['Q3'][i]["begin"] = list_a[i]
			json_object['Q3'][i]["end"] = list_b[i]
	with open('./GB팀.json', 'w', encoding='utf-8') as fs:
		json.dump(json_object, fs, indent="\t",  ensure_ascii=False)
        
        
        
def main(datafilePath):
    pathList = readCSVFile(datafilePath)
    list_1, list_2 = readMultipleFiles(pathList)
    startlist, endlist = subMain(list_1, list_2)
    saveToJson(startlist, endlist)
    
if __name__ == "__main__":
    main(sys.argv[1])
