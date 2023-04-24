# To run the script => streamlit run app.py
import streamlit as st
# Personnal functions
from model.model_apply import title_rec_given_user
from dags.model_training import open_csv
from dags.model_training import join_pyspark_df
# To Load the model
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import split
from pyspark.sql.functions import regexp_extract, col
from pyspark.sql import SparkSession

# DB
import psycopg2

# To load the data
movies_path = "./data/movies.csv"
ratings_path = "./data/ratings.csv"
# Open the 2 csv files
movies_df, ratings_df = open_csv(movies_path, ratings_path)

# Joining the 2 df in a single one and deleting the duplicated column
df = join_pyspark_df(movies_df, ratings_df, "movieId")

# Extract year and the title for the title column
df = df.withColumn('year', regexp_extract(col('title'), r'\((\d{4})\)$', 1))
df = df.withColumn('title_only', split(df.title, r'[()]').getItem(0))
df = df.withColumn('title_only', split(df.title_only, ',').getItem(0))

st.title("Welcome in your movie recommendations app !")

# Compute the max value for the user_id = nb max of user in the df
nb_user = df.select(df.userId).distinct().count()

user_id = int(st.number_input(label="What's the user's id you want recommendations for ?", min_value=1, max_value=nb_user))

nb_of_rec = int(st.number_input(label="How many movies recommendations do you want ?", min_value=1, max_value=10))

wanted_year = st.radio("Do you want to see the released year for the recommended movies ?", ("Yes", "No"))

# Computing the user's datas
# Loading the model
model = ALS().load("./model/ALS_Movie_Rec_model/")

# Create the button and when you click on it, it'll run the code in the condition
if st.button("Recommendations"):
    recommendations = title_rec_given_user(user_id, df, model)
    for i in range(nb_of_rec):
        if i == 0:
            st.write(f"For the user with the id {user_id} :")
        if wanted_year == "Yes":
            st.write(f"""The movie's title for the recommendation number {i+1} is : {recommendations[i][0]} 
                    \nand has been released in {recommendations[i][1]}""")
        else : 
            st.write(f"The movie's title for the recommendation number {i+1} is : {recommendations[i][0]}")