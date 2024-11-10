from flask import Flask, render_template, request, redirect, url_for
from DBmain import *
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'mysecretkey'


DatabaseSession = sessionmaker(bind=engine)  # Nu folosi 'session'
database_session = DatabaseSession()  # Foloseste 'database_session'


@app.route('/')
@app.route('/homepage')
def homepage():
    produse = database_session.query(Produs).all()
    return render_template('homepage.html', produse=produse)


@app.route('/adauga', methods=['GET', 'POST'])
def adauga_produs():
    if request.method == 'POST':
        nume = request.form.get('nume')
        if nume:
            produs_nou = Produs(nume=nume, cumparat=False)
            database_session.add(produs_nou)
            database_session.commit()
            return redirect(url_for('homepage'))
    return render_template('adauga_produs.html')


@app.route('/sterge/<int:produs_id>', methods=['POST'])
def sterge_produs(produs_id):
    produs = database_session.query(Produs).get(produs_id)
    if produs:
        database_session.delete(produs)
        database_session.commit()
    return redirect(url_for('homepage'))


@app.route('/marcheaza_cumparat/<int:produs_id>', methods=['POST'])
def marcheaza_cumparat(produs_id):
    produs = database_session.query(Produs).get(produs_id)
    if produs:
        produs.cumparat = True
        database_session.commit()
    return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.run(debug=True)
