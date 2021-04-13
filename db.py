import sqlite3
import datetime
import string
import random
from hashlib import sha256

from decimal import Decimal
import os

db_file = 'guildbytesPOS_database.db'

#For windows application
app_data = os.getenv('APPDATA')
DB_NAME = os.path.join(app_data,db_file)

# For a 6-char field, this one yields 2.1 billion unique IDs
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))


def create_pos_tables():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	#User settings
	try:
		with conn:
			c.execute("""CREATE TABLE about (
						id INTEGER PRIMARY KEY,
						shop_name TEXT,
						shop_address TEXT,
						shop_contacts TEXT
						)""")
	except sqlite3.Error as er:
		print("User settings ready...")


	#User settings
	try:
		with conn:
			c.execute("""CREATE TABLE sales_settings (
						id INTEGER PRIMARY KEY,
						currency TEXT,
						sales_person TEXT
						)""")
	except sqlite3.Error as er:
		print("User settings ready...")


	#Currencies
	try:
		with conn:
			c.execute("""CREATE TABLE currencies (
						id INTEGER PRIMARY KEY,
						currency_name TEXT,
						currency_code TEXT,
						currency_symbol TEXT
						)""")
	except sqlite3.Error as er:
		print("Currencies loaded...")


	#Items table
	try:
		with conn:
			c.execute("""CREATE TABLE items (
						id INTEGER PRIMARY KEY,
						uuid TEXT,
						qrcode TEXT,
						item_name TEXT,
						item_description TEXT,
						cost_price TEXT,
						unit_price TEXT,
						quantity INTEGER,
						date_added TEXT,
						last_stocked TEXT
						)""")
	except sqlite3.Error as er:
		print("Items table ready...")


	#Sales table
	try:
		with conn:
			c.execute("""CREATE TABLE sales (
						id INTEGER PRIMARY KEY,
						receipt_id TEXT,
						item_name TEXT,
						item_price TEXT,
						quantity INTEGER,
						amount TEXT,
						date_sold TEXT,
						item_uid TEXT
						)""")
	except sqlite3.Error as er:
		print("Sales table ready...")


	#Receipts table
	try:
		with conn:
			c.execute("""CREATE TABLE receipts (
						id INTEGER PRIMARY KEY,
						uuid TEXT,
						customer_name TEXT,
						customer_contact TEXT,
						customer_address TEXT,
						total_amount TEXT,
						total_payment TEXT,
						date_issued TEXT,
						date_last_paid TEXT
						)""")
	except sqlite3.Error as er:
		print("Invoices table ready...")


	#Payments table
	try:
		with conn:
			c.execute("""CREATE TABLE payments (
						id INTEGER PRIMARY KEY,
						receipt_id INTEGER,
						payment TEXT,
						date_paid TEXT
						)""")
	except sqlite3.Error as er:
		print("Payments table ready...")


	#Customers table
	try:
		with conn:
			c.execute("""CREATE TABLE customers (
						id INTEGER PRIMARY KEY,
						name TEXT,
						contact TEXT,
						address TEXT,
						date_added TEXT
						)""")
	except sqlite3.Error as er:
		print("Customers table ready...")

	conn.close()


def create_user_table():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("""CREATE TABLE users (
						id INTEGER PRIMARY KEY,
						username TEXT,
						hash TEXT,
						access_level INTEGER
						)""")
	except sqlite3.Error as er:
		print("User exists...")


def user_settings():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("""CREATE TABLE user_setting (
						id INTEGER PRIMARY KEY,
						login_on_startup BOOLEAN)""")
	except sqlite3.Error as er:
		print("User settings loaded...")


def user_setting_exist():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM user_setting")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def add_user_setting():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("INSERT INTO user_setting (login_on_startup) VALUES (:affirm)",
				{'affirm':True})
			print("Default setting created!")
			return True
	except sqlite3.Error as er:
		print(er)
		return False


def login_on_startup():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM user_setting")
			if c.fetchone()[1]:
				print("Login on startup")
				return True
			else:
				print("No login on startup!") 
				return False
	except sqlite3.Error as er:
		print("User settings error")
		return False


def toggle_login_on_startup(state):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("UPDATE user_setting SET login_on_startup = ?",(state,))
			return True
	except sqlite3.Error as er:
		print("User settings error")
		return False


def login(username,password):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	password_hash = sha256(password.encode('utf-8')).hexdigest()
	try:
		with conn:
			c.execute("SELECT 1 FROM users WHERE username = :username and hash = :password_hash",
				{'username':username,'password_hash':password_hash})
			if c.fetchone():
				return True
			else:
				return False
	except sqlite3.Error as er:
		print("Login error!")
		return False


def users_exist():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM users")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def add_user(username,password,access_level):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	#Encrypt password
	password_hash = sha256(password.encode('utf-8')).hexdigest()

	try:
		with conn:
			c.execute("INSERT INTO users (username, hash, access_level) VALUES (:username,:password_hash,:access_level)",
				{'username':username,'password_hash':password_hash,'access_level':access_level})
			return True
	except sqlite3.Error as er:
		return False

def is_currency_set():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM currencies")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def setup_currencies(currency_name,currency_code,currency_symbol):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("INSERT INTO currencies (currency_name, currency_code, currency_symbol) VALUES (:currency_name,:currency_code,:currency_symbol)",
				{'currency_name':currency_name,'currency_code':currency_code, 'currency_symbol':currency_symbol})
			return True
	except sqlite3.Error as er:
		return False


def get_currency_by_id(c_id):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM currencies WHERE id = :c_id",{'c_id':c_id})
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def get_currency_id(currency_code):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT id FROM currencies WHERE currency_code = :currency_code",{'currency_code':currency_code})
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def get_currency_symbol(currency_code):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM currencies WHERE currency_code = :currency_code",{'currency_code':currency_code})
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def get_all_currencies():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM currencies ")
			return c.fetchall()
	except sqlite3.Error as er:
		return False


def remove_currency(currency_code):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("DELETE FROM currencies WHERE currency_code = :currency_code", {'currency_code':currency_code})
			return True
	except sqlite3.Error:
		return False


def setup_about_settings():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM about")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def setup_sales_settings():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM sales_settings")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def create_sales_settings(currency,sales_person):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("INSERT INTO sales_settings (currency, sales_person) VALUES (:currency,:sales_person)",
				{'currency':currency,'sales_person':sales_person})
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def create_about_setting(shop_name,shop_contacts,shop_address):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("INSERT INTO about (shop_name, shop_contacts, shop_address) VALUES (:shop_name,:shop_contacts,:shop_address)",
				{'shop_name':shop_name,'shop_contacts':shop_contacts,'shop_address':shop_address})
			return True
	except sqlite3.Error as er:
		return False


def update_about_settings(shop_name,shop_contacts,shop_address):
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE about SET shop_name = ?, shop_contacts = ?, shop_address = ? WHERE id = 1",(shop_name, shop_contacts,shop_address))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False


def update_currency_settings(currency, sales_person):
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE sales_settings SET currency = ?, sales_person = ? WHERE id = 1",(currency, sales_person))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False


def get_about_settings():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM about WHERE id = 1")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def get_sales_settings():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM sales_settings WHERE id = 1")
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def item_name_exists(item):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM items WHERE item_name=?",(item,))
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def item_uid_exists(item_uid):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM items WHERE uuid=?",(item_uid,))
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def select_item_by_uid(item_uid):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT * FROM items WHERE uuid=?",(item_uid,))
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def add_item(qrcode, item_name, item_description, cost_price, unit_price, quantity):
	current_datetimestamp = datetime.datetime.now()
	current_datetime = current_datetimestamp.strftime('%B %d, %Y')
	item_uid = id_generator()
	while item_uid_exists(item_uid):
		item_uid = if_generator()

	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		with conn:
			c.execute("INSERT INTO items (uuid,qrcode,item_name,item_description,cost_price,unit_price,quantity,date_added,last_stocked) VALUES (:uuid,:qrcode,:item_name,:item_desc,:cost_price,:unit_price,:quantity,:date_added,:date_stocked)",
						{'uuid':item_uid,'qrcode':qrcode,'item_name':item_name,'item_desc':item_description,'cost_price':cost_price,'unit_price':unit_price,'quantity':quantity,
						'date_added':current_datetime,'date_stocked':current_datetime})
		
		
		return True
	except sqlite3.Error as er:
		return False


def delete_from_items(uid):
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		with conn:
			c.execute("DELETE FROM items WHERE uuid = ?",(uid,))		
		
		return True
	except sqlite3.Error as er:
		return False


def get_items(match=''):
	match = '%'+match+'%'
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("SELECT * FROM items WHERE uuid LIKE ? OR item_name LIKE ? OR item_description LIKE ? OR unit_price LIKE ? OR quantity LIKE ?",
				(match,match,match,match,match))
			return c.fetchall()
	except sqlite3.Error as er:
		print("Items query failed:",er)

	conn.close()


def get_invoices(match=''):
	match = '%'+match+'%'
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("SELECT * FROM receipts WHERE uuid LIKE ?",
				(match,))
			return c.fetchall()
	except sqlite3.Error as er:
		print("Items query failed:",er)

	conn.close()


def update_receipt(invoice_uid,new_payment_amt):
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE receipts SET total_payment = ? WHERE uuid = ?",(f'{new_payment_amt}', invoice_uid))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False


def edit_item_name(item_uid,item_name):
	if item_name.strip() == "":
		return False
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE items SET item_name = ? WHERE uuid = ?",(item_name.strip(), item_uid))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False


def edit_item_desc(item_uid,item_desc):
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE items SET item_description = ? WHERE uuid = ?",(item_desc.strip(), item_uid))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False


def edit_item_price(item_uid,item_price):
	item_price = item_price.strip()
	if len(item_price) <= 0:
		return False
	else:
		try:
			i_price = Decimal(item_price)
		except:
			return False

	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE items SET unit_price = ? WHERE uuid = ?",(item_price, item_uid))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False, e


def edit_cost_price(item_uid,cost_price):
	cost_price = cost_price.strip()
	if len(cost_price) <= 0:
		return False
	else:
		try:
			c_price = Decimal(cost_price)
		except:
			return False

	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE items SET cost_price = ? WHERE uuid = ?",(cost_price, item_uid))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False, e


def edit_item_qty(item_uid,item_qty):
	if item_qty.strip() == "":
		return False
	else:
		try:
			item_qty = int(item_qty.strip())
		except ValueError:
			return False

	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("UPDATE items SET quantity = ? WHERE uuid = ?",(item_qty, item_uid))
		conn.commit()
		conn.close()
		return True
	except sqlite3.Error as e:
		return False


def customer_exists(customer_name):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM customers WHERE name=?",(customer_name,))
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def add_customer(name,contact,address):
	current_datetimestamp = datetime.datetime.now()
	current_datetime = current_datetimestamp.strftime('%B %d, %Y')
	
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		with conn:
			c.execute("INSERT INTO customers (name,contact,address,date_added) VALUES (:name,:contact,:address,:date_added)",
						{'name':name,'contact':contact,'address':address,'date_added':current_datetime})		
		
		return True
	except sqlite3.Error as er:
		return False


def get_customers(match=''):
	match = '%'+match+'%'
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("SELECT * FROM customers WHERE name LIKE ?",(match,))
			return c.fetchall()
	except sqlite3.Error as er:
		print(er)

	conn.close()


def get_customer_by_id(c_id):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("SELECT * FROM customers WHERE id=?",(c_id,))
			return c.fetchone()
	except sqlite3.Error as er:
		print(er)

	conn.close()


def receipt_uid_exists(item_uid):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM receipts WHERE uuid=?",(item_uid,))
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def add_receipt(uid,customer_name,customer_contact,customer_address,total_amt, total_pay):
	current_datetimestamp = datetime.datetime.now()
	current_datetime = current_datetimestamp.strftime('%B %d, %Y')
	
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		with conn:
			c.execute("INSERT INTO receipts (uuid,customer_name,customer_contact,customer_address,total_amount,total_payment,date_issued,date_last_paid) VALUES (:uid,:customer_name,:customer_contact,:customer_address,:total_amt,:total_pay,:date_issued,:date_last_paid)",
						{'uid':uid,'customer_name':customer_name,'customer_contact':customer_contact,'customer_address':customer_address,'total_amt':f'{total_amt:.2f}','total_pay':f'{total_pay:.2f}','date_issued':current_datetime,'date_last_paid':current_datetime})
		return uid
	except sqlite3.Error as er:
		print(er)
		return False


def get_invoice(invoice_uid):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("SELECT * FROM receipts WHERE uuid=?",(invoice_uid,))
			return c.fetchone()
	except sqlite3.Error as er:
		print(er)

	conn.close()


def get_invoice_items(invoice_uid):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		with conn:
			c.execute("SELECT * FROM sales WHERE receipt_id=?",(invoice_uid,))
			return c.fetchall()
	except sqlite3.Error as er:
		print(er)

	conn.close()


def receipt_uid_exists(uid):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT 1 FROM receipts WHERE uuid=?",(uid,))
			return c.fetchone()
	except sqlite3.Error as er:
		return False


def add_sales(receipt_id,item_name,item_price,quantity,amt,item_uid):
	current_datetimestamp = datetime.datetime.now()
	current_datetime = current_datetimestamp.strftime('%B %d, %Y')
	
	try:
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		with conn:
			c.execute("INSERT INTO sales (receipt_id,item_name,item_price,quantity,amount,date_sold,item_uid) VALUES (:invoice_uid,:item_name,:item_price,:qty,:amt,:date_sold,:item_uid)",
						{'invoice_uid':receipt_id,'item_name':item_name,'item_price':item_price,'qty':quantity,'amt':amt,'date_sold':current_datetime,'item_uid':item_uid})
		return True
	except sqlite3.Error as er:
		return False


def decrement_item_qty(item_uid,sold_qty):
	item_sold = select_item_by_uid(item_uid)
	if item_sold:
		new_qty = int(item_sold[7]) - sold_qty
		if new_qty < 0:
			new_qty = 0
		try:
			conn = sqlite3.connect(DB_NAME)
			c = conn.cursor()
			c.execute("UPDATE items SET quantity = ? WHERE uuid = ?",(new_qty, item_uid))
			conn.commit()
			conn.close()
			return True
		except sqlite3.Error as e:
			return False


