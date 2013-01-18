from flask import Flask,request,session,g,redirect,url_for,render_template
import pickle
import json
import sqlite3

app=Flask(__name__)

def init_db():
	db=sqlite3.connect('database.db')
	db.cursor().executescript("""drop table if exists entries;
				create table entries(
				filename string not null,
				imagedata string not null);""")
	db.commit()	

@app.route("/<filename>")
def draw(filename):
	wholedata=[]
	fname=[]
	db=sqlite3.connect('database.db')
	cur=db.cursor().execute('select * from entries')
	for row in cur.fetchall():
		fname.append(row[0])
		if filename==row[0]:
			wholedata=pickle.loads(str(row[1]))
	return render_template("paint11.html",lis=fname,imagedata=wholedata)
	

@app.route("/h/",methods=['POST'])
def h():
	fname=request.form['fnam']
	imagedata=request.form['image']
	imagedata=pickle.dumps(imagedata)
	db=sqlite3.connect('database.db')	
	db.cursor().execute('insert into entries (filename,imagedata) values (?,?)',[fname,imagedata])
	db.commit()
	db.close()
	return redirect(url_for('hello'))
	
@app.route("/")
def hello():
	filename=[]
	wholedata=[]
	f= request.args.get('fnam')
	db=sqlite3.connect('database.db')
	cur=db.cursor().execute('select * from entries')
	for row in cur.fetchall():
		filename.append(row[0])
	return render_template("paint11.html",lis=filename,imagedata=wholedata) 

if __name__=="__main__":
	init_db()
	app.run()
