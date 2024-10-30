from flask import Flask
import sqlite3 as sql

con = sql.connect('dbInventory.db')
print("Database berhasil dibuat!")

con.execute('CREATE TABLE IF NOT EXISTS tbInventory (id SERIAL PRIMARY KEY,  name VARCHAR(100) NOT NULL, '
            'quantity INT NOT NULL, description TEXT)')
print("Table cread succesfully")
con.close()
