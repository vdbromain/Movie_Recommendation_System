# Model use to make recommendations
from pyspark.ml.recommendation import ALS
# Model evaluation
from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('app_name').getOrCreate()

ratings = spark.read.csv('data/ratings.csv',inferSchema=True,header=True)
movies = spark.read.csv('data/movies.csv',inferSchema=True,header=True)

# Joining the data toegether and droping the duplicated column 'movieId'
data_sdf = ratings.join(movies,movies["movieId"]==ratings["movieId"]).drop(ratings["movieId"])

# Initialize the model
als = ALS(userCol="userId", itemCol = "movieId", ratingCol = "rating", coldStartStrategy='drop')

def model_train_saving (als, data_sdf):

    # Split the dataset between train and test
    train, test = data_sdf.randomSplit([0.8, 0.2])
    # Fit the train dataset for the model
    alsModel=als.fit(train)

    # Generating Predictions
    prediction = alsModel.transform(test)

    # Evaluating the model
    evaluator = RegressionEvaluator(metricName="mse", labelCol="rating",  predictionCol="prediction")
    mse = evaluator.evaluate(prediction)
    print(f"The model accuracy is : {mse*100:.2f} %")

    #if mse < 0.75 :
    # What to do if the accuracy drop ? I should have a noticing of that.

    # Saving the model
    als.save("./model/ALS_Movie_Rec_model")
    print("Model is saved")

model_train_saving(als, data_sdf)