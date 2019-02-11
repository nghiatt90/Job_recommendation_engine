import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.metrics import pairwise

import global_data


user_similarity_matrix = None
job_similarity_matrix = None
user_index = None
job_index = None


def build_user_similarity_matrix():
    global user_similarity_matrix
    users = global_data.users
    users_combined = pd.DataFrame({'UserID': users.UserID})
    users_combined['Data'] = (
            users['City'] + ' '
            + users['State'] + ' '
            + users['DegreeType'] + ' '
            + users['Major'] + ' '
            + users['AllTitles']
    )

    tfidf = text.TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(users_combined['Data'])
    user_similarity_matrix = pairwise.linear_kernel(tfidf_matrix, tfidf_matrix)
    return user_similarity_matrix


def build_job_similarity_matrix():
    global job_similarity_matrix
    jobs = global_data.jobs
    jobs_combined = pd.DataFrame({'JobID': jobs.JobID})
    jobs_combined['Data'] = (
            jobs['Title'] + ' '
            + jobs['Description'] + ' '
            + jobs['City'] + ' '
            + jobs['State']
    )
    tfidf = text.TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(jobs_combined['Data'])
    job_similarity_matrix = pairwise.linear_kernel(tfidf_matrix, tfidf_matrix)
    return job_similarity_matrix


def build_user_index():
    global user_index
    user_index = pd.Series(global_data.users.index, index=global_data.users.UserID)
    return user_index


def build_job_index():
    global job_index
    job_index = pd.Series(global_data.jobs.index, index=global_data.jobs.JobID)
    return job_index


def recommend_by_similar_users(user_id, n_similar_users=50, n_jobs=5):
    apps = global_data.apps
    jobs = global_data.jobs
    users = global_data.users

    idx = user_index[user_id]
    similar_user_indices = np.argsort(-user_similarity_matrix[idx])[1:n_similar_users + 1]
    similar_user_ids = users.iloc[similar_user_indices].UserID
    applications = apps[apps.UserID.isin(similar_user_ids)]
    job_ids = applications.JobID.tolist()
    recommendable_jobs = pd.DataFrame(data=jobs[jobs.JobID.isin(job_ids)])
    return recommendable_jobs.head(n_jobs)


def recommend_by_similar_jobs(user_id, n_jobs=5):
    apps = global_data.apps
    jobs = global_data.jobs

    applied_job_ids = apps.loc[apps.UserID == user_id, 'JobID']
    applied_job_indices = list(set([job_index[x] for x in applied_job_ids]))
    similarity_scores = job_similarity_matrix[applied_job_indices].sum(axis=0)
    similar_job_indices = np.argsort(-similarity_scores)[:n_jobs + len(applied_job_indices)]
    similar_job_indices = list(set(similar_job_indices) - set(applied_job_indices))
    recommendable_jobs = jobs.iloc[similar_job_indices].copy()

    return recommendable_jobs[:n_jobs]
