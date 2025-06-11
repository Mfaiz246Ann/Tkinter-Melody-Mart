import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import urllib.request
import io
import musicstore_db as db

class MusicStoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        db.init_db()  # Inisialisasi database
        self.title("Toko Alat Musik - Database Management")
        self.geometry("1000x600")
        self.configure(bg="#181f2a")
        self.resizable(True, True)
        self.iconbitmap(default=None)

        # Load logo from local file using Pillow
        self.logo_img = self.load_logo_local()
        self.create_sidebar()
        self.create_header()
        self.create_dashboard()

    def load_logo_local(self):
        try:
            im = Image.open("Logo Melody_Mart.png").resize((120, 120))
            return ImageTk.PhotoImage(im)
        except Exception as e:
            print(f"Logo load error: {e}")
            return None

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#232b3e", width=200)
        self.sidebar.pack(side="left", fill="y")
        # Logo
        if self.logo_img:
            logo_label = tk.Label(self.sidebar, image=self.logo_img, bg="#232b3e")
            logo_label.image = self.logo_img
            logo_label.pack(pady=(30, 10))
        # Menu
        menu_font = ("Segoe UI", 12, "bold")
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Produk", self.show_produk),
            ("Supplier", self.show_supplier),
            ("Pelanggan", self.show_pelanggan),
            ("Penjualan", self.show_penjualan),
            ("Pembelian", self.show_pembelian),
            ("Laporan", self.show_laporan),
            ("Logout", self.quit)
        ]
        for text, cmd in buttons:
            b = tk.Button(self.sidebar, text=text, font=menu_font, bg="#232b3e", fg="#fff", bd=0, activebackground="#2e3951", activeforeground="#00e6ff", command=cmd)
            b.pack(fill="x", pady=5, padx=20)

    def create_header(self):
        self.header = tk.Frame(self, bg="#232b3e", height=60)
        self.header.pack(side="top", fill="x")
        title = tk.Label(self.header, text="Sistem Database Melody Mart - Dashboard", font=("Segoe UI", 18, "bold"), bg="#232b3e", fg="#00e6ff")
        title.pack(side="left", padx=30, pady=10)

    def create_dashboard(self):
        self.main_content = tk.Frame(self, bg="#181f2a")
        self.main_content.pack(expand=True, fill="both")
        self.show_dashboard()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_content()
        title = tk.Label(self.main_content, text="Selamat Datang di Sistem Database Melody Mart!", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#fff")
        title.pack(pady=30)
        summary_frame = tk.Frame(self.main_content, bg="#232b3e")
        summary_frame.pack(pady=10, padx=30, fill="x")
        data = [
            ("Total Produk", len(db.get_all_produk())),
            ("Total Supplier", len(db.get_all_supplier())),
            ("Total Pelanggan", len(db.get_all_pelanggan())),
            ("Penjualan Hari Ini", len(db.get_all_penjualan()))
        ]
        for i, (label, value) in enumerate(data):
            f = tk.Frame(summary_frame, bg="#232b3e", padx=30, pady=20)
            f.grid(row=0, column=i, padx=20)
            l1 = tk.Label(f, text=label, font=("Segoe UI", 12), bg="#232b3e", fg="#00e6ff")
            l1.pack()
            l2 = tk.Label(f, text=str(value), font=("Segoe UI", 20, "bold"), bg="#232b3e", fg="#fff")
            l2.pack()
        # Add app description below the summary (replace logo)
        desc_frame = tk.Frame(self.main_content, bg="#181f2a")
        desc_frame.pack(pady=(40, 10))
        desc1 = tk.Label(desc_frame, text="Project UAS Aplikasi  GUI Tkinter Python", font=("Segoe UI", 12, "bold"), bg="#181f2a", fg="#fff")
        desc1.pack()
        tk.Label(desc_frame, text="", bg="#181f2a").pack()  # Spacer
        desc2 = tk.Label(desc_frame, text="Aplikasi Database Toko Ala Musik Melody Mart", font=("Segoe UI", 12), bg="#181f2a", fg="#fff")
        desc2.pack()
        desc3 = tk.Label(desc_frame, text="Oleh Kelompok 5", font=("Segoe UI", 12), bg="#181f2a", fg="#fff")
        desc3.pack()
        desc4 = tk.Label(desc_frame, text="Dwei Puspitasari", font=("Segoe UI", 12), bg="#181f2a", fg="#fff")
        desc4.pack()
        desc5 = tk.Label(desc_frame, text="Muhammad Faiz Pohan", font=("Segoe UI", 12), bg="#181f2a", fg="#fff")
        desc5.pack()
        desc6 = tk.Label(desc_frame, text="Viana Raru Akmalia", font=("Segoe UI", 12), bg="#181f2a", fg="#fff")
        desc6.pack()

    def show_produk(self):
        self.clear_main_content()
        produk_frame = tk.Frame(self.main_content, bg="#181f2a")
        produk_frame.pack(fill="both", expand=True, padx=30, pady=20)
        title = tk.Label(produk_frame, text="Manajemen Produk", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#00e6ff")
        title.pack(anchor="w")
        # Form tambah/edit
        form_frame = tk.Frame(produk_frame, bg="#232b3e")
        form_frame.pack(fill="x", pady=10)
        tk.Label(form_frame, text="Nama", bg="#232b3e", fg="#fff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Jenis", bg="#232b3e", fg="#fff").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Stok", bg="#232b3e", fg="#fff").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(form_frame, text="Harga", bg="#232b3e", fg="#fff").grid(row=0, column=3, padx=5, pady=5)
        nama_var = tk.StringVar()
        jenis_var = tk.StringVar()
        stok_var = tk.StringVar()
        harga_var = tk.StringVar()
        nama_entry = tk.Entry(form_frame, textvariable=nama_var)
        jenis_entry = tk.Entry(form_frame, textvariable=jenis_var)
        stok_entry = tk.Entry(form_frame, textvariable=stok_var)
        harga_entry = tk.Entry(form_frame, textvariable=harga_var)
        nama_entry.grid(row=1, column=0, padx=5, pady=5)
        jenis_entry.grid(row=1, column=1, padx=5, pady=5)
        stok_entry.grid(row=1, column=2, padx=5, pady=5)
        harga_entry.grid(row=1, column=3, padx=5, pady=5)
        def tambah_produk():
            try:
                db.tambah_produk(nama_var.get(), jenis_var.get(), int(stok_var.get()), float(harga_var.get()))
                nama_var.set(""); jenis_var.set(""); stok_var.set(""); harga_var.set("")
                refresh_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal menambah produk: {e}")
        tambah_btn = tk.Button(form_frame, text="Tambah", command=tambah_produk, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        tambah_btn.grid(row=1, column=4, padx=5, pady=5)
        # Tabel produk
        table_frame = tk.Frame(produk_frame, bg="#181f2a")
        table_frame.pack(fill="both", expand=True, pady=10)
        columns = ("id", "nama", "jenis", "stok", "harga")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        def refresh_table():
            for row in tree.get_children():
                tree.delete(row)
            for row in db.get_all_produk():
                tree.insert("", "end", values=row)
        refresh_table()
        # Edit & Hapus
        def on_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                nama_var.set(item[1])
                jenis_var.set(item[2])
                stok_var.set(item[3])
                harga_var.set(item[4])
                tambah_btn.config(text="Update", command=lambda: update_produk(item[0]))
        def update_produk(id):
            try:
                db.update_produk(id, nama_var.get(), jenis_var.get(), int(stok_var.get()), float(harga_var.get()))
                nama_var.set(""); jenis_var.set(""); stok_var.set(""); harga_var.set("")
                tambah_btn.config(text="Tambah", command=tambah_produk)
                refresh_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal update produk: {e}")
        def hapus_produk():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                if tk.messagebox.askyesno("Konfirmasi", f"Hapus produk '{item[1]}'?"):
                    db.hapus_produk(item[0])
                    refresh_table()
        tree.bind("<Double-1>", on_select)
        hapus_btn = tk.Button(produk_frame, text="Hapus Produk Terpilih", command=hapus_produk, bg="#ff4d4d", fg="#fff", font=("Segoe UI", 10, "bold"))
        hapus_btn.pack(anchor="e", pady=5)

    def show_supplier(self):
        self.clear_main_content()
        supplier_frame = tk.Frame(self.main_content, bg="#181f2a")
        supplier_frame.pack(fill="both", expand=True, padx=30, pady=20)
        title = tk.Label(supplier_frame, text="Manajemen Supplier", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#00e6ff")
        title.pack(anchor="w")
        form_frame = tk.Frame(supplier_frame, bg="#232b3e")
        form_frame.pack(fill="x", pady=10)
        tk.Label(form_frame, text="Nama", bg="#232b3e", fg="#fff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Kontak", bg="#232b3e", fg="#fff").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Alamat", bg="#232b3e", fg="#fff").grid(row=0, column=2, padx=5, pady=5)
        nama_var = tk.StringVar()
        kontak_var = tk.StringVar()
        alamat_var = tk.StringVar()
        nama_entry = tk.Entry(form_frame, textvariable=nama_var)
        kontak_entry = tk.Entry(form_frame, textvariable=kontak_var)
        alamat_entry = tk.Entry(form_frame, textvariable=alamat_var, width=30)
        nama_entry.grid(row=1, column=0, padx=5, pady=5)
        kontak_entry.grid(row=1, column=1, padx=5, pady=5)
        alamat_entry.grid(row=1, column=2, padx=5, pady=5)
        def tambah_supplier():
            try:
                db.tambah_supplier(nama_var.get(), kontak_var.get(), alamat_var.get())
                nama_var.set(""); kontak_var.set(""); alamat_var.set("")
                refresh_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal menambah supplier: {e}")
        tambah_btn = tk.Button(form_frame, text="Tambah", command=tambah_supplier, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        tambah_btn.grid(row=1, column=3, padx=5, pady=5)
        table_frame = tk.Frame(supplier_frame, bg="#181f2a")
        table_frame.pack(fill="both", expand=True, pady=10)
        columns = ("id", "nama", "kontak", "alamat")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        def refresh_table():
            for row in tree.get_children():
                tree.delete(row)
            for row in db.get_all_supplier():
                tree.insert("", "end", values=row)
        refresh_table()
        def on_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                nama_var.set(item[1])
                kontak_var.set(item[2])
                alamat_var.set(item[3])
                tambah_btn.config(text="Update", command=lambda: update_supplier(item[0]))
        def update_supplier(id):
            try:
                db.update_supplier(id, nama_var.get(), kontak_var.get(), alamat_var.get())
                nama_var.set(""); kontak_var.set(""); alamat_var.set("")
                tambah_btn.config(text="Tambah", command=tambah_supplier)
                refresh_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal update supplier: {e}")
        def hapus_supplier():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                if tk.messagebox.askyesno("Konfirmasi", f"Hapus supplier '{item[1]}'?"):
                    db.hapus_supplier(item[0])
                    refresh_table()
        tree.bind("<Double-1>", on_select)
        hapus_btn = tk.Button(supplier_frame, text="Hapus Supplier Terpilih", command=hapus_supplier, bg="#ff4d4d", fg="#fff", font=("Segoe UI", 10, "bold"))
        hapus_btn.pack(anchor="e", pady=5)

    def show_pelanggan(self):
        self.clear_main_content()
        pelanggan_frame = tk.Frame(self.main_content, bg="#181f2a")
        pelanggan_frame.pack(fill="both", expand=True, padx=30, pady=20)
        title = tk.Label(pelanggan_frame, text="Manajemen Pelanggan", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#00e6ff")
        title.pack(anchor="w")
        form_frame = tk.Frame(pelanggan_frame, bg="#232b3e")
        form_frame.pack(fill="x", pady=10)
        tk.Label(form_frame, text="Nama", bg="#232b3e", fg="#fff").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Kontak", bg="#232b3e", fg="#fff").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Alamat", bg="#232b3e", fg="#fff").grid(row=0, column=2, padx=5, pady=5)
        nama_var = tk.StringVar()
        kontak_var = tk.StringVar()
        alamat_var = tk.StringVar()
        nama_entry = tk.Entry(form_frame, textvariable=nama_var)
        kontak_entry = tk.Entry(form_frame, textvariable=kontak_var)
        alamat_entry = tk.Entry(form_frame, textvariable=alamat_var, width=30)
        nama_entry.grid(row=1, column=0, padx=5, pady=5)
        kontak_entry.grid(row=1, column=1, padx=5, pady=5)
        alamat_entry.grid(row=1, column=2, padx=5, pady=5)
        def tambah_pelanggan():
            try:
                db.tambah_pelanggan(nama_var.get(), kontak_var.get(), alamat_var.get())
                nama_var.set(""); kontak_var.set(""); alamat_var.set("")
                refresh_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal menambah pelanggan: {e}")
        tambah_btn = tk.Button(form_frame, text="Tambah", command=tambah_pelanggan, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        tambah_btn.grid(row=1, column=3, padx=5, pady=5)
        table_frame = tk.Frame(pelanggan_frame, bg="#181f2a")
        table_frame.pack(fill="both", expand=True, pady=10)
        columns = ("id", "nama", "kontak", "alamat")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        def refresh_table():
            for row in tree.get_children():
                tree.delete(row)
            for row in db.get_all_pelanggan():
                tree.insert("", "end", values=row)
        refresh_table()
        def on_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                nama_var.set(item[1])
                kontak_var.set(item[2])
                alamat_var.set(item[3])
                tambah_btn.config(text="Update", command=lambda: update_pelanggan(item[0]))
        def update_pelanggan(id):
            try:
                db.update_pelanggan(id, nama_var.get(), kontak_var.get(), alamat_var.get())
                nama_var.set(""); kontak_var.set(""); alamat_var.set("")
                tambah_btn.config(text="Tambah", command=tambah_pelanggan)
                refresh_table()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal update pelanggan: {e}")
        def hapus_pelanggan():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                if tk.messagebox.askyesno("Konfirmasi", f"Hapus pelanggan '{item[1]}'?"):
                    db.hapus_pelanggan(item[0])
                    refresh_table()
        tree.bind("<Double-1>", on_select)
        hapus_btn = tk.Button(pelanggan_frame, text="Hapus Pelanggan Terpilih", command=hapus_pelanggan, bg="#ff4d4d", fg="#fff", font=("Segoe UI", 10, "bold"))
        hapus_btn.pack(anchor="e", pady=5)

    def show_penjualan(self):
        self.clear_main_content()
        penjualan_frame = tk.Frame(self.main_content, bg="#181f2a")
        penjualan_frame.pack(fill="both", expand=True, padx=30, pady=20)
        title = tk.Label(penjualan_frame, text="Transaksi Penjualan", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#00e6ff")
        title.pack(anchor="w")
        # Pilih pelanggan
        pelanggan_list = db.get_all_pelanggan()
        pelanggan_dict = {f"{p[1]} ({p[2]})": p[0] for p in pelanggan_list}
        pelanggan_var = tk.StringVar()
        pelanggan_combo = ttk.Combobox(penjualan_frame, textvariable=pelanggan_var, values=list(pelanggan_dict.keys()), state="readonly")
        pelanggan_combo.set("Pilih Pelanggan")
        pelanggan_combo.pack(anchor="w", pady=5)
        # Pilih produk
        produk_list = db.get_all_produk()
        produk_dict = {f"{p[1]} ({p[2]}) - Stok:{p[3]} - Rp{p[4]:,.0f}": (p[0], p[4], p[3]) for p in produk_list}
        produk_var = tk.StringVar()
        produk_combo = ttk.Combobox(penjualan_frame, textvariable=produk_var, values=list(produk_dict.keys()), state="readonly")
        produk_combo.set("Pilih Produk")
        produk_combo.pack(anchor="w", pady=5)
        qty_var = tk.StringVar()
        qty_entry = tk.Entry(penjualan_frame, textvariable=qty_var, width=10)
        qty_entry.pack(anchor="w", pady=5)
        # Keranjang
        keranjang = []
        keranjang_frame = tk.Frame(penjualan_frame, bg="#232b3e")
        keranjang_frame.pack(fill="x", pady=10)
        keranjang_tree = ttk.Treeview(keranjang_frame, columns=("produk", "qty", "harga", "subtotal"), show="headings")
        for col in ("produk", "qty", "harga", "subtotal"):
            keranjang_tree.heading(col, text=col.capitalize())
            keranjang_tree.column(col, anchor="center")
        keranjang_tree.pack(fill="x")
        def refresh_keranjang():
            for row in keranjang_tree.get_children():
                keranjang_tree.delete(row)
            for item in keranjang:
                keranjang_tree.insert("", "end", values=(item['nama'], item['qty'], f"Rp{item['harga']:,.0f}", f"Rp{item['qty']*item['harga']:,.0f}"))
        def tambah_keranjang():
            if not produk_var.get() or produk_var.get() == "Pilih Produk":
                tk.messagebox.showwarning("Pilih Produk", "Silakan pilih produk!")
                return
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError
            except:
                tk.messagebox.showwarning("Qty Salah", "Qty harus angka > 0!")
                return
            id_produk, harga, stok = produk_dict[produk_var.get()]
            if qty > stok:
                tk.messagebox.showwarning("Stok Kurang", "Stok produk tidak cukup!")
                return
            for item in keranjang:
                if item['id_produk'] == id_produk:
                    item['qty'] += qty
                    refresh_keranjang()
                    return
            keranjang.append({
                'id_produk': id_produk,
                'nama': produk_var.get(),
                'qty': qty,
                'harga': harga
            })
            refresh_keranjang()
        tambah_btn = tk.Button(penjualan_frame, text="Tambah ke Keranjang", command=tambah_keranjang, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        tambah_btn.pack(anchor="w", pady=5)
        def simpan_penjualan():
            if not keranjang:
                tk.messagebox.showwarning("Keranjang Kosong", "Keranjang masih kosong!")
                return
            if not pelanggan_var.get() or pelanggan_var.get() == "Pilih Pelanggan":
                tk.messagebox.showwarning("Pilih Pelanggan", "Silakan pilih pelanggan!")
                return
            from datetime import datetime
            total = sum(item['qty']*item['harga'] for item in keranjang)
            try:
                db.tambah_penjualan(
                    tanggal=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    id_pelanggan=pelanggan_dict[pelanggan_var.get()],
                    total=total,
                    items=keranjang
                )
                tk.messagebox.showinfo("Sukses", "Transaksi penjualan berhasil disimpan!")
                keranjang.clear()
                refresh_keranjang()
                refresh_histori()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal simpan penjualan: {e}")
        simpan_btn = tk.Button(penjualan_frame, text="Simpan Transaksi Penjualan", command=simpan_penjualan, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        simpan_btn.pack(anchor="w", pady=5)
        # Histori penjualan
        histori_frame = tk.Frame(penjualan_frame, bg="#232b3e")
        histori_frame.pack(fill="both", expand=True, pady=10)
        histori_label = tk.Label(histori_frame, text="Histori Penjualan", font=("Segoe UI", 12, "bold"), bg="#232b3e", fg="#fff")
        histori_label.pack(anchor="w")
        histori_tree = ttk.Treeview(histori_frame, columns=("id", "tanggal", "pelanggan", "total"), show="headings")
        for col in ("id", "tanggal", "pelanggan", "total"):
            histori_tree.heading(col, text=col.capitalize())
            histori_tree.column(col, anchor="center")
        histori_tree.pack(fill="both", expand=True)
        def refresh_histori():
            for row in histori_tree.get_children():
                histori_tree.delete(row)
            for row in db.get_all_penjualan():
                id_pel = row[2]
                nama_pel = next((p[1] for p in pelanggan_list if p[0] == id_pel), "-")
                histori_tree.insert("", "end", values=(row[0], row[1], nama_pel, f"Rp{row[3]:,.0f}"))
        refresh_histori()

    def show_pembelian(self):
        self.clear_main_content()
        pembelian_frame = tk.Frame(self.main_content, bg="#181f2a")
        pembelian_frame.pack(fill="both", expand=True, padx=30, pady=20)
        title = tk.Label(pembelian_frame, text="Transaksi Pembelian", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#00e6ff")
        title.pack(anchor="w")
        # Pilih supplier
        supplier_list = db.get_all_supplier()
        supplier_dict = {f"{s[1]} ({s[2]})": s[0] for s in supplier_list}
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(pembelian_frame, textvariable=supplier_var, values=list(supplier_dict.keys()), state="readonly")
        supplier_combo.set("Pilih Supplier")
        supplier_combo.pack(anchor="w", pady=5)
        # Pilih produk
        produk_list = db.get_all_produk()
        produk_dict = {f"{p[1]} ({p[2]}) - Stok:{p[3]} - Rp{p[4]:,.0f}": (p[0], p[4]) for p in produk_list}
        produk_var = tk.StringVar()
        produk_combo = ttk.Combobox(pembelian_frame, textvariable=produk_var, values=list(produk_dict.keys()), state="readonly")
        produk_combo.set("Pilih Produk")
        produk_combo.pack(anchor="w", pady=5)
        qty_var = tk.StringVar()
        qty_entry = tk.Entry(pembelian_frame, textvariable=qty_var, width=10)
        qty_entry.pack(anchor="w", pady=5)
        # Keranjang
        keranjang = []
        keranjang_frame = tk.Frame(pembelian_frame, bg="#232b3e")
        keranjang_frame.pack(fill="x", pady=10)
        keranjang_tree = ttk.Treeview(keranjang_frame, columns=("produk", "qty", "harga", "subtotal"), show="headings")
        for col in ("produk", "qty", "harga", "subtotal"):
            keranjang_tree.heading(col, text=col.capitalize())
            keranjang_tree.column(col, anchor="center")
        keranjang_tree.pack(fill="x")
        def refresh_keranjang():
            for row in keranjang_tree.get_children():
                keranjang_tree.delete(row)
            for item in keranjang:
                keranjang_tree.insert("", "end", values=(item['nama'], item['qty'], f"Rp{item['harga']:,.0f}", f"Rp{item['qty']*item['harga']:,.0f}"))
        def tambah_keranjang():
            if not produk_var.get() or produk_var.get() == "Pilih Produk":
                tk.messagebox.showwarning("Pilih Produk", "Silakan pilih produk!")
                return
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError
            except:
                tk.messagebox.showwarning("Qty Salah", "Qty harus angka > 0!")
                return
            id_produk, harga = produk_dict[produk_var.get()]
            for item in keranjang:
                if item['id_produk'] == id_produk:
                    item['qty'] += qty
                    refresh_keranjang()
                    return
            keranjang.append({
                'id_produk': id_produk,
                'nama': produk_var.get(),
                'qty': qty,
                'harga': harga
            })
            refresh_keranjang()
        tambah_btn = tk.Button(pembelian_frame, text="Tambah ke Keranjang", command=tambah_keranjang, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        tambah_btn.pack(anchor="w", pady=5)
        def simpan_pembelian():
            if not keranjang:
                tk.messagebox.showwarning("Keranjang Kosong", "Keranjang masih kosong!")
                return
            if not supplier_var.get() or supplier_var.get() == "Pilih Supplier":
                tk.messagebox.showwarning("Pilih Supplier", "Silakan pilih supplier!")
                return
            from datetime import datetime
            total = sum(item['qty']*item['harga'] for item in keranjang)
            try:
                db.tambah_pembelian(
                    tanggal=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    id_supplier=supplier_dict[supplier_var.get()],
                    total=total,
                    items=keranjang
                )
                tk.messagebox.showinfo("Sukses", "Transaksi pembelian berhasil disimpan!")
                keranjang.clear()
                refresh_keranjang()
                refresh_histori()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Gagal simpan pembelian: {e}")
        simpan_btn = tk.Button(pembelian_frame, text="Simpan Transaksi Pembelian", command=simpan_pembelian, bg="#00e6ff", fg="#232b3e", font=("Segoe UI", 10, "bold"))
        simpan_btn.pack(anchor="w", pady=5)
        # Histori pembelian
        histori_frame = tk.Frame(pembelian_frame, bg="#232b3e")
        histori_frame.pack(fill="both", expand=True, pady=10)
        histori_label = tk.Label(histori_frame, text="Histori Pembelian", font=("Segoe UI", 12, "bold"), bg="#232b3e", fg="#fff")
        histori_label.pack(anchor="w")
        histori_tree = ttk.Treeview(histori_frame, columns=("id", "tanggal", "supplier", "total"), show="headings")
        for col in ("id", "tanggal", "supplier", "total"):
            histori_tree.heading(col, text=col.capitalize())
            histori_tree.column(col, anchor="center")
        histori_tree.pack(fill="both", expand=True)
        def refresh_histori():
            for row in histori_tree.get_children():
                histori_tree.delete(row)
            for row in db.get_all_pembelian():
                id_sup = row[2]
                nama_sup = next((s[1] for s in supplier_list if s[0] == id_sup), "-")
                histori_tree.insert("", "end", values=(row[0], row[1], nama_sup, f"Rp{row[3]:,.0f}"))
        refresh_histori()

    def show_laporan(self):
        self.clear_main_content()
        laporan_frame = tk.Frame(self.main_content, bg="#181f2a")
        laporan_frame.pack(fill="both", expand=True, padx=30, pady=20)
        title = tk.Label(laporan_frame, text="Laporan & Rekapitulasi", font=("Segoe UI", 16, "bold"), bg="#181f2a", fg="#00e6ff")
        title.pack(anchor="w")
        # Laporan Penjualan
        penjualan = db.get_all_penjualan()
        total_penjualan = sum(row[3] for row in penjualan)
        penjualan_label = tk.Label(laporan_frame, text=f"Total Penjualan: Rp{total_penjualan:,.0f}", font=("Segoe UI", 12, "bold"), bg="#181f2a", fg="#fff")
        penjualan_label.pack(anchor="w", pady=(10,0))
        penjualan_tree = ttk.Treeview(laporan_frame, columns=("id", "tanggal", "pelanggan", "total"), show="headings", height=5)
        for col in ("id", "tanggal", "pelanggan", "total"):
            penjualan_tree.heading(col, text=col.capitalize())
            penjualan_tree.column(col, anchor="center")
        penjualan_tree.pack(fill="x", pady=5)
        pelanggan_list = db.get_all_pelanggan()
        for row in penjualan:
            id_pel = row[2]
            nama_pel = next((p[1] for p in pelanggan_list if p[0] == id_pel), "-")
            penjualan_tree.insert("", "end", values=(row[0], row[1], nama_pel, f"Rp{row[3]:,.0f}"))
        # Laporan Pembelian
        pembelian = db.get_all_pembelian()
        total_pembelian = sum(row[3] for row in pembelian)
        pembelian_label = tk.Label(laporan_frame, text=f"Total Pembelian: Rp{total_pembelian:,.0f}", font=("Segoe UI", 12, "bold"), bg="#181f2a", fg="#fff")
        pembelian_label.pack(anchor="w", pady=(20,0))
        pembelian_tree = ttk.Treeview(laporan_frame, columns=("id", "tanggal", "supplier", "total"), show="headings", height=5)
        for col in ("id", "tanggal", "supplier", "total"):
            pembelian_tree.heading(col, text=col.capitalize())
            pembelian_tree.column(col, anchor="center")
        pembelian_tree.pack(fill="x", pady=5)
        supplier_list = db.get_all_supplier()
        for row in pembelian:
            id_sup = row[2]
            nama_sup = next((s[1] for s in supplier_list if s[0] == id_sup), "-")
            pembelian_tree.insert("", "end", values=(row[0], row[1], nama_sup, f"Rp{row[3]:,.0f}"))
        # Laporan Stok Produk
        produk = db.get_all_produk()
        stok_label = tk.Label(laporan_frame, text="Stok Produk", font=("Segoe UI", 12, "bold"), bg="#181f2a", fg="#fff")
        stok_label.pack(anchor="w", pady=(20,0))
        produk_tree = ttk.Treeview(laporan_frame, columns=("id", "nama", "jenis", "stok", "harga"), show="headings", height=5)
        for col in ("id", "nama", "jenis", "stok", "harga"):
            produk_tree.heading(col, text=col.capitalize())
            produk_tree.column(col, anchor="center")
        produk_tree.pack(fill="x", pady=5)
        for row in produk:
            produk_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], f"Rp{row[4]:,.0f}"))
        # Laba/Rugi
        laba = total_penjualan - total_pembelian
        laba_label = tk.Label(laporan_frame, text=f"Laba/Rugi: Rp{laba:,.0f}", font=("Segoe UI", 14, "bold"), bg="#181f2a", fg="#00e6ff")
        laba_label.pack(anchor="w", pady=(20,0))

if __name__ == "__main__":
    app = MusicStoreApp()
    app.mainloop() 