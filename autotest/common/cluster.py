#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 31, 2018
cluster.py: data mining for text cluster
@author: Neo
'''

import os, logging, multiprocessing
import pandas as pd
from gensim import corpora
from gensim.models.doc2vec import Doc2Vec, TaggedLineDocument, TaggedDocument
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn import cluster 
from sklearn.externals import joblib 
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
#from nltk.stem.porter import PorterStemmer 

#global variables
english_punctuations = [',','.',';','?','!','(',')','[',']','@','&','#','%','$','{','}','--','-',"'"]
src_path = "/home/information/log"
model_path = "/home/information/data-mining/model/log.model"
cluster_path = "/home/information/data-mining/cluster/log.pkl"
cluster_result = '/home/information/data-mining/cluster/cluster.xls'
#dump in source data
def get_dataset(object):
	srcdata = []
	for root, dirs, files in os.walk(object):
		for f in files:
			file_path = os.path.join(root,f)
			if file_path.find('dmesg') >= 0:
				print "Handle dataset in file: %s..." %file_path
				f = open(file_path, 'r')
				data = f.read().decode('utf8', 'ignore')
				lines = data.split('\n')
				for line in lines:
					line = line[line.find(']')+1:]
					srcdata.append(line)
				f.close()
			elif file_path.find('messages') >= 0 and file_path.find('SUSE') >=0:
				print "Handle dataset in file: %s..." %file_path
				f = open(file_path, 'r')
				data = f.read().decode('utf8', 'ignore')
				lines = data.split('\n')
				for line in lines:
					str1 = line[line.find('linux'):]
					line = str1[str1.find(' '):]
					srcdata.append(line)
				f.close()
			elif file_path.find('messages') >= 0 and file_path.find('RedHat') >=0:
				print "Handle dataset in file: %s..." %file_path
				f = open(file_path, 'r')
				data = f.read().decode('utf8', 'ignore')
				lines = data.split('\n')
				for line in lines:
					line = line[line.find('localhost')+9:]
					srcdata.append(line)
				f.close()
			else:
				pass
	yield srcdata

#preprocess all the dataset, including tokenize, remove stopwords, remove punctuation, and stemming words
def preprocess(dataset):
	global english_puncutations
	#tokenize
	dataset_tokenized = [[word.lower() for word in word_tokenize(item)] for item in dataset]
	#remove stopwords
	english_stopwords = stopwords.words('english')
	dataset_flr_stopwords = [[word for word in item if not word in english_stopwords] for item in dataset_tokenized]
	#remove punctuation
	dataset_flr_punctuation = [[word for word in item if not word in english_punctuations] for item in dataset_flr_stopwords]
	#stem words
	#st = PorterStemmer()   
	#dataset_stemmed = [[st.stem(word) for word in item] for item in dataset_flr_punctuation]
	#convert data to TaggedDocument
	dataset_processed = dataset_flr_punctuation
	count = 0
	pre_data = []
	for item in dataset_processed:
		document = TaggedDocument(item, tags=[count])
		pre_data.append(document)
		count += 1
	return pre_data

#use doc2vec to train the dataset
#class gensim.models.doc2vec.Doc2Vec(documents=None,md_mean=None,dm=1,dbow_words=0,
#					dm_concat=0,dm_tag_count=1,docvecs=None,docvecs_mapfile=None,trim_rule=None,**kwargs)
#dm defines the training algorithm. dm=1 means 'distributed memory' (PV-DM). Otherwise, 'distributed
#bag of words' (PV-DBOW) is employed. size is the dimensionality of the feature vectors. window is the maximum
#distance between the predicted word and context words used for predicttion within a document.
#alpha is the initial learning rate. seed= for random number generator. min_count= ignore all words with total
#frequency lower than this. iter= number of iterations over the corpus.hs= if 1, hierarchical softmax will be
#used for model training.dm_mean = if 0, use the sum of the content word vector. If 1, use the mean. Only used
#when dm is used in non-concatenative mode. dm_concat= if 1, use concatenation of context vectors.
def train(pre_data):
	dm = 0
	cores = multiprocessing.cpu_count()
	size = 160
	context_window = 3
	min_count = 1
	alpha = 0.2
	max_iter = 20
	sample = 1e-1 
	negative = 1
	dm_concat=0
	hs = 1

	#pre_data = TaggedLineDocument(filename)
	model = Doc2Vec(dm=dm, alpha=alpha, min_count=min_count, \
			window=context_window, size=size, sample=sample, negative=negative, \
			workers=cores, hs=hs, dm_concat=dm_concat, iter=max_iter)
	model.build_vocab(pre_data)
	model.train(pre_data, total_examples=model.corpus_count, epochs=100)
	model.save(model_path)

#cluster
def datacluster(data):
	infered_vectors_list = []
	print "load model..."
	model_dm = Doc2Vec.load(model_path)
	print "load train vectors..."
	for text, label in data:
		vector = model_dm.infer_vector(text)
		infered_vectors_list.append(vector)
	'''
	print "Check the optimized parameter..."
	Nc = range(1, 50)
	pca_data = [PCA(n_components = i).fit(infered_vectors_list).transform(infered_vectors_list) for i in Nc]
	kmeans = cluster.KMeans(init='k-means++',n_clusters=20,max_iter=300)
	score = [kmeans.fit(pca_data[i]).score(pca_data[i]) for i in range(len(pca_data))]
	print score
	plt.plot(Nc,score)
	plt.xlabel('PCA components')
	plt.ylabel('Score')
	plt.title('Elbow Curve')
	plt.show()
	'''

	print "PCA decomposition..."
	pca = PCA(n_components = 10).fit(infered_vectors_list)
	pca_data = pca.transform(infered_vectors_list)
	print "train K-Means model..."
	kmean_model = cluster.KMeans(init='k-means++',n_clusters=16,max_iter=300)
	kmean_model.fit(pca_data)
	#get the classified index
	result = kmean_model.fit_predict(pca_data)
	print "Predicting result:", result
	#save the cluster result
	joblib.dump(kmean_model, cluster_path)
	#load the cluster result
#	new_km = joblib.load(cluster_path)
	numSamples = len(pca_data) 
	print numSamples
	centroids = kmean_model.labels_
	
	#print centroids,type(centroids) #显示中心点
	#print kmean_model.inertia_  #显示聚类效果
	'''	
	marker = ['o', '.', ',', 'x', '*', 'd', 's', 'p']
	color = ['r', 'g', 'b', 'c', 'm', 'k', 'y', 'w']
	for i in xrange(numSamples):
		plt.scatter(pca_data[i][0], pca_data[i][1], \
				marker=marker[centroids[i]], color=color[centroids[i]])
	plt.show()
	'''
	return centroids

if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	dataset = get_dataset(src_path).next()
#	print "DATASET:", dataset
	processed_data = preprocess(dataset)
#	print "===>Processed_data:", processed_data
	train(processed_data)
	clusters = datacluster(processed_data)
	'''
	#print the dataset cluster result
	for i in range(len(processed_data)):  
		string = ""  
		text = processed_data[i][0]
		output = ' '.join(list(text)) + '===>cluster:' + str(clusters[i]) + '\n'	
		print output
	'''
	#managed by pd
	logs = {'information': dataset, 'cluster':clusters}
	df = pd.DataFrame(logs, index=[clusters], columns=['information','cluster'])
	df.to_excel(cluster_result, index=False)
	'''
	for i in range(15):
		print("Cluster %d information:" % i)
		for information in frame.ix[i]['information'].values.tolist():
			print('%s\n' % information)
		print("") #add whitespace
		print("")
	'''
