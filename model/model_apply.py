def title_rec_given_user(user_id : int, df, model_loaded):
    """
    Give the recommended movies'titles for a given user sorted from the best recommendations to the worst
    in our dataset (df) who has the format "pyspark.sql.dataframe.DataFrame"
    """
    #taking the movieId, userId and title for the given user_id
    user = df.filter(df['userId'] == user_id).select(['movieId','userId', 'title', 'year','title_only'])
    #Take the recommendations for the user defined the line above
    recommendations = model_loaded.fit(df).transform(user)
    #Show the recommended movies for that user sorted from the best recommendations to the worst
    title_rec = recommendations.orderBy('prediction',ascending=False).select('title_only','year')

    return title_rec.collect()