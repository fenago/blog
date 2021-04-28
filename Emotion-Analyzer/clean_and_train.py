from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
from sklearn.metrics import confusion_matrix
import pandas as pd
import os
import shutil

def move_all_files_to_single_folder(folder_path):
    folders = os.listdir(folder_path)
    for folder in folders:
        inner_folder_path = os.path.join(folder_path, folder)
        files = os.listdir(inner_folder_path)
        for file in files:
            shutil.move(os.path.join(inner_folder_path, file), os.path.join(folder_path, file))
            
        os.rmdir(inner_folder_path)
        


def calculate_labels(file_names):
    emotion_id_to_label = {
        '01': 'neutral', 
        '02': 'calm',
        '03': 'happy',
        '04': 'sad',
        '05': 'angry',
        '06': 'fearful',
        '07': 'disgust',
        '08': 'surprised'
    }
    labels = []
    for file in file_names:
        label_id = file.split('-')[2]
        actor_gender = 'male' if int(file.split('-')[-1].split('.')[0]) % 2 else 'female' 
        label = f'{actor_gender}-{emotion_id_to_label[label_id]}'
        labels.append(label)
        
    return pd.DataFrame(labels)

        

def calculating_the_features(file_names):
    df = pd.DataFrame(columns=['feature'])
    for file in file_names:
        X, sample_rate = librosa.load(os.path.join('../Audio_Speech_Actors_01-24/', file), 
                                      res_type='kaiser_fast',
                                      duration=2.5,
                                      sr=22050*2,
                                      offset=0.5)
        

        sample_rate = np.array(sample_rate)
        feature = np.mean(librosa.feature.mfcc(y=X,
                                               sr=sample_rate, 
                                               n_mfcc=13),
                          axis=0)
        
        df.loc[len(df)] = [feature]
        
    df = pd.DataFrame(df['feature'].values.tolist())
    df = df.fillna(0)
    return df



def divide_into_train_test(df, labels):
    X_train, X_test, y_train, y_test = train_test_split(df,
                                                        labels,
                                                        test_size=0.2,
                                                        random_state=42,
                                                        shuffle=True)
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    lb = LabelEncoder()

    y_train = tf.keras.utils.to_categorical(lb.fit_transform(y_train))
    y_test = tf.keras.utils.to_categorical(lb.fit_transform(y_test))
    
    X_train = np.expand_dims(X_train, axis=2)
    X_test = np.expand_dims(X_test, axis=2)
    
    return X_train, X_test, y_train, y_test

def create_model():
    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Conv1D(256, 5,padding='same',input_shape=(216,1)))
    model.add(tf.keras.layers.Activation('relu'))
    
    model.add(tf.keras.layers.Conv1D(128, 5,padding='same'))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.MaxPooling1D(pool_size=(8)))
    model.add(tf.keras.layers.Dropout(0.3))


    model.add(tf.keras.layers.Conv1D(128, 5,padding='same',))
    model.add(tf.keras.layers.Activation('relu'))

    model.add(tf.keras.layers.Conv1D(128, 5,padding='same',))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Flatten())
    
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Activation('softmax'))
    
    opt = tf.keras.optimizers.RMSprop(lr=0.00001, decay=1e-6)
    
    
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint('Emotion_Voice_Detection_Model.h5',
                                                          save_best_only=True)
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                              patience=3, min_lr=0.00000001)
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)
    
    
    
    model.compile(loss='categorical_crossentropy', 
                  optimizer=opt,
                  metrics=['accuracy'],
                  callbacks=[model_checkpoint, reduce_lr, early_stopping])
    
    return model

def plot(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def predict( file_path, model_path):
    X, sample_rate = librosa.load(file_path, 
                                  res_type='kaiser_fast',
                                  duration=2.5,
                                  sr=22050*2,
                                  offset=0.5)

    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    features = pd.DataFrame(data=mfccs).T #convert to a single row
    features = np.expand_dims(features, axis=2)
    model = tf.keras.models.load_model(model_path)


    prediction = model.predict(features)
    prediction = prediction.argmax(axis=1)
    lb = LabelEncoder()
    labels = pd.read_csv('labels.csv')['0']
    lb.fit(labels)
    pred = prediction.astype(int).flatten()
    return lb.inverse_transform(pred)

if __name__ == '__main__':
    move_all_files_to_single_folder('../Audio_Speech_Actors_01-24/')
    file_names = os.listdir('../Audio_Speech_Actors_01-24/')

    labels = calculate_labels(file_names)
    labels.to_csv('labels.csv')

    df = calculating_the_features(file_names)
    X_train, X_test, y_train, y_test = divide_into_train_test(df, labels)

    model = create_model()
    history = model.fit(X_train, y_train, batch_size=16, epochs=500, validation_data=(X_test, y_test))
