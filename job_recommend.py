import re

import flask
from flask import request

import global_data
import htmlutils
import recommend_engine


app = flask.Flask(__name__)

# Pre-build similarity matrices
recommend_engine.build_user_similarity_matrix()
recommend_engine.build_job_similarity_matrix()
recommend_engine.build_user_index()
recommend_engine.build_job_index()


@app.route('/')
def main_page():
    return flask.render_template(
        'main_page.html',
        sample_users=global_data.users.head().to_html(),
        sample_jobs=htmlutils.create_job_hyperlinks(global_data.jobs.head()),
    )


@app.route('/recommend')
def recommend():
    user_id = int(request.args.get('user_id'))
    recommendations_by_similar_users = recommend_engine.recommend_by_similar_users(user_id)
    recommendations_by_similar_jobs = recommend_engine.recommend_by_similar_jobs(user_id)

    past_applications = global_data.apps[global_data.apps.UserID == user_id]
    past_applications = past_applications.join(global_data.jobs.set_index('JobID'), on='JobID').dropna()

    return flask.render_template(
        'recommendations.html',
        user_info=global_data.users[global_data.users.UserID == user_id].to_html(),
        app_history=htmlutils.create_job_hyperlinks(past_applications),
        recommendations_by_similar_users=htmlutils.create_job_hyperlinks(recommendations_by_similar_users.head()),
        recommendations_by_similar_jobs=htmlutils.create_job_hyperlinks(recommendations_by_similar_jobs.head()),
    )


@app.route('/all_users')
def show_all_users():
    return global_data.users.to_html()


@app.route('/all_jobs')
def show_all_jobs():
    return htmlutils.create_job_hyperlinks(global_data.jobs)


@app.route('/all_history')
def show_all_history():
    return htmlutils.create_job_hyperlinks(global_data.apps)


@app.route('/job_details/<int:job_id>')
def show_job_details(job_id):
    job = global_data.jobs[global_data.jobs.JobID == job_id].copy()
    job.Description = job.Description.apply(htmlutils.beautify)
    job.Requirements = job.Requirements.apply(htmlutils.beautify)
    job.Title = job.Title.apply(htmlutils.beautify)

    return flask.render_template(
        'job_details.html',
        job=job,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
