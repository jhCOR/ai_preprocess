import json
import pandas as pd
import sys
def loadData(filePath):
    train_data = pd.read_table(filePath)
    print(train_data)
    return train_data

def find(sentence):
	start = 0
	end = 0
	cursor = 0;
	while sentence.find(')/(', start) != -1:
		start = sentence.find('(', cursor)
		end = sentence.find(')/(', start)
		if(start is not -1):
			if(end is not -1):
				sentence = sentence[:start]+sentence[end+len(')/(')-1:]
				cursor = end+len(')/(')-2
	return sentence

def extractJustKor(filePath='./answer.json'):
    with open(filePath, encoding='utf-8') as f:
        json_object = json.load(f)
        json_object_Q2 = json_object['Q2']
        json_object_new = [find(json_object_Q2[i]['original']) for i in range(len(json_object_Q2))]
        train_data = pd.DataFrame(json_object_new)
        train_data.columns = ['original']
        train_data['original'] = train_data['original'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
        result = [{'original':json_object_Q2[i]['original'], 'new':train_data['original'][i]} for i in range(len(train_data))]
        json_object['Q2'] = result
    with open('./GB팀.json', 'w', encoding='utf-8') as fs:
        json.dump(json_object, fs, indent="\t",  ensure_ascii=False)

def main(datafilePath):
	extractJustKor(datafilePath)
    
if __name__ == "__main__":
	main(sys.argv[1])
