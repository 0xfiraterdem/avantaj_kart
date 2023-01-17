import datetime
import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkcalendar import DateEntry
import locale

locale.setlocale(locale.LC_ALL, '')


def ekle_musteri(e_musteri):
    customers = list(map(lambda n: n.upper(), musteri_adi()))
    musteri = e_musteri.get()
    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    if musteri == "":
        MessageBox.showinfo("uyarı", "Müşteri boş bırakılamaz!!!")
        return

    if musteri.upper() in customers:
        MessageBox.showinfo("uyarı", "Müşteri sistemde bulunmaktadır")
        e_musteri.delete(0, 'end')
        return

    if musteri.upper() not in customers and musteri != "":
        cursor.execute("insert into `musteriler` values (NULL,'" + musteri + "')")
        cursor.execute("commit")
        MessageBox.showinfo("Ekleme Durumu", "Ekleme Başarılı")
    e_musteri.delete(0, 'end')
    return musteri_adi()


def sil_musteri(musteri, musteri1):
    if musteri.get() == "":
        MessageBox.showinfo("Uyarı", " Silmek istediğiniz müşteriyi seçin!!!")
    else:
        con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute("delete from musteriler where Ad='" + musteri.get() + "'")
        cursor.execute("commit")

        MessageBox.showinfo("Silme Durumu", "Silme Başarılı...")

        musteri1.set("")
        musteri.set("")
        con.close()
        return musteri_adi()


def guncelle_musteri(e_musteri, musteri, musteri1):
    eski_musteri = musteri.get()
    yeni_musteri = e_musteri.get()
    print(eski_musteri, yeni_musteri)

    if eski_musteri == "":
        MessageBox.showinfo("Uyarı", "Güncellemek istediğiniz müşteriyi seçiniz!!!")
        return

    if yeni_musteri == "":
        MessageBox.showinfo("Uyarı", "Müşteri adı boş olamaz!!!")
        return

    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("update musteriler set Ad ='" + yeni_musteri + "' where Ad ='" + eski_musteri + "' ")
    cursor.execute("commit")
    musteri.set("")
    musteri1.set("")
    e_musteri.delete(0, 'end')
    MessageBox.showinfo("Uyarı", "Güncelleme başarılı!!!")
    return musteri_adi()


def ekle_kart(e_musteri, e_aylk, e_gnlk, e_plaka, e_kart_no):
    if e_musteri.get() == "":
        MessageBox.showinfo("Uyarı", "Önce kart eklemek istediğiniz müşteriyi seçiniz!!!")
        return

    if e_aylk.get() == "" or e_gnlk.get() == "" or e_plaka.get() == "" or e_kart_no == "":
        MessageBox.showinfo("Uyarı", "Tüm kutuları doldurunuz!!!")
        return

    if not e_aylk.get().isnumeric():
        MessageBox.showinfo("Uyarı", "Aylık İndirim Hakkı Sayı Olmalıdır!!!")
        return

    if not e_gnlk.get().isnumeric():
        MessageBox.showinfo("Uyarı", "Günlük İndirim Hakkı Sayı Olmalıdır!!!")
        return
    if len(e_kart_no.get()) != 19:
        MessageBox.showinfo("Uyarı", "Kart Numarası 16 Haneli Olmalıdır!!!")
        return

    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                            auth_plugin='mysql_native_password')
    cursor = con.cursor()

    cursor.execute("select `Kart_No` from kartlar")
    data = cursor.fetchall()

    for i in data:
        if i[0] == e_kart_no:
            MessageBox.showinfo("Uyarı", "Kart sistemde mevcut!!!")
            return

    cursor.execute("select `ID` from musteriler where Ad = '" + e_musteri.get() + "'")
    musteri_no = cursor.fetchall()[0][0]

    cursor.execute("insert into kartlar values (NULL,'" + e_kart_no.get() + "','" + e_gnlk.get() + "','" + e_aylk.get() + "','" + e_plaka.get().upper() + "','" + str(musteri_no) + e_musteri.get() + "')")
    cursor.execute("commit")

    e_kart_no.delete(0, 'end')
    e_aylk.delete(0, 'end')
    e_gnlk.delete(0, 'end')
    e_plaka.delete(0, 'end')

    MessageBox.showinfo("Ekleme Durumu", "Ekleme Başarılı...")
    con.close()


def sil_kart(box):
    select = box.curselection()
    if select == () or select[0] == 0:
        MessageBox.showinfo("Uyarı", "Önce bir kart seçiniz!!!")
        return

    kart_no = box.get(select[0], select[0])[0].split()[0]

    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("delete from kartlar where Kart_No='" + kart_no + "'")
    cursor.execute("commit")

    MessageBox.showinfo("Silme Durumu", "Silme Başarılı...")
    box.delete(select[0], select[0])

    con.close()


def guncelle_kart(e_aylk, e_gnlk, e_plaka, e_kart_no):
    kart_no = []
    if e_aylk.get() == "" or e_gnlk.get() == "" or e_plaka.get() == "" or e_kart_no == "":
        MessageBox.showinfo("Uyarı", "Tüm kutuları doldurunuz!!!")
        return
    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("select Kart_No from kartlar")
    data = cursor.fetchall()

    for i in data:
        kart_no.append(i[0])

    if e_kart_no.get() not in kart_no:
        MessageBox.showinfo("Uyarı", "Kart sistemde mevcut değil!!!")
        con.close()
        return

    cursor.execute(
        "update kartlar set `Aylik_limit(Lt)` ='" + e_aylk.get() + "',`Gunluk_limit(Lt)` ='" + e_gnlk.get() + "',Plaka='" + e_plaka.get() + "' where Kart_No='" + e_kart_no.get() + "'")
    cursor.execute("commit")

    MessageBox.showinfo("Güncelleme Durumu", "Güncelleme Başarılı...")
    e_aylk.delete(0, 'end')
    e_gnlk.delete(0, 'end')
    e_plaka.delete(0, 'end')
    e_kart_no.delete(0, 'end')

    con.close()


def listele(box, musteri):
    box.delete(1, END)
    bilgi = []
    if musteri.get() == "":
        MessageBox.showinfo("Uyarı", "Önce musteri seçiniz!!!")
        return

    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("select `ID` from musteriler where Ad = '" + musteri.get() + "'")
    data = cursor.fetchall()

    cursor.execute("select Kart_No,`Gunluk_limit(Lt)`,`Aylik_limit(Lt)`,Plaka from kartlar where musteri_id = '" + str(
        data[0][0]) + "'")
    data = cursor.fetchall()
    for i in data:
        for j in i:
            bilgi.append(f"{j:>15}")
        box.insert(END, bilgi[0] + bilgi[1] + bilgi[2] + bilgi[3])
        bilgi.clear()


def goster_kart(box, e_aylik, e_gunluk, e_plaka, e_kart_no):
    e_kart_no.delete(0, END)
    e_gunluk.delete(0, END)
    e_aylik.delete(0, END)
    e_plaka.delete(0, END)
    select = box.curselection()
    if select == () or select[0] == 0:
        MessageBox.showinfo("Uyart", "Önce bir kart seçiniz!!!")
        return
    secim = box.get(select[0], select[0])[0].split()
    print(secim)

    e_kart_no.insert(0, secim[0])
    e_gunluk.insert(0, secim[1])
    e_aylik.insert(0, secim[2])
    e_plaka.insert(0, secim[3])

    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("select * from kartlar where Kart_No='" + secim[0] + "'")
    con.close()


def musteri_adi():
    con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("select `Ad` from musteriler")
    data = cursor.fetchall()
    customers = []
    for i in data:
        for j in i:
            customers.append(j)
    return customers


def kart_sayfa(kartlar):
    frame = Frame(kartlar, bd=5)
    frame.pack(padx=10, pady=10)

    label1 = LabelFrame(frame, text="Müşteri Bilgisi")
    label1.grid(row=0, column=0, padx=10, pady=10, sticky="NEWS")

    e_musteri = Entry(label1)
    e_musteri.grid(row=1, column=1, padx=10, pady=5)
    musteri = ttk.Combobox(label1, values=musteri_adi(), state="readonly")
    musteri.grid(row=1, column=0, padx=10, pady=5)

    Button(label1, text="Ekle",
           command=lambda: [musteri.config(values=ekle_musteri(e_musteri)), musteri1.config(values=musteri_adi()),
                            musteri], bd=2).grid(row=1, column=2, ipadx=7, pady=5)
    Button(label1, text="Sil", command=lambda: [musteri.config(values=sil_musteri(musteri, musteri1)),
                                                musteri1.config(values=musteri_adi())], bd=2).grid(row=1, column=3,
                                                                                                   ipadx=7, pady=5)
    Button(label1, text="Güncelle",
           command=lambda: [musteri.config(values=guncelle_musteri(e_musteri, musteri, musteri1)),
                            musteri1.config(values=musteri_adi())], bd=2).grid(row=1, column=4, ipadx=6, pady=5)

    label2 = LabelFrame(frame, text="Kart Bilgisi")
    label2.grid(row=1, column=0, padx=10, pady=10, sticky="NEWS")

    Label(label2, text="Aylık Limit(Lt):").grid(row=0, column=0, padx=10, pady=5)
    Label(label2, text="Günlük Limit(Lt):").grid(row=0, column=1, padx=10, pady=5)
    Label(label2, text="Plaka:").grid(row=0, column=2, padx=10, pady=5)
    Label(label2, text="Kart Numarası:").grid(row=2, column=0, padx=10, pady=0)

    def show_format(event):
        kart_no = '1' + event.widget.get()
        if len(kart_no) < 20:
            if len(kart_no) % 5 == 0:
                if event.keycode != 8:
                    kart_no += '-'
                else:
                    kart_no = kart_no[:len(kart_no) - 1]
            event.widget.delete(0, END)
        else:
            kart_no = kart_no[:20]
            event.widget.delete(0, END)
        event.widget.insert(0, kart_no[1:])
        return event.widget.get()

    e_aylk = Entry(label2)
    e_aylk.grid(row=1, column=0, padx=10, pady=10, ipadx=7)

    e_gnlk = Entry(label2)
    e_gnlk.grid(row=1, column=1, padx=10, pady=5, ipadx=7)

    e_plaka = Entry(label2)
    e_plaka.grid(row=1, column=2, padx=10, pady=5, ipadx=7)

    e_kart_no = Entry(label2)
    e_kart_no.grid(row=3, column=0, padx=10, pady=0, ipadx=7)
    e_kart_no.bind("<KeyRelease>", show_format)
    e_kart_no.bind("<Return>", show_format)

    label3 = LabelFrame(label2)
    label3.grid(row=3, column=2, padx=5, pady=10, sticky=E)
    Button(label3, text="Ekle",
           command=lambda: ekle_kart(musteri, e_aylk, e_gnlk, e_plaka, e_kart_no)).grid(row=2, column=1)
    Button(label3, text="Güncelle",
           command=lambda: guncelle_kart(e_aylk, e_gnlk, e_plaka, e_kart_no)).grid(row=2, column=2)

    label4 = LabelFrame(frame, text="Müşteri Kart Bilgisi")
    label4.grid(row=4, column=0, padx=10, pady=10, sticky="news")

    list_box = Frame(label4, bd=10)
    list_box.grid(row=0, column=1)

    box = Listbox(list_box, width=45, font=("bold", 9))
    scroll1 = Scrollbar(list_box, command=box.yview)
    scroll1.pack(side=LEFT, fill=Y)
    scroll2 = Scrollbar(list_box, command=box.xview, orient="horizontal")
    scroll2.pack(side=BOTTOM, fill=X)
    box.pack(side=LEFT, fill=BOTH)

    box.config(yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
    box.insert(END, "Kart_No                                G. Limit    A. Limit       Plaka")

    musteri1 = ttk.Combobox(list_box, values=musteri_adi(), state="readonly", width=15)
    musteri1.pack(anchor=N, padx=5, pady=5)
    Button(list_box, text="Listele", command=lambda: listele(box, musteri1)).pack(fill=X, padx=5, pady=5)
    Button(list_box, text="Göster",
           command=lambda: goster_kart(box, e_aylk, e_gnlk, e_plaka, e_kart_no)).pack(fill=X,padx=5,pady=5)
    Button(list_box, text="Sil", command=lambda: sil_kart(box)).pack(fill=X, padx=5, pady=5)


def kampanya_sil(kampanya):
    if kampanya.get() == "":
        MessageBox.showinfo("Uyarı", " Silmek istediğiniz müşteriyi seçin!!!")
    else:
        con = mysql.connect(host="localhost", user="root", password="13542612", database="kampanya",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute("delete from kampanyalar where Ad='" + kampanya.get().upper() + "'")
        cursor.execute("commit")

        MessageBox.showinfo("Silme Durumu", "Silme Başarılı...")

        kampanya.set("")
        con.close()
        return musteri_adi()


def gecerli_musteri_ekle(box, musteri, musteriler):
    if musteri.get() == "":
        MessageBox.showinfo("Uyarı", " Müşteri boş bırakılamaz!!!")
        return

    if musteri.get() in musteriler:
        MessageBox.showinfo("Uyarı", " Müşteri mevcut!!!")
        return

    box.insert(END, musteri.get())
    musteriler.append(musteri.get())
    musteri.set("")


def gecerli_musteri_sil(box, musteriler):
    select = box.curselection()
    if select == () or select[0] == 0:
        MessageBox.showinfo("Uyarı", "Önce bir müşteri seçiniz!!!")
        return
    musteriler.remove(box.get(select))
    box.delete(select)


def gecerli_istasyon_ekle(box1, istasyon, istasyonlar):
    if "" == istasyon.get():
        MessageBox.showinfo("Uyarı", "Tüm alanları doldurunuz!!!")
        return

    if istasyon.get() in istasyonlar:
        MessageBox.showinfo("Uyarı", "İstasyon Mevcut")
        return

    box1.insert(END, istasyon.get())
    istasyonlar.append(istasyon.get())

    istasyon.set("")


def gecerli_istasyon_sil(box, istasyon):
    select = list(box.curselection())
    if select == () or select[0] == 0:
        MessageBox.showinfo("Uyarı", "Önce bir müşteri seçiniz!!!")
        return
    istasyon.remove(box.get(select))
    box.delete(select)


def check_btn(indirim_btn, kontrol):
    if kontrol.get():
        indirim_btn.configure(state='normal')
    else:
        indirim_btn.configure(state='disabled')


def istasyon_grubu():
    con = mysql.connect(host="localhost", user="root", password="13542612", database="istasyonlar",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("select `Ad` from istasyon_grubu")
    data = cursor.fetchall()
    istasyon_grubu_list = []
    for i in data:
        for j in i:
            istasyon_grubu_list.append(j)
    return istasyon_grubu_list


def kampanya_adi():
    con = mysql.connect(host="localhost", user="root", password="13542612", database="kampanya",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("select `Ad` from kampanyalar")
    data = cursor.fetchall()
    kampanya = []
    for i in data:
        for j in i:
            kampanya.append(j)
    return kampanya


def uygula(e_ad, e_basla, e_bitis, musteriler, box, box1, istasyonlar, kontrol1, kontrol2, indirim):
    ad = e_ad.get()
    basla = e_basla.get()
    bitis = e_bitis.get()
    indirimli_urun = []

    for i in range(0, len(kontrol1)):
        if kontrol1[i].get():
            if indirim[i].get() != "":
                indirimli_urun.append(kontrol2[i])
                indirimli_urun.append(indirim[i].get())
            else:
                MessageBox.showinfo("Uyarı", "Tüm alanları doldurunuz!!!")
                return

    print(e_ad.get(), e_basla.get(), e_bitis.get(), musteriler, istasyonlar, indirimli_urun)

    if "" in (e_ad.get(), e_basla.get(), e_bitis.get()) or len(musteriler) == 0 or len(istasyonlar) == 0 or len(
            indirimli_urun) == 0 or len(indirimli_urun) % 2 != 0:
        MessageBox.showinfo("Uyarı", "Tüm alanları doldurunuz!!!")
        return

    if ad in kampanya_adi():
        MessageBox.showinfo("Ekleme Durumu", "Kampanya Adı Mevcut...")
        return

    for i in range(0, len(indirimli_urun), 2):
        if not indirimli_urun[i + 1].isnumeric():
            MessageBox.showinfo("Uyarı", "İndirim oranı sayı olmalıdır!!!")
            return

    con = mysql.connect(host="localhost", user="root", password="13542612", database="kampanya",
                        auth_plugin='mysql_native_password')
    cursor = con.cursor()
    cursor.execute("insert into kampanyalar values (NULL,'" + ad.upper() + "','" + basla + "','" + bitis + "')")
    cursor.execute("select `ID` from kampanyalar")
    kmpn_id = list(cursor.fetchall()[-1])[0]
    for i in range(0, len(musteriler)):
        cursor.execute(
            "insert into gecerli_musteri values ('" + (str(kmpn_id) + ad).upper() + "','" + musteriler[
                i].upper() + "')")
    print(istasyonlar)
    for i in istasyonlar:
        cursor.execute(
            "insert into gecerli_istasyon values ('" + (str(kmpn_id) + ad).upper() + "','" + i.upper() + "')")
    for i in range(0, len(indirimli_urun), 2):
        print(i)
        cursor.execute(
            "insert into urun_indirim values ('" + (str(kmpn_id) + ad).upper() + "','" + indirimli_urun[
                i].upper() + "','" +
            indirimli_urun[i + 1] + "')")

    cursor.execute("commit")
    MessageBox.showinfo("Ekleme Durumu", "Ekleme Başarılı...")
    e_ad.delete(0, 'end')
    e_basla.delete(0, 'end')
    e_bitis.delete(0, 'end')
    box.delete(0, 'end')
    box1.delete(0, 'end')
    for orn in indirim:
        if orn.get() != "":
            indx = indirim.index(orn)
            kontrol1[indx].set(False)
            orn.delete(0, 'end')
            check_btn(orn, kontrol1[indx])

    musteriler.clear()
    istasyonlar.clear()


def kampanya_sayfa(kampanyalar):
    frame = Frame(kampanyalar)
    frame.pack(padx=10, pady=10, fill=BOTH)

    an = datetime.datetime.now()

    kampanya = LabelFrame(frame, text="Kampanya Bilgisi", height=100)
    kampanya.grid(row=0, column=0, padx=20, pady=5, sticky="NEWS")

    Label(kampanya, text="Kampanya Adı").grid(row=0, column=0, padx=10, sticky=W)
    Label(kampanya, text="Başlangıç Tarihi").grid(row=2, column=0, padx=10, sticky=W)
    Label(kampanya, text="Biriş Tarihi").grid(row=2, column=1, padx=10, sticky=W)

    e_ad = Entry(kampanya)
    e_ad.grid(row=1, column=0, padx=15, pady=0)

    kampanya_ad = ttk.Combobox(kampanya, values=kampanya_adi(), state="readonly")
    kampanya_ad.grid(row=1, column=1, padx=8, pady=5)

    e_basla = DateEntry(kampanya, width=12, day=an.day, month=an.month, year=an.year, locale='tr_TR',
                        background='darkblue', foreground='white', borderwidth=2)
    e_basla._set_text(e_basla.date.strftime('%d.%m.%Y'))
    e_basla.grid(row=3, column=0, padx=13, pady=3, sticky=W)

    e_bitis = DateEntry(kampanya, width=12, day=an.day, month=an.month, year=an.year, locale='tr_TR',
                        background='darkblue', foreground='white', borderwidth=2)
    e_bitis._set_text(e_bitis.date.strftime('%d.%m.%Y'))
    e_bitis.grid(row=3, column=1, padx=10, pady=0, sticky=W)

    Button(kampanya, text="Ekle", command=lambda: [
        uygula(e_ad, e_basla, e_bitis, musteriler, box, box1, istasyonlar, kontrol1, kontrol2, indirim_orani),
        kampanya_ad.config(values=kampanya_adi())]).grid(row=1, column=4, ipadx=10,pady=0)
    Button(kampanya, text="Sil", command=lambda: [kampanya_sil(kampanya_ad), kampanya_ad.config(values=kampanya_adi())],
           bd=2).grid(row=1, column=5, ipadx=10,pady=0)
    Button(kampanya, text="Yenile", command=lambda: musteri.config(values=musteri_adi()),
           bd=2).grid(row=1, column=6, ipadx=9, pady=0)

    gecerli_musteri = LabelFrame(frame, text="Geçerli Müşteriler")
    gecerli_musteri.grid(row=2, column=0, padx=20, pady=8, sticky="NEWS")

    list_box = Label(gecerli_musteri, bd=10)
    list_box.grid(row=0, column=0)

    box = Listbox(list_box, height=8)
    box.pack(side=LEFT, fill=Y)
    scroll = Scrollbar(list_box, command=box.yview)
    scroll.pack(side=RIGHT, fill=Y)
    box.config(yscrollcommand=scroll.set)
    box.insert(END, "Müşteriler")

    musteriler = []
    musteri = ttk.Combobox(list_box, values=musteri_adi(), state="readonly", width=18)
    musteri.pack(anchor=N, ipady=1, padx=5)
    Button(list_box, text="Ekle", command=lambda: gecerli_musteri_ekle(box, musteri, musteriler)).pack(pady=5, fill=X,
                                                                                                       padx=5)
    Button(list_box, text="Sil", command=lambda: gecerli_musteri_sil(box, musteriler)).pack(pady=5, fill=X, padx=5)

    gecerli_istasyon = LabelFrame(frame, text="Geçerli İstasyonlar ve Ürün İndirim Oranları")
    gecerli_istasyon.grid(row=1, column=0, padx=20, pady=10, sticky="news")

    list_box1 = Frame(gecerli_istasyon, bd=10)
    list_box1.grid(row=0, column=0)

    box1 = Listbox(list_box1, width=17, height=8, font=("bold", 9))
    box1.pack(side=LEFT, fill=Y)
    scroll1 = Scrollbar(list_box1, command=box.yview)
    scroll1.pack(side=RIGHT, fill=Y)
    box1.config(yscrollcommand=scroll1.set)
    box1.insert(END, "İstasyon Grupları")

    istasyonlar = []
    istasyon = ttk.Combobox(list_box1, values=istasyon_grubu(), state="readonly", width=18)
    istasyon.pack(anchor=N, padx=5, pady=5)

    Button(list_box1, text="Ekle",
           command=lambda: gecerli_istasyon_ekle(box1, istasyon, istasyonlar)).pack(
        fill=X, padx=5, pady=5)
    Button(list_box1, text="Sil", command=lambda: gecerli_istasyon_sil(box1, istasyonlar)).pack(pady=5, fill=X, padx=5)

    urunler = LabelFrame(gecerli_istasyon)
    urunler.grid(row=0, column=1, padx=5, pady=10, sticky="N")

    kontrol1 = [BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()]
    kontrol2 = ["Benzin", "Motorin", "Dizel", "LPG"]

    Label(urunler, text="İndirim:").grid(row=1, column=1, sticky=W)
    indirim_btn1 = Entry(urunler)
    indirim_btn1.configure(width=4, state='disabled')
    indirim_btn1.grid(row=1, column=2, sticky='W', padx=5)

    Label(urunler, text="İndirim:").grid(row=2, column=1, sticky=W)
    indirim_btn2 = Entry(urunler)
    indirim_btn2.configure(width=4, state='disabled')
    indirim_btn2.grid(row=2, column=2, sticky='W', padx=5)

    Label(urunler, text="İndirim:").grid(row=3, column=1, sticky=W)
    indirim_btn3 = Entry(urunler)
    indirim_btn3.configure(width=4, state='disabled')
    indirim_btn3.grid(row=3, column=2, sticky='W', padx=5)

    Label(urunler, text="İndirim:").grid(row=4, column=1, sticky=W)
    indirim_btn4 = Entry(urunler)
    indirim_btn4.configure(width=4, state='disabled')
    indirim_btn4.grid(row=4, column=2, sticky='W', padx=5)

    indirim_orani = [indirim_btn1, indirim_btn2, indirim_btn3, indirim_btn4]

    Checkbutton(urunler, text=kontrol2[0], variable=kontrol1[0], offvalue=False, onvalue=True,
                command=lambda: check_btn(indirim_orani[0], kontrol1[0])).grid(row=1, column=0, sticky=W)
    Checkbutton(urunler, text=kontrol2[1], variable=kontrol1[1], offvalue=False, onvalue=True,
                command=lambda: check_btn(indirim_orani[1], kontrol1[1])).grid(row=2, column=0, sticky=W)
    Checkbutton(urunler, text=kontrol2[2], variable=kontrol1[2], offvalue=False, onvalue=True,
                command=lambda: check_btn(indirim_orani[2], kontrol1[2])).grid(row=3, column=0, sticky=W)
    Checkbutton(urunler, text=kontrol2[3], variable=kontrol1[3], offvalue=False, onvalue=True,
                command=lambda: check_btn(indirim_orani[3], kontrol1[3])).grid(row=4, column=0, sticky=W)


def main():
    root = Tk()
    root.title("Avantaj Kart")
    root.geometry()
    nb = ttk.Notebook(root)
    ttk.Style().configure('TNotebook', font=('bold', 10), backgraund="black")

    kartlar = Frame(nb)
    kartlar.configure(bg='#363636')

    kampanyalar = Frame(nb)
    kampanyalar.configure(bg='#363636')

    nb.add(kartlar, text="Müşteri")
    nb.add(kampanyalar, text="Kampanya")

    nb.pack(pady=7, fill=BOTH, expand=True)

    kampanya_sayfa(kampanyalar)
    kart_sayfa(kartlar)
    root.mainloop()

main()
