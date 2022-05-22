import numpy as np
import math
from sklearn.svm import SVC
import os
import re
import sklearn
from sklearn.ensemble import RandomForestClassifier

def getshan(domain): 1
	tmp_dict = {}
	domain_len = len(domain)
	for i in range(0,domain_len):
		if domain[i] in tmp_dict.keys():
			tmp_dict[domain[i]] = tmp_dict[domain[i]] + 1
		else:
			tmp_dict[domain[i]] = 1
	shannon = 0
	for i in tmp_dict.keys():
		p = float(tmp_dict[i]) / domain_len
		shannon = shannon - p * math.log(p,2)
	return shannon

def getlen(domain):           
	return len(domain)

def getroot(domain):            
	return domain.split('.')[-1]

def getnum(domain):     
	num=0
	for i in domain:
		if i.isdigit():
		    num=num+1
	return num

def getseg(domain):         
    return (domain.count('.')+1)

class Domain:
    def __init__(self, _name, _label):
        self.name = _name
        self.label = _label

    def returnData(self): 
        return [getlen(self.name), getnum(self.name), getshan(self.name),getseg(self.name)]

    def returnLabel(self):
        if self.label == "notdga":
            return 0
        else:
            return 1

train_domainlist = []
test_domainlist = []
def loaddata(filename, method):      
    if method == 'train':
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue
                tokens = line.split(",")
                name = tokens[0]
                label = tokens[1]
                train_domainlist.append(Domain(name, label))
    elif method == 'test':
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue
                tokens = line.split(",")
                name = tokens[0]
                test_domainlist.append(name)

def main():
    loaddata("train.txt","train")
    loaddata("test.txt","test")
    featureMatrix = []
    labelList = []
    for item in train_domainlist:
        featureMatrix.append(item.returnData())
        labelList.append(item.returnLabel())

    #print(featureMatrix)
    clf = RandomForestClassifier(random_state=0)
    clf.fit(featureMatrix, labelList)

    arr = ["notdga", "dga"]
    f = open("result.txt", 'w')
    for item in test_domainlist:   #随机森林feed进去特征
        t = clf.predict([[getlen(item), getnum(item), getshan(item) , getseg(item)]])
        f.write(item + ',' + np.array(arr)[t][0] + '\n')

if __name__ == '__main__':
    main()
    print("finish")
