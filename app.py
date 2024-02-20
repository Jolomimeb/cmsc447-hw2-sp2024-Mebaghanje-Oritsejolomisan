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


@app.route('/updatestudent', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        try:
            old_id = request.form['old_id']
            new_id = request.form['new_id']
            new_name = request.form['new_name']
            new_points = request.form['new_points']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE students SET Id = ?, name = ?, Points = ? WHERE Id = ?", (new_id, new_name, new_points, old_id))
                con.commit()

                msg = "Record successfully updated"
        except:
            con.rollback()
            msg = "Error in update operation"
        finally:
            con.close()
            return render_template("result.html", msg=msg)

    return render_template('update_student.html')



if __name__ == '__main__':
    #enables us to auto reload application
    app.run(debug=True)