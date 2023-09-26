import ipaddress as ipadd  # Bibliothek, um IPs zu checken etc.
import os  # Future Use
import re  # Bibliothek, um IP Adressen zu prüfen, auch wenn Geraetenamen enthalten sind
import platform
import pandas as pd  # Bibliothek, um CSVs zu parsen


class OutOfMenu(Exception):
    pass


class MissIpStep(Exception):
    pass


"""
Methode für den Filter um leere Felder der CSV zu filtern
"""


def is_nan(element) -> bool:
    if element == "nan":
        return False
    return True


def check_conf_file() -> bool:
    path = '\\Users\light\Documents\Schule\config.csv'
    return os.path.isfile(path)


def validate_ping_parameters(parameters):
    valid_parameters = {
        "Windows": ["-t", "-a", "-n", "-l", "-f", "-i", "-v", "-r", "-s", "-j", "-k", "-w", "-R", "-S", "-c", "-p"],
        "Linux": ["-c", "-D", "-d", "-f", "-F", "-I", "-i", "-l", "-M", "-m", "-n", "-p", "-Q", "-q", "-R", "-s", "-S",
                  "-T", "-t", "-U", "-u", "-v", "-V", "-w", "-W", "-x"],
        "Default": []
    }

    numeric_params = {
        "Windows": ["-n", "-l", "-i", "-v", "-r", "-s", "-w"],
        "Linux": ["-c", "-f", "-i", "-l", "-n", "-p", "-q", "-s", "-t", "-w", "-W"]
    }

    continuing_params = {
        "Windows": ["-j", "-k", "-S", "-c"],
        "Linux": []
    }

    system = platform.system()
    if system not in valid_parameters:
        print("Der Ping Befehl ist lediglich auf Window und Linux ausgelegt.")
        return False

    i = 0
    while i < len(parameters):
        param = parameters[i]
        if param not in valid_parameters[system]:
            print(f"{param} ist kein gueltiger Parameter.")
            return False

        if param in numeric_params[system]:
            if i + 1 < len(parameters):
                next_param = parameters[i + 1]
                if not next_param.isdigit():
                    print(f"{param} benötigt ein nummerisches Attribut")
                    return False
                i += 1  # Iterator auf das Attribut setzen.
            else:
                print(f"{param} benötigt ein nummerisches Attribut")
                return False

        elif param in continuing_params[system]:
            if i + 1 < len(parameters):
                next_param = parameters[i + 1]
                if next_param.startswith("-"):
                    print(f"{param} benötigt ein Argument")
                    return False
                i += 1  # Iterator auf das Attribut setzen.
            else:
                print(f"{param} benötigt ein Argument")
                return False

        else:
            if i + 1 < len(parameters):
                next_param = parameters[i + 1]
                if not next_param.startswith("-"):
                    print(f"{param} akzeptiert keine Attribute")
                    return False

        i += 1  # Iterator auf nächsten Parameter setzen.

    return True


def parse_parameters():
    pass


def parse_devices():
    path = '\\Users\light\Documents\Schule\ipliste.csv'
    if not os.path.isfile(path):
        print(f'Es wurde keine Liste mit Geraeten unter {path} gefunden!')
        return None
    df = pd.read_csv(path)
    text_series_list = [df[col].astype(str) for col in df.columns]  # Parsed CSV in pandas DataFrame
    text_strings = [' '.join(text_series) for text_series in text_series_list]  # Parsed DataFrame in text String
    devices = []
    for text_string in text_strings:
        x = filter(is_nan, text_string.split(" "))  # nan Elemente aus der IP-Liste löschen
        devices += list(x)  # Erstellen einer normalisierten Liste der IP-Adressen
    try:
        for element in devices:
            if re.match(r'\b\d+\.\d+\.\d+\.\d+\b', element):
                ipadd.ip_address(element)
    except Exception as e:
        print(f'Die IP-Adresse {element} ist ungueltig!', str(e))
        return None
    return devices  # Liste mit IPs und Hostnamen übergeben.


def enter_ip():
    while True:
        try:
            ip = ipadd.ip_address(input("Bitte geben Sie eine IP-Adresse ein (X.X.X.X): "))
            return [ip]
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
    return [device]


def process_parameter(parameter=None):
    if parameter is not None:
        if validate_ping_parameters(parameter):
            os.system("cls")
            print("Die Eingabe der Parameter wurde akzeptiert")
        else:
            desc = ["Die Config-Datei enthielt Fehler bei den oben genannten Parametern!",
                    "Bitte berichtigen Sie die Config, speichern diese und lesen diese neu ein",
                    "Alternativ können Sie die Parameter nun per Hand Eingeben."]
            print("\n".join(desc))
            parameter = None

    while parameter is None:
        choice = input("Bitte geben Sie die Parameter ein. Um die Hilfe aufzurufen -? eingeben.\n"
                       "Mehrere Parameter werden durch ein Leerzeichen getrennt.\n"
                       "Sie koennen in das Menue durch die Eingabe \"e\" gelangen.\n"
                       "Zum Beispiel: -n 4 -w 1000")
        parameter = choice.split()
        if "-?" in parameter:
            os.system("ping -?")
            parameter = None
        elif "e" in parameter:
            return
        elif validate_ping_parameters(parameter):
            os.system("cls")
            print("Die Eingabe der Parameter wurde akzeptiert")
        else:
            parameter = None

        return parameter


def ping_devices(to_ping, parameter=None):
    os.system("cls")
    if to_ping is None:
        print("Es wurde keine IP-Adresse uebergeben.")
        return
    if parameter is None:
        return
    print(True)

def menu_input() -> int:
    x = ["Geben Sie ein:",
         "\t1. Eingabe einer IP-Adresse",
         "\t2. Eingabe eines IP-Adressbereiches",
         "\t3. Eingabe eines Rechnernames",
         "\t4. Eingabe eines Netzwerks",
         "\t5. Einlesen einer IP-Liste",
         "\t6. Einlesen einer Config",
         "\t7. Programm beenden."]
    while True:
        try:
            choice = int(input('\n'.join(x)))
            if 0 < choice < 7:
                os.system("cls")
                return choice
            raise OutOfMenu
        except OutOfMenu:
            os.system("cls")
            print("Es muss die Zahl einer Option gewaehlt werden.\n")
        except Exception as e:
            os.system("cls")
            print("Eingabe einer Zahl gefordert!\n", str(e))


def main():
    if check_conf_file():
        ping_devices(parse_devices(), process_parameter(parse_parameters()))
        pass
    running = True
    while running:
        action = menu_input()
        match action:
            case 1:
                ping_devices(enter_ip(), process_parameter())
            case 2:
                ping_devices(enter_iprange(), process_parameter())
            case 3:
                ping_devices(enter_name(), process_parameter())
            case 4:
                ping_devices(enter_ipnetwork(), process_parameter())
            case 5:
                ping_devices(parse_devices(), process_parameter())
            case 6:
                ping_devices(parse_devices(), process_parameter(parse_parameters()))
            case 7:
                running = False


if __name__ == "__main__":
    main()
