from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Connect to the database
conn = psycopg2.connect(database='flask_db',
                        user="postgres",
                        password="1234",
                        host="localhost", port="5432")

# Create a cursor
cur = conn.cursor()

# if you already have any table or not it doesn't matter
# will create a todo table for you.

cur.execute( 
    '''CREATE TABLE IF NOT EXISTS todo (id serial  
    PRIMARY KEY, name varchar(100), note text);''')

# Insert some data into the table
cur.execute(
    '''INSERT INTO todo (name, note) VALUES
        ('Update Resume', 'Make sure to add current job.'), ('Dishes', 'Finish by Friday'), ('Shopping', 'Prep for mom and dad');''')

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

@app.route('/')
def index():
    # Connect to the database
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    
    # Create a cursor
    cur = conn.cursor()

    # Select all todos from the table
    cur.execute('''Select * FROM todo''')

    # Fetch the data
    data = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

@app.route('/create', methods=['POST'])
def create():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    note = request.form['note']

    # Insert the data into the table
    cur.execute(
        '''INSERT INTO todo \
        (name, note) VALUES (%s, %s)''',
        (name, note))
    
    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    
    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    note = request.form['note']
    id = request.form['id']

    # update the data in the table
    cur.execute(
        '''UPDATE todo SET name=%s,
        note=%s WHERE id=%s''', (name, note, id))
    
    # commit the changes
    conn.commit()
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST']) 
def delete(): 
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor() 
  
    # Get the data from the form 
    id = request.form['id'] 
  
    # Delete the data from the table 
    cur.execute('''DELETE FROM todo WHERE id=%s''', (id,)) 
  
    # commit the changes 
    conn.commit() 
  
    # close the cursor and connection 
    cur.close() 
    conn.close() 
  
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run()
