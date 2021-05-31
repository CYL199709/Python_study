import tensorflow as tf
from tensorflow import keras
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
import numpy as np
#(train_data,train_labels),(test_data,test_labels)=imdb.load_data(num_words=10000)
#print(train_data,train_labels)
import re
def rm_tags(text):
    re_tag = re.compile(r'<[^>]+>')
    return re_tag.sub('', text)

# word_index是一个将单词映射为整数索引的字典
word_index=imdb.get_word_index()

all_texts = []
train_label = []
with open("imdb_labelled.txt", encoding='utf8') as file_input:
    filelines = file_input.readlines()
for i in range(0,len(filelines)):
    all_texts += [rm_tags(filelines[i].split('\t')[0])]
    train_label+=(filelines[i][len(filelines[i])-2])
train_label = np.asarray(train_label,dtype="int")
all_texts = [z.lower().replace('\n', '') for z in all_texts]
all_texts = [z.lower().replace('.  ', '.') for z in all_texts]
all_texts = [z.replace('<br />', ' ') for z in all_texts]
#print(len(all_texts))

tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(all_texts)

train_seq = tokenizer.texts_to_sequences(all_texts)

x_train = sequence.pad_sequences(train_seq, maxlen=80)  # shape  (1000, 80)
#print(x_train[0])
#print(train_label)
"""
#键值颠倒，将整数索引映射为单词
reverse_word_index=dict([(value,key) for (key,value) in word_index.items()])
#将评论阶码，减去了3是因为0、1、2是保留的索引（0：padding填充；1：start of sequence序列开始；2：unknown未知词）。
decoded_review=" ".join([reverse_word_index.get(i-3,"?") for i in train_data[0]])
#得到的decoded_review是train_data[0]的原评论，print一下可以查看
print(decoded_review)
"""

vocab_size = 10000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
model.summary()

model.compile(optimizer=tf.compat.v1.train.AdamOptimizer(),loss='binary_crossentropy',metrics=['accuracy'])
history = model.fit(x_train[0:800],train_label[0:800],epochs=100,batch_size=100,validation_data=(x_train[800:1000],train_label[800:1000]),verbose=1)

import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
print(val_acc[len(val_acc)-1])
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

