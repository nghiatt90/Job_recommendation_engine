# Job recommendation demo

A simple web app demonstrating a basic job recommendation system.

Forked from https://github.com/jalajthanaki/Job_recommendation_engine


## Dataset

* You can download dataset from this [link](https://www.kaggle.com/c/job-recommendation/data)
* Make a folder `input`
* Put all datafiles (.tsv) inside this folder

## Usage

1. Run the `Data Processing.ipynb` notebook to preprocess the data.
2. Use [Flask](http://flask.pocoo.org/) to run the file `job_recommend.py`

## Basic functions

1. Main page: `http://<flask server>:<port>/`
2. Data pages:
  - `http://<flask server>:<port>/all_users`
  - `http://<flask server>:<port>/all_jobs`
  - `http://<flask server>:<port>/all_history`
3. Recommendation page: `http://<flask server>:<port>/recommend?user_id=<user_id>`
4. Job details: `http://<flask server>:<port>/job_details/<job_id>`
