import pandas as pd #type: ignore
import numpy as np #type: ignore
from sklearn.model_selection import train_test_split  #type: ignore
from tensorflow.keras.utils import to_categorical  #type: ignore
from tensorflow.keras.models import Sequential #type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout #type: ignore


csv_path = "A_Z Handwritten Data.csv"  
data = pd.read_csv(csv_path)


y = data['0'].values
X = data.drop(columns=['0']).values.reshape(-1, 28, 28, 1).astype("float32") / 255.0
y = to_categorical(y, num_classes=26)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

#CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(26, activation='softmax')
])

# Compile and train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=128)

#model 
model.save("alphabet_cnn_model.h5")
print(" Model saved as 'alphabet_cnn_model.h5'")
