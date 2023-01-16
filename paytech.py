import binascii
import time
import locale
from datetime import datetime
import mysql.connector as mysql
import crcmod.crcmod
from communication import *

locale.setlocale(locale.LC_ALL, '')
date = datetime.now()
istayon = "ISTANBUL"

STX = "FD"
ETX = "FE"
DIR = "80"

_CRC_FUNC = crcmod.predefined.mkCrcFun('crc-16')


class Paytech:

    def __init__(self, Communication, Address):
        self.Address = Address
        self.Communication = Communication
        self.Communication.connect()

    def CRC16(self, data):
        crc = hex(_CRC_FUNC(bytes.fromhex(data)))[2:]
        crc = '{0:04x}'.format(int(crc, 16))
        crc = crc[2:] + crc[:2]
        return crc

    def poll(self):

        packet = self.Address + DIR + "0800"
        CRC = self.CRC16(packet)
        string = (STX + packet + CRC + ETX).upper()
        packet = bytes.fromhex(string)

        self.Communication.send(packet)
        self.Communication.listen()

    def parser_key_data(self):
        data = self.Communication.last_data
        data_lenght = data[8:10]
        data_lenght = int(data_lenght, 16)
        data = data[10:10 + 2 * data_lenght]
        if data == '1c':
            data = 'Benzin'
        elif data == '1d':
            data = 'Dizel'
        elif data == 'f3':
            data = 'Motorin'
        elif data == 'f4':
            data = 'LPG'
        elif data == '0d':
            data = 'ONAY'
        elif data == '08':
            data = 'sil'
        elif data in ('2b', '2d', '2a', '2f', '25', '3d', '26', '22', '31', '40', '23'):
            data = '1'
        else:
            data = bytes.fromhex(data).decode("cp1254")
        return data

    def Clear_Screen(self):
        self.Communication.send(bytes.fromhex("FD 3A 80 21 04 01 01 03 20 A4 C6 FE"))

    def ClearPressKey(self):
        self.Communication.send(bytes.fromhex("FD 3A 80 06 00 0E 90 FE "))

    def Keyboard_enable(self):
        self.Communication.send(bytes.fromhex("FD 3A 80 26 02 04 01 6D 0C FE "))

    def show_message(self, image, delay, BXP, BYP, text, box, TYP, TXP):
        try:
            OPCODE = "21"
            if box:
                style = f"BBX={delay}&BNAME={image}.bmp &BXP={BXP}&BYP={BYP}"
                style = "{" + style + "}"
            else:
                style = f"BNAME={image}.bmp &TXP={TXP} &TYP={TYP}"
                style = "{" + style + "}"
            asda = style.encode() + text.encode()
            x = binascii.hexlify(asda)
            y = str(x, 'cp1254')
            data = "010107" + y
            length = '{0:02x}'.format(round(len(data) / 2))

            packet = self.Address + DIR + OPCODE + length + data
            CRC = self.CRC16(packet)

            string = (STX + packet + CRC + ETX).upper()
            packet = bytes.fromhex(string)

            self.Communication.send(packet)
            self.Communication.listen()
        except:
            pass

    def print_onscreen(self, text):
        self.poll()
        self.show_message("", 0, 1, 1, box=False, text=text, TXP=20, TYP=40)

    def choice(self):
        while True:
            self.poll()
            secim = self.parser_key_data()
            if secim in ("Benzin", "Motorin", "LPG", "Dizel"):
                return secim
            self.ClearPressKey()

    def kart_id(self, secim):
        kart_id = ""
        text = f"Urun: {secim:<33} Kart ID:{kart_id}"
        self.print_onscreen(text)
        while True:
            self.poll()
            self.ClearPressKey()
            if self.Communication.last_data[6:8] == "04":
                continue
            data = self.parser_key_data()
            if data == 'ONAY':
                return kart_id

            if data == 'sil':
                kart_id = kart_id[:-1]

            elif data not in ("Benzin", "Motorin", "LPG", "Dizel"):
                kart_id += data
            text = f"Urun: {secim:<33} Kart ID:{kart_id}"
            self.print_onscreen(text)
            time.sleep(0.025)

    def plaka(self, secim):
        plaka = ""
        text = f"Urun: {secim:<33} Plaka:{plaka}"
        self.print_onscreen(text)
        while True:
            self.poll()
            self.ClearPressKey()
            if self.Communication.last_data[6:8] == "04":
                continue
            data = self.parser_key_data()
            if data == 'ONAY':
                return plaka
            if data == 'sil':
                plaka = plaka[:-1]
            elif data not in ("Benzin", "Motorin", "LPG", "Dizel"):
                plaka += data
            text = f"Urun: {secim:<33} Plaka:{plaka}"
            self.print_onscreen(text)
            time.sleep(0.025)

    def card_plaka_check(self, choice):
        cards = self.cards()
        kart_id = self.kart_id(choice)

        if not kart_id.isnumeric() or int(kart_id) not in [*cards.keys()]:
            self.print_onscreen("Tanimsiz Kart!!!")
            return

        plaka = self.plaka(choice)
        if plaka != cards[int(kart_id)]['Plaka']:
            self.print_onscreen("Kart ile Plaka  Eslesmedi!!!")
            return
        self.ClearPressKey()
        card = {int(kart_id): cards[int(kart_id)]}
        return card

    def miktar(self, secim):
        miktar = ""
        self.poll()
        text = f"Urun: {secim:<33} Miktar:{miktar}TL"
        self.print_onscreen(text)
        while True:
            self.poll()
            self.ClearPressKey()
            if self.Communication.last_data[6:8] == "04":
                continue
            data = self.parser_key_data()
            if data == 'ONAY':
                return miktar
            if data == 'sil':
                miktar = miktar[:-1]
            elif data not in ("Benzin", "Motorin", "LPG", "Dizel"):
                miktar += data
            text = f"Urun: {secim:<33} Miktar:{miktar}TL"
            self.print_onscreen(text)
            time.sleep(0.025)

    def cards(self):
        cards = {}
        con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute("select `ID`,Kart_No,`Gunluk_limit(Lt)`,`Aylik_limit(Lt)`,`Plaka` from kartlar")
        data = cursor.fetchall()
        for i in data:
            cards[i[0]] = {"Kart No": f"{i[1]}", "Günlük Bakiye": f"{i[2]}", "Aylık Bakiye": f"{i[3]}",
                           "Plaka": f"{i[4]}"}
        con.close()
        return cards

    def campaign(self, secim, kart):
        kampanya = {}
        card = [*kart][0]

        con = mysql.connect(host="localhost", user="root", password="13542612", database="avantaj_kart",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute(
            "SELECT musteriler.Ad FROM `musteriler`,kartlar WHERE kartlar.musteri_id=musteriler.ID AND kartlar.ID='" + str(
                card) + "'")
        data = cursor.fetchall()
        musteri = data[0][0]
        con.close()

        con = mysql.connect(host="localhost", user="root", password="13542612", database="kampanya",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute(
            "SELECT `kampanyalar`.ID,kampanyalar.Ad,Baslangıc,Bitis,gecerli_istasyon.Ad,gecerli_musteri.Ad,urun_indirim.Ad,urun_indirim.indirim_orani FROM `kampanyalar`,`gecerli_istasyon`,`urun_indirim`,`gecerli_musteri` WHERE `kampanyalar`.ID=`gecerli_istasyon`.kampanya_id AND `kampanyalar`.ID = `urun_indirim`.kampanya_id AND `kampanyalar`.ID = `gecerli_musteri`.kampanya_id AND `gecerli_istasyon`.Ad = '" + istayon + "' AND `urun_indirim`.Ad='" + secim + "' AND gecerli_musteri.Ad = '" + musteri + "'")
        data = cursor.fetchall()
        con.close()
        try:
            for i in data:
                kampanya[i[0]] = {"Kampanya Adı": f"{i[1]}", f'Başlangıç Tarihi': f'{i[2]}', f"Bitiş Tarihi": f"{i[3]}",
                                  f"İstasyon": f"{i[4]}", f"Müşteri": f"{i[5]}", f"Ürün": f"{i[6]}",
                                  f"İndirim Oranı": f"{i[7]}"}
        except:
            pass
        return kampanya

    def kampanya_control(self, gecerli_kampanya):
        kampanya = {}
        maks_indirim = []

        for i in gecerli_kampanya:
            basla = time.mktime(datetime.strptime(f"{gecerli_kampanya[i]['Başlangıç Tarihi']}", '%d.%m.%Y').timetuple())
            bitis = time.mktime(
                datetime.strptime(f"{gecerli_kampanya[i]['Bitiş Tarihi']} 23:59:59", '%d.%m.%Y %H:%M:%S').timetuple())
            now = time.mktime(date.timetuple())
            if now - basla > 0 and now - basla < bitis - basla:
                kampanya[i] = gecerli_kampanya[i]

        gecerli_kampanya = {}

        for i in kampanya.values():
            maks_indirim.append(int(i['İndirim Oranı']))

        try:
            index = maks_indirim.index(max(maks_indirim))

            key_kampanya = [*kampanya.keys()][index]

            gecerli_kampanya[key_kampanya] = kampanya[key_kampanya]
        except:
            pass

        if len(gecerli_kampanya) != 0:
            return gecerli_kampanya

    def bakiye_kontrol(self, card,gecerli_kampanya):
        key = [*card][0]
        con = mysql.connect(host="localhost", user="root", password="13542612", database="islemler",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute("select * from islemler where islemler.kart_no='" + card[key]['Kart No'] + "'")
        data = cursor.fetchall()

        kalan_gnlk = float(card[key]['Günlük Bakiye'])
        kalan_aylk = float(card[key]['Aylık Bakiye'])

        for i in data:
            if date.strftime('%d.%m.%Y') == i[9]:
                kalan_gnlk -= i[7]

            if date.strftime('%m.%Y') == i[9][-7:]:
                kalan_aylk -= i[7]

        print(kalan_aylk,kalan_gnlk)

        if kalan_aylk <= 0 or kalan_gnlk <= 0 or gecerli_kampanya is None:
            return 0

        if kalan_aylk >= kalan_gnlk:
            return kalan_gnlk

        if kalan_aylk < kalan_gnlk:
            return kalan_aylk

    def indirim_orani(self, kampanya):
        key_campaign = [*kampanya][0]
        indirim_orani = int(kampanya[key_campaign]['İndirim Oranı'])
        return indirim_orani

    def islem(self, secim, miktr, indirim_miktari, indirim_orani):

        con = mysql.connect(host="localhost", user="root", password="13542612", database="urun_fiyat",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute("select urun_fiyat.`fiyat(TL/L)` from  urun_fiyat where urun_fiyat.urun='" + secim + "'")
        data = cursor.fetchall()
        fiyat = data[0][0]

        miktar = int(miktr)
        indirimli_fiyat = fiyat - indirim_orani * fiyat / 100

        if miktar/fiyat > indirim_miktari:
            alinan_miktar = indirim_miktari + (miktar - indirim_miktari*indirimli_fiyat) / fiyat

        else:
            alinan_miktar = miktar/indirimli_fiyat
            indirim_miktari=alinan_miktar

        return [fiyat, indirim_miktari, alinan_miktar]

    def print_islem(self, card, secim, miktar, indirim,gecerli_kampanya):
        odenen = 0.0
        l = 0.0
        key = [*card][0]
        kart_no = card[key]['Kart No']
        plaka = card[key]['Plaka']

        if gecerli_kampanya is not None:
            key_kampanya=[*gecerli_kampanya][0]
            kampanya = gecerli_kampanya[key_kampanya]['Kampanya Adı']
        else:
            kampanya = "Yok"

        while odenen < float(miktar):
            if (float(miktar) - odenen) < 2 and (float(miktar) - odenen) > 0.25:
                l += 0.01
            if float(miktar) - odenen <= 0.25:
                l += 0.0002
            if (float(miktar) - odenen) > 2:
                l += 0.06
            odenen = l * indirim[0]
            text = f"Urun: {secim}        L:{round(l, 2)}   TL:{round(odenen, 2)}    TL/L:{indirim[0]}"
            self.print_onscreen(text)
            time.sleep(0.0002)

        con = mysql.connect(host="localhost", user="root", password="13542612", database="islemler",
                            auth_plugin='mysql_native_password')
        cursor = con.cursor()
        cursor.execute("insert into islemler values (NULL,'" + kart_no + "','" + plaka + "','" + secim + "','" + str(indirim[0]) + "','" + str(miktar) + "','" + str(indirim[2]) + "','" + str(indirim[1]) + "','" + kampanya + "','" + date.strftime('%d.%m.%Y') + "','" + date.strftime('%H:%M:%S') + "')")
        cursor.execute("commit")


def main():
    MyCommunication = Communication(IP="192.168.1.202", PORT=3000)
    MyPaytech = Paytech(MyCommunication, "3A")
    MyPaytech.Keyboard_enable()

    while True:
        MyPaytech.Clear_Screen()
        MyPaytech.ClearPressKey()
        MyPaytech.poll()
        MyPaytech.print_onscreen("1) Benzin           2) Dizel            3) Motorin          4) LPG")
        secim = MyPaytech.choice()
        kart = MyPaytech.card_plaka_check(secim)
        print(kart)

        if kart is None:
            time.sleep(3)
            continue

        campaigns = MyPaytech.campaign(secim, kart)
        gecerli_kampanya = MyPaytech.kampanya_control(campaigns)
        print(gecerli_kampanya)

        if gecerli_kampanya is not None:
            indirim_orani = MyPaytech.indirim_orani(gecerli_kampanya)
        else:
            indirim_orani = 0
            MyPaytech.print_onscreen("Kampanya Bulunamadi")
            time.sleep(3)

        miktr = MyPaytech.miktar(secim)

        indirim_miktari = MyPaytech.bakiye_kontrol(kart,gecerli_kampanya)
        print(indirim_miktari)

        transaction = MyPaytech.islem(secim, miktr, indirim_miktari, indirim_orani)

        MyPaytech.print_islem(kart,secim, miktr, transaction, gecerli_kampanya)

        time.sleep(3)

main()
