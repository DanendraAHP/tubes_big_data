from src.dataset_utils import Dataset
from src.model import TFModel

#prepare the training data
#set training to false if want to infer
train = False
print('now creating dataset'.center(60, '-'))
data = Dataset(train)
data.prepare_training_data()
#train the model
model = TFModel(data.train_df, data.val_df)
model.train_and_eval()