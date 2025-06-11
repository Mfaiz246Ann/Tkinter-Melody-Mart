import sqlite3

DB_NAME = 'music_store.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            jenis TEXT NOT NULL,
            stok INTEGER NOT NULL,
            harga REAL NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS supplier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kontak TEXT,
            alamat TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pelanggan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kontak TEXT,
            alamat TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS penjualan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            id_pelanggan INTEGER,
            total REAL NOT NULL,
            FOREIGN KEY(id_pelanggan) REFERENCES pelanggan(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS detail_penjualan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_penjualan INTEGER NOT NULL,
            id_produk INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            harga REAL NOT NULL,
            FOREIGN KEY(id_penjualan) REFERENCES penjualan(id),
            FOREIGN KEY(id_produk) REFERENCES produk(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pembelian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            id_supplier INTEGER,
            total REAL NOT NULL,
            FOREIGN KEY(id_supplier) REFERENCES supplier(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS detail_pembelian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pembelian INTEGER NOT NULL,
            id_produk INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            harga REAL NOT NULL,
            FOREIGN KEY(id_pembelian) REFERENCES pembelian(id),
            FOREIGN KEY(id_produk) REFERENCES produk(id)
        )
    ''')
    conn.commit()
    conn.close()

# CRUD Produk
def tambah_produk(nama, jenis, stok, harga):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO produk (nama, jenis, stok, harga) VALUES (?, ?, ?, ?)', (nama, jenis, stok, harga))
    conn.commit()
    conn.close()

def get_all_produk():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM produk')
    rows = c.fetchall()
    conn.close()
    return rows

def update_produk(id, nama, jenis, stok, harga):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE produk SET nama=?, jenis=?, stok=?, harga=? WHERE id=?', (nama, jenis, stok, harga, id))
    conn.commit()
    conn.close()

def hapus_produk(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM produk WHERE id=?', (id,))
    conn.commit()
    conn.close()

# CRUD Supplier
def tambah_supplier(nama, kontak, alamat):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO supplier (nama, kontak, alamat) VALUES (?, ?, ?)', (nama, kontak, alamat))
    conn.commit()
    conn.close()

def get_all_supplier():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM supplier')
    rows = c.fetchall()
    conn.close()
    return rows

def update_supplier(id, nama, kontak, alamat):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE supplier SET nama=?, kontak=?, alamat=? WHERE id=?', (nama, kontak, alamat, id))
    conn.commit()
    conn.close()

def hapus_supplier(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM supplier WHERE id=?', (id,))
    conn.commit()
    conn.close()

# CRUD Pelanggan
def tambah_pelanggan(nama, kontak, alamat):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO pelanggan (nama, kontak, alamat) VALUES (?, ?, ?)', (nama, kontak, alamat))
    conn.commit()
    conn.close()

def get_all_pelanggan():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pelanggan')
    rows = c.fetchall()
    conn.close()
    return rows

def update_pelanggan(id, nama, kontak, alamat):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE pelanggan SET nama=?, kontak=?, alamat=? WHERE id=?', (nama, kontak, alamat, id))
    conn.commit()
    conn.close()

def hapus_pelanggan(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM pelanggan WHERE id=?', (id,))
    conn.commit()
    conn.close()

# Penjualan
def tambah_penjualan(tanggal, id_pelanggan, total, items):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO penjualan (tanggal, id_pelanggan, total) VALUES (?, ?, ?)', (tanggal, id_pelanggan, total))
    penjualan_id = c.lastrowid
    for item in items:
        c.execute('INSERT INTO detail_penjualan (id_penjualan, id_produk, qty, harga) VALUES (?, ?, ?, ?)', (penjualan_id, item['id_produk'], item['qty'], item['harga']))
        c.execute('UPDATE produk SET stok = stok - ? WHERE id = ?', (item['qty'], item['id_produk']))
    conn.commit()
    conn.close()

def get_all_penjualan():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM penjualan')
    rows = c.fetchall()
    conn.close()
    return rows

def get_detail_penjualan(id_penjualan):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM detail_penjualan WHERE id_penjualan=?', (id_penjualan,))
    rows = c.fetchall()
    conn.close()
    return rows

# Pembelian
def tambah_pembelian(tanggal, id_supplier, total, items):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO pembelian (tanggal, id_supplier, total) VALUES (?, ?, ?)', (tanggal, id_supplier, total))
    pembelian_id = c.lastrowid
    for item in items:
        c.execute('INSERT INTO detail_pembelian (id_pembelian, id_produk, qty, harga) VALUES (?, ?, ?, ?)', (pembelian_id, item['id_produk'], item['qty'], item['harga']))
        c.execute('UPDATE produk SET stok = stok + ? WHERE id = ?', (item['qty'], item['id_produk']))
    conn.commit()
    conn.close()

def get_all_pembelian():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pembelian')
    rows = c.fetchall()
    conn.close()
    return rows

def get_detail_pembelian(id_pembelian):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM detail_pembelian WHERE id_pembelian=?', (id_pembelian,))
    rows = c.fetchall()
    conn.close()
    return rows 