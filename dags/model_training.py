# Model use to make recommendations
from pyspark.ml.recommendation import ALS
# Model evaluation
from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.sql import SparkSession

url1 = "./data/movies.csv" 
url2 = "./data/ratings.csv"

def open_csv(*urls, header=True, inferSchema=True):
    """
    Reads multiple CSV files and returns the corresponding DataFrames.

    Args:
        *urls (str): The URLs of the CSV files to be read.
        header (bool, optional): Indicates whether the CSV files have a header row. Defaults to True.
        inferSchema (bool, optional): Indicates whether PySpark should guess the data types of the CSV file columns. Defaults to True.

    Returns:
        tuple: A tuple containing the DataFrames read from the CSV files.

    Raises:
        Exception: If a CSV file cannot be read.

    Example:
        >>> ratings, movies = open_csv('data/ratings.csv', 'data/movies.csv', header=True, inferSchema=True)
    """
    spark = SparkSession.builder.appName('app_name').getOrCreate()

    df_collector = []
    for url in urls:
        try:
            df = spark.read.csv(url, inferSchema=inferSchema, header=header)
            df_collector.append(df)
        except Exception as e:
            raise Exception(f"Error reading file '{url}': {str(e)}")

    return tuple(df_collector)


def join_pyspark_df(df1, df2, column_name="movieId"):
    """
    Joined 2 Pyspark DF with a common column_name and returns the joined DF.

    Args:
        df1 (df PySpark): first df to join
        df2 (df PySpark): second df to join
        column_name (str): the name on which joined both df
    
    Returns:
        PySpark df: a PySpark df who contains the both of previous df joined with the
        common column delete once.

    Raises:
        Exception: if one of the PySpark df is missing 

    Example:
        >>> final_df = join_pyspark_df(ratings, movies, "movieId")
    """
    if df1 is None or df2 is None:
        raise ValueError("Both df must be provided.")
    joined_df = df1.join(df2,df1[column_name]==df2[column_name]).drop(df1[column_name])
    return joined_df


def model_train_saving (data_sdf):
    # Initialize the model
    als = ALS(userCol="userId", itemCol = "movieId", ratingCol = "rating", coldStartStrategy='drop')
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
    als.write().overwrite().save("./model/ALS_Movie_Rec_model")
    print("Model is saved")

def model_training():
    ratings, movies = open_csv(url1, url2)
    df_final = join_pyspark_df(ratings, movies, "movieId")
    model_train_saving(df_final)

if __name__ == "__main__":
    model_training()
