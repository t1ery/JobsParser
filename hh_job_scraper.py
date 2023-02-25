from flask import Flask, render_template, request, redirect, send_file
from parser import get_jobs
from exporter import save_to_csv

app = Flask('FlaskUser')

db = {}


# Default page which is shown by default
@app.route('/')
def home():
    return render_template('home.html')


# Report page which shows the job search results
@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        # Check if the search results for the keyword exist in the database.
        # If they do, get the data from the database, otherwise perform job parsing.
        getdb = db.get(keyword)
        if getdb:
            jobs = getdb
        else:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
        print(jobs)
    else:
        return redirect('/')
    return render_template('report.html', searchBy=keyword, resultsNumber=len(jobs), jobs=jobs)


# Export page which allows exporting job search results in CSV format
@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        # Get the data from the database and save it to the CSV file.
        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file('jobs.csv')
    except:
        return redirect('/')


app.run(host='0.0.0.0')
