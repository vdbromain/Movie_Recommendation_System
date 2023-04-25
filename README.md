<div>
<h1 align="center"> Movie Recommendation System </h1>
</div>

## Description

In this project, I implemented a movie recommendation system script using PySpark, Streamlit, Apache Airflow, Docker and PostgreSQL together.

Duration : `7 days

## Tools

- PySpark : Python library for manipulating BigData faster and more powerfully than with Pandas.

- Streamlit : Python library for creating a nice app to deploy.

- Apache Airflow : Python library to schedule scripts.

- Docker : an application to run other applications in isolated small boxes named containers which are built from an image who is built from a Dockerfile or a docker-compose.yml file.

- PostgreSQL : an open-source and powerful database who is scalable for the most complex workloads, if needed.  

## Project Structure

- Dags folder : defines airflow's DAGs (Directed Acyclic Graph) in one file and my model_training function in another one. 
  
  An Airflow DAG is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies.
  
  ![DAG.png](/Users/cecilewinand/Desktop/BeCode_Projects/Movie_Recommendation_System/img/DAG.png)

- Data folder : stores the csv files and the database script.

- Docker folder : contains 2 differents folders : One for airflow who contains the Docker_airflow file and ist requirements.txt file and the other one who contains the Docker_streamlit file and its requirements.txt file also. All these files create the environnement where everything will work toegheter.

- Model folder: contains a folder with the model from PySpark who makes the recommendations, saved. And a python script with a function to access the recommendations the model made for the data the user will give us.

Here is a picture to show you the project's structure

![Main_diag_airflow.png](/Users/cecilewinand/Desktop/BeCode_Projects/Movie_Recommendation_System/img/app_movie_recom_diag.png)

As you can see in the airflow-container, airflow is managing everything.

To clarify the relation between the three containers, the posgresql-container stores only the database. My python script (who is located in the airflow-container) contains the function who reruns the model when it's updated. PySpark manages the datas, trains and tests the model.

The streamlit-container displays the app has who could see it at the end. PySpark is needed to open the datasets, the model who was saved in the first container and to count the number of users in the datasets.

The postgresql-container contains the database with the tables where the csv files will be stored in the next version. Right now, the database exists and I manage to connect to it and to write the tables in it from the streamlit-container.

## Installation and Usage

1. To launch this project, you'll need to install and run Docker Desktop on your computer. You can find all you need to install it here : [Download Docker Desktop | Docker](https://www.docker.com/products/docker-desktop/)

2. Clone this repo

3. Open the root of the folder in your terminal

4. Build the 3 containers at once with the docker-compose file to be able to connect to the streamlit app and to the airflow web UI if you want, to see the results of the movies recommendations for a defined user ID. All of this, with this simple command :
   
   ```docker
   docker compose up
   ```
   
   It will take a bit a time for docker to build each image it needs to finally run the containers after a few minutes.

5. When everything runs succesfully with a result like this in your terminal :
   
   ![DAG.png](/Users/cecilewinand/Desktop/BeCode_Projects/Movie_Recommendation_System/img/terminal_docker_compose.png)

6. As the three dockers'containers are on the same network, you can click on this link to see the streamlit app live : [http://0.0.0.0:8501/](http://0.0.0.0:8501/)

7. Now, you can play a bit around with the app, enjoy !

8. If you want to go to the Airflow's portal you can click on this link : http://0.0.0.0:9090/
   
   Username : admin
   
   Password : admin
   
   ![Airflow_Login.png](/Users/cecilewinand/Desktop/BeCode_Projects/Movie_Recommendation_System/img/login.png)

9. You click on the button on the left to activate the DAG and afterwards on the little play arrow under actions on the right. A few seconds later, you'll see a new folder named "ALS_Movie_Rec_model" in the model folder that contains the new files for the model who has just been saved. If you already have a folder called "ALS_Movie_Rec_model", delete it and you'll see it'll appear after running the dag.
   
   
   
   ![Airflow_Dag_Page.png](/Users/cecilewinand/Desktop/BeCode_Projects/Movie_Recommendation_System/img/main_screen.png)

## Results

My solution scraped Yahoo Finance data for one ticker ("ACN") daily following a preset shcedule. The stock informations obtained from the scraper includes :

- Date

- Open

- High

- Low

- Close*

- Ajd Close**

- Volume

which are important to investors interested in financial markets.

The main goal for this project was creating a script that automates the processes. This structure can be "easily" adapted to scrap data from multiple companies, updated regularly on an user defined scheduled, used on any operating system, and deployed online if needed.

## Improvements

- ###### scrapper
  
  - Adapt the scrapping script to scrap stock informations of 100+ companies
  
  - Implement threading to speed up the scraping process

- ###### data's storage :
  
  - Create a database to store the scraped data to facilitate data management (updating) and access to it

- ###### docker
  
  - Create a docker-compose file to skip step 4 to step 7 included in the installation and usage procédure above.

- ###### deployment
  
  - Deploy it on the cloud 
  
  - Create an online app where users could interact directly with the scraper selecting the ticker, the timing range... they want.

## Contact

<div>
<a href="https://github.com/vdbromain">
  <img title="" src="img/GitHub-logo.png" alt="GitHub-logo.png" width="62">
</a>
<a href="https://www.linkedin.com/in/vdbromain/">
  <img title="" src="img/linked-in-logo.png" alt="linked-in-logo.png" width="62">
</a>
</div>
