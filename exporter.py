import csv


# save vacancies data in CSV file format
def save_to_csv(hh_jobs):
    file = open('jobs.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in hh_jobs:
        writer.writerow(list(job.values()))
    return
