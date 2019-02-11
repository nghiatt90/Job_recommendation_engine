import pandas as pd

# Pre-load data, might take some time
jobs = pd.read_csv('data/processed/jobs.csv')
users = pd.read_csv('data/processed/users.csv')
apps = pd.read_csv('data/processed/applications.csv')
