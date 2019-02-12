import html
import re


def create_job_hyperlinks(job_df):
    job_df = job_df.copy()
    if 'JobID' in job_df.columns:
        job_df.JobID = job_df.JobID.apply(lambda x: f'<a href="job_details/{x}">{x}</a>')
    if 'Description' in job_df.columns:
        job_df.Description = job_df.Description.apply(html.escape)
    if 'Requirements' in job_df.columns:
        job_df.Requirements = job_df.Requirements.apply(html.escape)
    return job_df.to_html(escape=False)


def beautify(text):
    return re.sub(r'\\r\\n|\\r|\\n', '<br>', text)
