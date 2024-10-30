from flask import Flask, render_template, request, url_for, redirect, session, flash,g
import random
import sqlite3 as sql
app = Flask (__name__)
app.secret_key = 'pemrograman-web-framework'

#inisialisasi variabel database
DATABASE = "dbInventory.db"

#fungsi ambil database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.route ('/')
def main():
    if 'username' in session:
        suhu = round(random.uniform(10, 40), 2)
        username = session['username']
        lampuSts = 0
        resultData = {
            'username' : username,
            'suhu'     : suhu,
            'lampu'    : lampuSts
        }
        return render_template("index.html", **resultData)
    else:
        return render_template("session.html")

@app.route ('/login', methods =["POST", "GET"] )
def login():
    if 'username' in session:
        username = session['username']
        return render_template("index.html", username=username)
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if ((password != "BOE-Malang") or (username !='Maklon')):
                flash("Invalid: username anda password")
                return render_template("login.html", name="Username and password invalid")
            else:
                session['username'] = request.form["username"]
                flash("Success login")
                return redirect(url_for('main'))
        else:
            return render_template("login.html")

@app.route ('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route ('/home')
def home():
    if 'username' in session:
        suhu = round(random.uniform(10, 40), 2)
        username = session['username']
        lampuSts = 0
        resultData = {
            'username' : username,
            'suhu'     : suhu,
            'lampu'    : lampuSts
        }
        return render_template ('index.html', **resultData)
    else:
        return redirect(url_for('main'))

@app.route("/<deviceName>/<action>")
def action (deviceName, action):
    lampuSts=0
    if 'username' in session:
        if deviceName == 'lampu':
            actuator = 1
        if action == "on":
            lampuSts = 1
        if action == "off":
            lampuSts = 0

        suhu = round(random.uniform(10, 40), 2)
        username = session['username']
        resultData = {
            'username' : username,
            'suhu'     : suhu,
            'lampu'    : lampuSts
        }
        return render_template ('index.html', **resultData)
    else:
        return redirect(url_for('main'))

@app.route ('/about')
def about():
    if 'username' in session:
        return render_template("about.html")
    else:
        return redirect(url_for('main'))

@app.route ('/barang')
def barang():
    if 'username' in session:
        return render_template("barang.html")
    else:
        return redirect(url_for('main'))

@app.route ('/result', methods =["POST", "GET"] )
def result():
    if request.method == "POST":
        result = request.form
        return render_template("result.html", result=result)
    else:
        result = request.form
        return render_template("result.html", result=result)

#route tampilkan data student dalam tabel
@app.route('/tampil_barang')
def tampil_barang():
    if 'username' in session:
        cur = get_db().cursor()
        cur.execute("SELECT * FROM tbInventory")
        result = cur.fetchall()
        return render_template('barang_table.html', items=result)
    else:
        return redirect(url_for('main'))

#route tampilkan (show) data detail student
@app.route('/show/<string:idb>',  methods=['GET', 'POST'])
def show_barang(idb):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM tbInventory WHERE id = ?", (idb,))
    result = cur.fetchall()
    return render_template('result.html', result=result)

#route tampilkan halaman edit data student
@app.route('/edit_barang/<string:idb>',  methods=['GET', 'POST'])
def edit_barang(idb):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM tbInventory WHERE id = ?", (idb,))
    result = cur.fetchall()
    return render_template('barang_edit.html', result=result)

#route update data student
@app.route('/update_barang/<string:idb>', methods=['GET', 'POST'])
def update_barang(idb):
    if 'username' in session:
        cur = get_db().cursor()
        if request.method == 'POST':
            id_barang = request.form['idb'].strip()
            name = request.form['name'].strip()
            qa = request.form['qa'].strip()
            des = request.form['des'].strip()

            cur.execute("UPDATE tbInventory SET name = ?, quantity = ?, description = ? WHERE id = ?",
                        (name, qa, des, id_barang))
            get_db().commit()
            flash("OKEdit")
            return redirect(url_for('tampil_barang'))
        else:
            flash("ERROR")
            return redirect(url_for('tampil_barang'))
    else:
        return redirect(url_for('main'))

#route add student_(tambah data)
@app.route('/add_barang', methods=['GET', 'POST'])
def add_barang():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name'].strip()
            qa = request.form['qa'].strip()
            des = request.form['des'].strip()

            #Memeriksa_apakah_field_kosong
            if not name or not qa or not des:
                flash('ERROR')
                return redirect(url_for('tampil_barang'))

            cur = get_db().cursor()
            cur.execute("INSERT INTO tbInventory (name, quantity, description) VALUES (?, ?, ?)",
                        (name, qa, des))
            get_db().commit()
            flash("OKSave")
            return redirect(url_for('tampil_barang'))
        return render_template('barang.html')
    else:
        return redirect(url_for('main'))

#route delete data student
@app.route('/delete_barang/<string:idb>')
def delete_barang(idb):
    if 'username' in session:
        cur = get_db().cursor()
        cur.execute("DELETE FROM tbInventory WHERE id = ?", (idb,))
        get_db().commit()
        flash("OKDel")
        return redirect(url_for('tampil_barang'))
    else:
        return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
