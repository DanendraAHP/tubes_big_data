from src.dataset_utils import Dataset
from src.model import TFModel
from datetime import datetime
from config.config import INFERENCE_CONFIG
from pyspark.sql import SparkSession

if  __name__=='__main__':
    #create spark 
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("SparkByExamples.com") \
        .getOrCreate()
    #preprocess before inference
    RAW_FOLDER = INFERENCE_CONFIG['RAW_FOLDER']
    RAW_FOLDER = f'{RAW_FOLDER}/*.parquet'
    df = spark.read.parquet(RAW_FOLDER)
    pd_df = df.toPandas()
    pd_df = pd_df.rename(columns={
        '_1' : 'video_id',
        '_2' : 'description',
        '_3' : 'published_at',
        '_4' : 'channel_name',
        '_5' : 'video_title'
    })
    pd_df = pd_df.drop_duplicates(subset='video_id')
    pd_df = pd_df.dropna(subset=['description'])
    pd_df.to_csv(INFERENCE_CONFIG['RAW_CSV_FILE'], index=False)

    #model inference
    train = False
    #prepare the inference data
    print('now creating dataset'.center(60, '-'))
    data = Dataset(train)
    data.prepare_inference_data()
    model = TFModel()
    y = model.inference(data.tfdf)
    #post-process
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data.df['sentiment'] = y
    data.df['inferred_date'] = dt_string
    #Create PySpark DataFrame from Pandas
    sparkDF=spark.createDataFrame(data.df) 
    sparkDF.write.save(INFERENCE_CONFIG['INFERENCE_FOLDER'], format='parquet', mode='append')