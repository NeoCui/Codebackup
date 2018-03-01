# main.py

import os
from db_setup import init_db, db_session
from forms import SearchForm, RecordForm
from flask import Flask, flash, render_template, request, redirect
from models import Album, Artist
from tables import Results

init_db()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/new_record', methods=['GET', 'POST'])
def new_record():
	form = RecordForm(request.form)
	if request.method == 'POST' and form.validate():
		# save the record 
		record = Album()
		save_changes(record, form, new=True)
		flash('Record created successfully!')
		return redirect('/')
	return render_template('new_record.html', form=form)

def save_changes(record, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    artist = Artist()
    artist.name = form.artist.data

    record.artist = artist
    record.title = form.title.data
    record.release_date = form.release_date.data
    record.publisher = form.publisher.data
    record.media_type = form.media_type.data

    if new:
        # Add the new album to the database
        db_session.add(record)

    # commit the data to the database
    db_session.commit()

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Album).filter(
                Album.id==id)
    record = qry.first()

    if record:
        form = RecordForm(formdata=request.form, obj=record)
        if request.method == 'POST' and form.validate():
			form = RecordForm(request.form)
			# save edits 
			save_changes(record, form)
			flash('Record updated successfully!')
        return render_template('edit_record.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


if __name__ == '__main__':
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(debug=True, host='10.245.39.75', port=8000)
