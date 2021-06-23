from flask import Flask,render_template, flash, request, redirect, url_for
from flask_mysqldb import MySQL

app=Flask(__name__)


# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_PORT'] = 3370 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'PetsMedicalHistory'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def pet():
    return render_template('petInfo.html')


@app.route('/petInfo')
def petInfo():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * from Pet')
    data=cur.fetchall()
    print(data)    
    return render_template('petInfo.html',pets=data)


@app.route('/edit/<id>')
def get_pet(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * from Pet where idPet = {0}'.format(id))
    data = cur.fetchall()  
    return render_template('editPet.html', pet=data[0])



@app.route('/update/<id>', methods=['POST'])
def update_pet(id):
  if request.method == 'POST':
        petName = request.form['petName']
        age = request.form['age']
        race = request.form['race']
        specie = request.form['specie']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Pet
            SET petName = %s,
                age = %s,
                race = %s,
                specie = %s
            WHERE idPet = %s
        """, (petName, age, race, specie,id))
        flash('Pet updated successfully')
        mysql.connection.commit()
        return redirect(url_for('petInfo'))
    
    
@app.route('/delete/<id>')
def delete_pet(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM Pet WHERE idPet= {0}'.format(id))
    mysql.connection.commit()
    flash('Pet removed successfully')
    return redirect(url_for('petInfo'))


@app.route('/create')
def create_PetView():   
    return render_template('createPet.html')

    
       
@app.route('/create', methods=['POST'])
def createPet():
    if request.method == 'POST':
        petName = request.form['petName']
        age = request.form['age']
        race = request.form['race']
        specie = request.form['specie']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Pet (petName, age, race,specie ) VALUES (%s,%s,%s,%s)",
        (petName, age, race, specie))
        mysql.connection.commit()
        flash('Pet added successfully')
        return redirect(url_for('petInfo'))

if __name__ == '__main__':
    app.run(port=3001, debug=True)
