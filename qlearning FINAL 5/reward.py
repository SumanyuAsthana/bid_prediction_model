import numpy as np
import tensorflow as tf
def calcLoss(y_true,y_pred):
  #this is our loss function we can try various losses here we dont need to use it right now since we use random forest
  return tf.keras.losses.MeanAbsoluteError()(y_true, y_pred)