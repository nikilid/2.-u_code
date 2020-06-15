import random
import math
import base64
import sys
import json

def H(data):
	source = data["source"]
	switches = data["switches"]
	models = data["models"]
	res = 0
	for s in source:
		switche = switches[s]
		for m in sorted(switche.keys()):
			for val in sorted(models[str(m)].keys()):
				p = (eval(str(models[str(m)][str(val)])))
				res -= p*math.log2(p) 
	return res

def HwithSigma(data):
	source = data["source"]
	switches = data["switches"]
	models = data["models"]
	entr = 0
	mat = 0
	dic = []
	for s in source:
		switche = switches[s]
		for m in sorted(switche.keys()):
			for val in sorted(models[str(m)].keys()):
				p = (eval(str(models[str(m)][str(val)])))
				dic.append((eval(val), p))
				entr -= p*math.log2(p) 
				mat += math.log2(p)*math.log2(p)*p
	return (dic, entr, mat - entr*entr)

count = 0
l_prob = []
code = []

def check(d, l, f):
	v = 1
	for j in d:
		for m in l:
			if (m[0] == eval(j)):
				v *= m[1]
	l_prob.append((d, v))


def gen(f, n, l, d, i):
	for j in l:
		d = d[:i] + str(j[0]) + d[i+1:]
		if (i == n-1):
			check(d, l, f)	
		else:
			gen(f, n, l, d, i+1)


def gen1(f, n, l, d, i):
	for j in l:
		d = d[:i] + str(j) + d[i+1:]
		if (i == n-1):
			code.append((d))
		else:
			gen1(f, n, l, d, i+1)

if (int(sys.argv[1]) == 1):
	with open(sys.argv[2], "r") as read_file:
		data = json.load(read_file)
	print(H(data))
else:
	if (int(sys.argv[1]) == 2):
		with open(sys.argv[2], "r") as read_file:
			data = json.load(read_file)
		R = eval(sys.argv[3])
		delta = eval(sys.argv[4])
		q = eval(sys.argv[5])
		dic, entr, sigma = HwithSigma(data)
		dic.sort(key = lambda i: i[1])
		if (R < entr):
			print("Ошибка: R < H")
		else: 
			eps = R - entr
			#eps = 2.5
			n = sigma/delta/eps/eps
			if (n - int(n) != 0):
				n = int(n) + 1
			n = int(n)
			#print('n = ' + str(n))
			#print('sigma = ' + str(sigma))
			#print('h = ' + str(entr))
			len_code = math.log2(pow(2, n*R))/math.log2(q)
			if (len_code - int(len_code) != 0):
				len_code = int(len_code) + 1
			#print('len_code' + str(len_code))
			len_code = int(len_code)
			pr = int(pow(q, len_code))
			f = open("result.txt", 'w')
			d = ''
			st = ''
			for i in range(q):
				st += str(i)
			gen(f,n,dic,d, 0)
			l_prob.sort(key = lambda i: i[1])
			d = ''
			gen1(f,len_code,st,d, 0)
			j = 0
			for i in range(len(l_prob)-1, -1, -1):
				f.write(str(l_prob[i][0])+ ' ' +str(code[j%pr])+' \n')
				j += 1
		

		
		