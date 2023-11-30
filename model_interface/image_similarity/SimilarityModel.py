from keras.src.preprocessing.image import DirectoryIterator

from model_interface.image_similarity.config import *
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import GlobalAveragePooling2D, Dense, Input
from keras.models import Model
from keras.optimizers import Adam
from keras.applications.resnet50 import preprocess_input, ResNet50
from keras.losses import CategoricalCrossentropy
import tensorflow as tf
import tf2onnx
import onnx

# SimilarityModel
class SimilarityModel:
    NUM_EPOCHS = NUM_EPOCHS
    BATCH_SIZE = BATCH_SIZE
    INIT_LR = INIT_LR
    image_size = IMAGE_SIZE
    classification_model = None
    similarity_model = None
    number_of_classes = NUMBER_OF_CLASSES
    train_size = None
    optimizer = Adam(learning_rate=INIT_LR)
    imageGenerator = ImageDataGenerator(preprocessing_function=preprocess_input)

    def init_layers(self):
        model = ResNet50(
            weights="imagenet",
            include_top=False,
            input_shape=(self.image_size[0], self.image_size[1], 3),
        )
        inputs = Input(shape=(self.image_size[0], self.image_size[1], 3))
        x = model(inputs)
        x = GlobalAveragePooling2D()(x)
        outputs = Dense(self.number_of_classes, activation="softmax")(x)
        self.classification_model = Model(inputs=inputs, outputs=outputs)
        self.classification_model.compile(
            loss=CategoricalCrossentropy(),
            optimizer=self.optimizer,
            metrics=["accuracy"],
        )

    def feed_train_sets(self, feed_test: bool = True) -> tuple[DirectoryIterator, ...]:
        train = self.imageGenerator.flow_from_directory(
            TRAIN_PATH,
            class_mode="categorical",
            target_size=self.image_size,
            color_mode="rgb",
            shuffle=True,
            batch_size=BATCH_SIZE,
        )
        validation = self.imageGenerator.flow_from_directory(
            VAL_PATH,
            class_mode="categorical",
            target_size=self.image_size,
            color_mode="rgb",
            shuffle=True,
            batch_size=BATCH_SIZE,
        )

        if feed_test:
            test = self.imageGenerator.flow_from_directory(
                TEST_PATH,
                class_mode="categorical",
                target_size=self.image_size,
                color_mode="rgb",
                shuffle=True,
                batch_size=BATCH_SIZE,
            )
        else:
            test = []
        assert self.number_of_classes == train.num_classes
        self.train_size = len(train.filenames)
        return train, validation, test

    def train(self, train: DirectoryIterator, validation: DirectoryIterator):
        assert self.classification_model is not None
        assert self.train_size is not None
        self.classification_model.fit(
            train,
            steps_per_epoch=self.train_size // BATCH_SIZE,
            validation_data=validation,
            validation_steps=len(validation.filenames) // BATCH_SIZE,
            epochs=NUM_EPOCHS,
        )

    def save_model(self):
        self.classification_model.save(MODEL_WEIGHTS, save_format="h5")

    def save_onnx(self):
        classification_model_signature = [
            tf.TensorSpec(model_input.shape, model_input.dtype)
            for model_input in self.classification_model.inputs
        ]
        onnx_classification_model, _ = tf2onnx.convert.from_keras(
            self.classification_model, classification_model_signature, opset=13
        )
        onnx.save(onnx_classification_model, CLASSIFICATION_MODEL_PATH)
