from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

  #setting up reviews

#database creation
con = sqlite3.connect('reviews.db', check_same_thread=False)
cur = con.cursor()

#creating the Turkey review table
create_db_query = "CREATE TABLE IF NOT EXISTS Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10), review TEXT NOT NULL)"
cur.execute(create_db_query)

#creating Japan review table
japan_create_db_query = "CREATE TABLE IF NOT EXISTS Japan_Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10), review TEXT NOT NULL)"
cur.execute(japan_create_db_query)

#creating Colombia review table
colombia_create_db_query = "CREATE TABLE IF NOT EXISTS Colombia_Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10), review TEXT NOT NULL)"
cur.execute(colombia_create_db_query)

#creating South Africa review table
SA_create_db_query = "CREATE TABLE IF NOT EXISTS SA_Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10), review TEXT NOT NULL)"
cur.execute(SA_create_db_query)

#creating Spain review table
SA_create_db_query = "CREATE TABLE IF NOT EXISTS Spain_Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10), review TEXT NOT NULL)"
cur.execute(SA_create_db_query)

#creating users table
create_db_query = "CREATE TABLE IF NOT EXISTS Users(username TEXT, password TEXT, email TEXT)"
cur.execute(create_db_query)


#printing results
#cur.execute("INSERT INTO Reviews Values('Joe', 9, 'Great Country!')")
results = cur.execute('SELECT * FROM Reviews')
print("The following below are reviews from Turkey")
print(results)
print([result for result in results])
print("End of reviews")

#printing Japan results
japan_results = cur.execute('SELECT * FROM Japan_Reviews')
print("The following below are reviews from Japan")
print(japan_results)
print([result for result in japan_results])
print("End of reviews")

#printing Colombia results
colombia_results = cur.execute('SELECT * FROM Colombia_Reviews')
print("The following below are reviews from Colombia")
print(colombia_results)
print([result for result in colombia_results])
print("End of reviews")

#printing South Africa results
SA_results = cur.execute('SELECT * FROM SA_Reviews')
print("The following below are reviews from South Africa")
print(SA_results)
print([result for result in SA_results])
print("End of reviews")

#printing South Africa results
spain_results = cur.execute('SELECT * FROM Spain_Reviews')
print("The following below are reviews from Spain")
print(spain_results)
print([result for result in spain_results])
print("End of reviews")

#printing users data
users_results = cur.execute('SELECT * FROM Users')
print("The following below are Users username and password")
print(users_results)
print([result for result in users_results])

#app route to home page
@app.route('/')
def index():
    return render_template("index.html")

#app route to turkey page, updating results/score in the process
@app.route('/turkey')
def turkey():
  results = cur.execute('SELECT * FROM Reviews ORDER BY rowid DESC').fetchall()
  processed_results = [result for result in results]
  average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Reviews').fetchone()[0]
  return render_template("turkey.html", results=processed_results, score=average_score)

#app route to login page
@app.route('/login')
def login():
    return render_template('login.html')
    
#app route to currency page  
@app.route('/currency')
def currency():
    return render_template("currency.html")

#app route to services page
@app.route('/services')
def services():
    return render_template("services.html")

#app route to about page
@app.route('/about')
def about():
    return render_template("about.html")

#app route to contact us page
@app.route('/contactus')
def contactus():
  return render_template("contactus.html")

#app route to country ranking page
@app.route('/countries')
def countries():
    return render_template("countries.html")
  
#@app.route('/signup')
#def signup():
#  return render_template("test.html")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
     
        cur = con.cursor()
        cur.execute('SELECT * FROM Users WHERE username = ?', (username,))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cur.execute('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
            con.commit()
            msg = 'You have successfully registered!'
          
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    
    return render_template('test.html', msg=msg)

#app route to japan page
@app.route('/japan')
def japan():
    results = cur.execute('SELECT * FROM Japan_Reviews ORDER BY rowid DESC').fetchall()
    processed_results = [result for result in results]
    japan_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Japan_Reviews').fetchone()[0]
    return render_template("japan.html", results=processed_results, score=japan_average_score)

#app route to colombia page
@app.route('/colombia')
def colombia():
    results = cur.execute('SELECT * FROM Colombia_Reviews ORDER BY rowid DESC').fetchall()
    processed_results = [result for result in results]
    colombia_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Colombia_Reviews').fetchone()[0]
    return render_template("colombia.html", results=processed_results, score=colombia_average_score)

#app route to south africa page
@app.route('/southafrica')
def southafrica():
    results = cur.execute('SELECT * FROM SA_Reviews ORDER BY rowid DESC').fetchall()
    processed_results = [result for result in results]
    colombia_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM SA_Reviews').fetchone()[0]
    return render_template("southafrica.html", results=processed_results, score=colombia_average_score)

#app route to spain page
@app.route('/spain')
def spain():
    results = cur.execute('SELECT * FROM Spain_Reviews ORDER BY rowid DESC').fetchall()
    processed_results = [result for result in results]
    spain_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Spain_Reviews').fetchone()[0]
    return render_template("spain.html", results=processed_results, score=spain_average_score)

#review implementiation for turkey
@app.route('/review', methods=['POST'])
def review():

  name = request.form.get("name")
  score = int(request.form.get("score"))
  review = request.form.get("review")

  cur.execute(f"INSERT INTO Reviews VALUES('{name}', {score}, '{review}')")
  con.commit()

  results = cur.execute('SELECT * FROM Reviews ORDER BY rowid DESC').fetchall()
  processed_results = [result for result in results]
  average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Reviews').fetchone()[0]

  return render_template('turkey.html', results=processed_results, score=average_score)

#review implementiation for japan
@app.route('/japan_review', methods=['POST'])
def japan_review():

  name = request.form.get("name")
  score = int(request.form.get("score"))
  review = request.form.get("review")

  cur.execute(f"INSERT INTO Japan_Reviews VALUES('{name}', {score}, '{review}')")
  con.commit()

  results = cur.execute('SELECT * FROM Japan_Reviews ORDER BY rowid DESC').fetchall()
  processed_results = [result for result in results]
  japan_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Japan_Reviews').fetchone()[0]

  return render_template('japan.html', results=processed_results, score=japan_average_score)

#review implementiation for colombia
@app.route('/colombia_review', methods=['POST'])
def colombia_review():

  name = request.form.get("name")
  score = int(request.form.get("score"))
  review = request.form.get("review")

  cur.execute(f"INSERT INTO Colombia_Reviews VALUES('{name}', {score}, '{review}')")
  con.commit()

  results = cur.execute('SELECT * FROM Colombia_Reviews ORDER BY rowid DESC').fetchall()
  processed_results = [result for result in results]
  colombia_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Colombia_Reviews').fetchone()[0]

  return render_template('colombia.html', results=processed_results, score=colombia_average_score)

#review implementiation for south africa
@app.route('/southafrica_review', methods=['POST'])
def southafrica_review():

  name = request.form.get("name")
  score = int(request.form.get("score"))
  review = request.form.get("review")

  cur.execute(f"INSERT INTO SA_Reviews VALUES('{name}', {score}, '{review}')")
  con.commit()

  results = cur.execute('SELECT * FROM SA_Reviews ORDER BY rowid DESC').fetchall()
  processed_results = [result for result in results]
  colombia_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM SA_Reviews').fetchone()[0]

  return render_template('southafrica.html', results=processed_results, score=colombia_average_score)

#review implementiation for spain
@app.route('/spain_review', methods=['POST'])
def spain_review():

  name = request.form.get("name")
  score = int(request.form.get("score"))
  review = request.form.get("review")

  cur.execute(f"INSERT INTO Spain_Reviews VALUES('{name}', {score}, '{review}')")
  con.commit()

  results = cur.execute('SELECT * FROM Spain_Reviews ORDER BY rowid DESC').fetchall()
  processed_results = [result for result in results]
  spain_average_score = cur.execute('SELECT ROUND(AVG(score), 2) FROM Spain_Reviews').fetchone()[0]

  return render_template('spain.html', results=processed_results, score=spain_average_score)
  
app.run(host='0.0.0.0', port=5000)
