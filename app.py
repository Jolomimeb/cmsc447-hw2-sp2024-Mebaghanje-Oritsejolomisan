from flask import Flask,render_template,request

import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_name():
    return render_template('student.html')

@app.route('/addrec',methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try: 
            nm = request.form['nm']
            idd = request.form['idd']
            points = request.form['points']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,Id,Points) VALUES (?,?,?)",(nm,idd,points))
                con.commit()

                msg = "Record succefully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()

    return render_template("list.html", rows=rows)


@app.route('/removestudent', methods=['GET', 'POST'])
def remove_student():
    if request.method == 'POST':
        try:
            id_to_delete = request.form['id']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM students WHERE Id = ?", (id_to_delete,))
                con.commit()

                msg = "Record successfully deleted"
        except:
            con.rollback()
            msg = "Error in delete operation"
        finally:
            con.close()
            return render_template("result.html", msg=msg)

    return render_template('remove_student.html')

if __name__ == '__main__':
    #enables us to auto reload application
    app.run(debug=True)