import os  # Future Use
import ipaddress as ipadd  # Bibliothek, um IPs zu checken etc.
import re  # Future Use

import pandas as pd  # Bibliothek, um CSVs zu parsen


class OutOfMenu(Exception):
    pass


class MissIpStep(Exception):
    pass


"""
Methode für den Filter um leere Felder der CSV zu filtern
"""


def is_nan(element):
    if element == "nan":
        return False
    return True


def parse_devices():
    df = pd.read_csv('C:\\Users\light\Documents\Schule\ipliste.csv')
    text_series_list = [df[col].astype(str) for col in df.columns]  # Parsed CSV in pandas DataFrame
    text_strings = [' '.join(text_series) for text_series in text_series_list]  # Parsed DataFrame in text String
    devices = []
    for text_string in text_strings:
        x = filter(is_nan, text_string.split(" "))  # nan Elemente aus der IP-Liste löschen
        devices += list(x)  # Erstellen einer normalisierten Liste der IP-Adressen
    return devices  # Liste mit IPs und Hostnamen übergeben.


def enter_ip():
    while True:
        try:
            ip = ipadd.ip_address(input("Bitte geben Sie eine IP-Adresse ein (X.X.X.X): "))
            return ip
        except Exception as e:
            print("Es wurde eine ungueltige IP eingegeben.", str(e))


def enter_ipnetwork():
    while True:
        try:
            network = input("Bitte geben Sie eine IP-Adresse ein (X.X.X.X/X): ")
            ips_dirty = list(ipadd.ip_network(network).hosts())
            ips = [str(element).split("'") for element in ips_dirty]
            return ips
        except Exception as e:
            print("Es wurde eine ungueltige IP eingegeben.", str(e))


def enter_iprange():
    while True:
        try:
            ip = ipadd.IPv4Address(input("Bitte geben Sie die erste IP-Adresse ein (X.X.X.X): "))
            ip2 = ipadd.IPv4Address(input("Bitte geben Sie die zweite IP-Adresse ein (X.X.X.X): "))
            ip_int = int(ip)
            ip2_int = int(ip2)
            if ip_int >= ip2_int:
                raise MissIpStep
            ip_step = range(ip_int, ip2_int)
            ips_dirty = [ipadd.IPv4Address(ip_int) for ip_int in ip_step]
            ips = [str(element).split("'") for element in ips_dirty]
            return ips

        except MissIpStep:
            print("Die erste IP-Adresse muss unter der zweiten IP-Adresse liegen!")
        except Exception as e:
            print("Bitte geben Sie gültige IP-Adressen ein!", str(e))


def enter_name():
    device = input("Bitte Geraetenamen eingeben")
    return device


def ping_devices():
    pass


def menu_input():
    x = ["Geben Sie ein:",
         "\t1. Eingabe einer IP-Adresse",
         "\t2. Eingabe eines IP-Adressbereiches",
         "\t3. Eingabe eines Rechnernames",
         "\t4. Eingabe eines Netzwerks",
         "\t5. Einlesen einer IP-Liste",
         "\t6. Programm beenden."]
    while True:
        try:
            choice = int(input('\n'.join(x)))
            if 0 < choice < 7:
                return choice
            raise OutOfMenu
        except OutOfMenu:
            print("Es muss die Zahl einer Option gewaehlt werden.")
        except Exception as e:
            print("Eingabe einer Zahl gefordert!", str(e))


def main():
    running = True
    while running:
        action = menu_input()
        match action:
            case 1:
                ping_devices(enter_ip())
            case 2:
                ping_devices(enter_iprange())
            case 3:
                ping_devices(enter_name())
            case 4:
                ping_devices(enter_ipnetwork())
            case 5:
                ping_devices(parse_devices())
            case 6:
                running = False


if __name__ == "__main__":
    main()
