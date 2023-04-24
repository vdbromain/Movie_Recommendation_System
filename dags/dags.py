# Personnal Functions for the dag to run
from model_training import model_training
# Model use to make recommendations
from pyspark.ml.recommendation import ALS
# Model evaluation
from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('app_name').getOrCreate()

#AIRFLOW
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator 

#To manage the dates
from datetime import datetime, timedelta

#Defining the default_args for the DAG
defaults_args = {
    "owner": "Romain",
    "description": "Training and saving the model",
    "depends_on_past" : False,
    "start_date" : datetime(2023, 4, 20),
    "email": ['admin@admin.be'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

#Defining the dag => #0 0 * * * is the same as @daily makes the same "everyday at midnight"
#Catchup=False to not make the tasks from the start_date until now when I'll launch it
with DAG("Training_saving_model", default_args=defaults_args, schedule_interval='0 0 * * *', catchup=False) as dag : 

    #Defining the PythonOperator to call the function everyday at midnight
    #yahoo_scrapper = PythonOperator(task_id="yahoo_scrapper", python_callable=print_thg, op_kwargs={'what_I_have_to_print':"I'm in the first print"}, dag=scrapping_dag)
    
    #Start_end
    start_task = EmptyOperator(task_id="start_task")
    #end_dag
    end_task = EmptyOperator(task_id="end_task")
    #Print the first task is finished
    training_saving_model_task = PythonOperator(task_id="training_saving_model_task", python_callable=model_training)

#Defining the dependencies
start_task >> training_saving_model_task >> end_task