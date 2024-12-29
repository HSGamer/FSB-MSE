import numpy as np
from keras.src.layers import average
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

from util import load_dataset, INDICE_TO_LABEL, NUMBER_OF_CLASSES, MODEL_NAME

X_train, Y_train, X_test, Y_test = load_dataset()

print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
print(Y_test.shape)

X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2)

# for i in range(20):
#     plt.imshow(X_train[i,:].reshape((128, 128)), cmap='gray', interpolation='bicubic')
#     plt.title(INDICE_TO_LABEL[np.argmax(Y_train[i])])
#     plt.xticks([]), plt.yticks([])
#     plt.show()
#
# for i in range(20):
#     plt.imshow(X_test[i,:].reshape((128, 128)), cmap='gray', interpolation='bicubic')
#     plt.title(INDICE_TO_LABEL[np.argmax(Y_test[i])])
#     plt.xticks([]), plt.yticks([])
#     plt.show()

aug = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=45,
    zoom_range=0.1,
    width_shift_range=0.05,
    height_shift_range=0.05,
    shear_range = 0.1,
    horizontal_flip=False,
    fill_mode="nearest")

model = keras.Sequential([
    Input(shape=(128, 128, 1)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(NUMBER_OF_CLASSES, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=[
        keras.metrics.CategoricalAccuracy(name='accuracy'),
        keras.metrics.Recall(name='recall'),
        keras.metrics.Precision(name='precision'),
        keras.metrics.F1Score(name='f1', average='macro')
    ]
)
keras.utils.plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)

history = model.fit(
    aug.flow(X_train, Y_train, batch_size=32),
    validation_data=(X_val, Y_val),
    epochs=50,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=5),
        keras.callbacks.ModelCheckpoint(MODEL_NAME, save_best_only=True)
    ]
)

model.save(MODEL_NAME)

eval_result = model.evaluate(X_test, Y_test, return_dict=True)
print(eval_result)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('accuracy.png')
plt.clf()

plt.plot(history.history['recall'])
plt.plot(history.history['val_recall'])
plt.title('Model recall')
plt.ylabel('Recall')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('recall.png')
plt.clf()

plt.plot(history.history['precision'])
plt.plot(history.history['val_precision'])
plt.title('Model precision')
plt.ylabel('Precision')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('precision.png')
plt.clf()

plt.plot(history.history['f1'])
plt.plot(history.history['val_f1'])
plt.title('Model F1')
plt.ylabel('F1')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.savefig('f1.png')
plt.clf()

Y_pred = model.predict(X_test)
Y_pred = np.argmax(Y_pred, axis=1)
Y_test = np.argmax(Y_test, axis=1)
cm = confusion_matrix(Y_test, Y_pred)
plt.figure(figsize=(10, 10))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=INDICE_TO_LABEL, yticklabels=INDICE_TO_LABEL)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion matrix')
plt.savefig('confusion_matrix.png')
plt.clf()