import flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

# Initialize Falsk
app = Flask(__name__)

#Database Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin123@localhost/staff_management'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#initailize Database
db = SQLAlchemy(app)


# Define Staff Model

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    designation = db.Column(db.String(100), nullable = False)   
    dept = db.Column(db.String(100), nullable = False)
    salary = db.Column(db.Float(10,2), nullable = False)

    def __str__(self) -> str:
        return super().__str__() 
    

# Route for home page
@app.route('/')
def home():
    staffData = Staff.query.all() # fetch the data from dastabase
    return render_template('index.html',sData = staffData)

@app.route('/add', methods = ['POST'])
def add_staff():
    # Adding to database logic here
    sName = request.form['staffName']
    sDesg = request.form['designation']
    sDept = request.form['dept']
    sSalry = request.form['salary']

    # Create New Staff record
    new_staff = Staff(name = sName,designation = sDesg,dept = sDept, salary = sSalry)
    db.session.add(new_staff)
    db.session.commit() 
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods = ['GET','POST'])
def edit_staff(id):
    sData = Staff.query.get_or_404(id)
    if request.method == 'POST':
        sData.name = request.form['name']
        sData.designation = request.form['designation']
        sData.dept = request.form['dept']
        sData.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html',staff = sData)



@app.route('/delete/<int:id>', methods = ['POST'])
def delete_staff(id):
    sData = Staff.query.get_or_404(id) 
    db.session.delete(sData)       
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)



 