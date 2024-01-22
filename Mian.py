""" 
!!!
Disclaimer: Diese Klasse sollte nie als Teil eines Skriptes, oder Programms importiert werden, da hier die main Methode immer ausgefuehrt wird.
Eine Pruefung durch if __name__ == __main__ findet nicht statt.
!!!
"""
import pandas as pd                     #Package fuer das Parsen von CSV Dateien
import ipaddress                        #Package fur das Handling von IP Adressen
import ping3                            #Package fuer das Ausfuehren der Pings
import time                             #Wird genutzt, um Wartezustaende im Programm auszuloesen
import os                               #Package um Systeminformationen, wie Dateipfade zu pruefen 


#Erweitert die Klasse Exception um die Subklasse FChoice > Spezifischeres Exception Handling siehe menu()
class FChoice(Exception):
    pass


#Erweitert die Klasse Exception um die Subklasse StepFault > Spezifischeres Exception Handling siehe eingabeIPRange()
class StepFault(Exception):
    pass


#Erweitert die Klasse Exception um die Subklasse ModusError > Spezifischeres Exception Handling siehe parseParamFile() 
class ModusError(Exception):
    pass


#Hilfsfunktion, welche Ueberprueft, ob ein uebergebener Wert "test_val" eine gueltige IP-Adresse ist
def checkIP(test_val):
    try:
        #Versuche test_val in ein Objekt der Klasse ipaddress zu casten, wenn moeglich dann -> True
        ipaddress.IPv4Address(test_val)
        return True

    except:
        #Falls test_val nicht dem Format einer IP entspricht wird dieser Fehler hier abgefangen -> False
        print(f"{test_val} ist keine gueltige IP Adresse. Bitte geben sie diese im Folgenden selbst ein.")
        return False


#Hilfsfunktion, welche Ueberprueft, ob eine Datei plist.csv mit dem gegebenen Pfad existiert
def checkParamFile():
    #Existiert die Datei -> True ansonsten -> False
    if os.path.isfile("C:\Projekt\plist.csv"):
        return True
    return False


#Funktion, welche die CSV Datei ausliest und anhand dieser eine Parameterliste erzeugt und zurueckgibt -> list
def parseParamFile():
    #Definieren der Variable path durch den Standardpfad der Parameterdatei
    path = "C:\Projekt\plist.csv"

    #df ist eine Objektvariable der Klasse pandas. Hier wird die csv Datei in Zeilen und Spalten dargestellt.
    #Delimiter ist das Datentrennende Symbol in der CSV. Die 1. Spalte (Erster Wert in jeder Zeile) erhaelt den Bezeichner Eigenschaft und die 2. Wert.
    df = pd.read_csv(path, delimiter=";", header=None, names=["Eigenschaft", "Wert"])

    
    values = [] #Initalisieren der Liste für die Parameter

    #Die for-Schleife itterriert durch die CSV. Der Inhalt wird durch iterrows() anhand von Indexen angegeben jeder Index beinhaltet die Daten einer Zeile
    for index, row in df.iterrows():
        try:
            #Wenn eine Zeile den Wert -? wird die Funktion abgebrochen und -> None zurueckgegeben
            if row["Wert"] == "-?" or row["Eigenschaft"] == "-?":
                return None

            #Wenn eine ungueltiger Wert fuer den Modus angegeben wurde (nicht zwischen 1 und 3) values zurueckgeben und entsprechenden Fehler ausloesen
            if row["Eigenschaft"] == "Modus (IPAdresse [1], IPRange [2], Rechnername[3])" and not (1 <= int(row["Wert"]) <= 3):   
                
                #Befuellen der Liste mit None Werten, um spaetere Errors bei der Verarbeitung der Liste zu vermeiden
                values.append(None)
                values.append(None)
                values.append(None)
                raise ModusError

            #Wenn der Modus 3(Geraetenamen) ausgewaehlt wurde und die Zeile IP1 erreicht ist
            if row["Eigenschaft"] == "IP1" and values[2] == 3:
                value = str(row["Wert"])                        #PCNamen als String in value zwischenspeichern
                values.append(value)                            #value der Liste anhaengen
                values.append(None)                             #Ein None Element anfuegen um spaetere Errors zu vermeiden
                return values                                   #Liste der Parameter(values) zurueckgeben

            #Ansosnten wenn der Modus 1(eine IP) oder 2(IPRange) angegeben wurde und die Zeile IP1 erreicht wurde
            elif row["Eigenschaft"] == "IP1" and (values[2] == 1 or values[2] == 2):
                
                #Ueberpruefen ob der Wert von IP1 eine IPAdresse darstellt mithilfe der Hilfsfunktion checkIP
                if checkIP(row["Wert"]):
                    value = str(row["Wert"])    #IPAdresse wird als Sting in value zwischengespeichert
                    values.append(value)        #value wird der Liste values angehangen
                    if values[2] == 1:          #Wenn der Modus 1 (EingabeIP) angegeben wurde
                        values.append(None)     #Anhaengen eines None Elements, um Fehler bei der Verarbeitung zu verhindern
                        return values           #Liste values zurueckgeben und somit die Funktion beenden, da keine Werte mehr benoetigt werden
                    continue                    #Falls der Modus 2 gewaehlt wurde wird der restliche Teil des Durchlaufes for-Schleife uebersprungen
                values.append(None)             #Falls eine ungueltige IP angegeben wurde wird die Liste mit None Elementen befuellt
                values.append(None)
                return values                   #values ohne eingetragene IP Adresse zurueckgeben, da diese Fehlerhaft war
            
            #Ansosnten wenn der Modus 2 (IPRange) angegeben wurde
            elif row["Eigenschaft"] == "IP2" and values[2] == 2:
                
                #Ueberpruefen ob der Wert von IP1 eine IPAdresse darstellt mithilfe der Hilfsfunktion checkIP
                if checkIP(row["Wert"]):
                    value = str(row["Wert"])    #IPAdresse wird als Sting in value zwischengespeichert
                    values.append(value)        #value wird der Liste values angehangen
                    return values               #Liste values zurueckgeben und somit die Funktion beenden, da keine Werte mehr benoetigt werden
                values.append(None)             #Falls eine ungueltige IP angegeben wurde wird die Liste mit None Elementen befuellt
                return values                   #values ohne eingetragene IP Adresse zurueckgeben, da diese Fehlerhaft war

            value = int(row["Wert"])            #Wert des Parameters als Ganzzahl casten und in value zwischenspeichern
            values.append(value)                #value an values anhaengen

        #Wird ausgefuehrt, sobald beim Type Casten der Parameter ein Fehler auftritt
        except ValueError:
            print(f"Ein ungueltiger Parameter wurde Uebergeben. {row['Eigenschaft']} : {row['Wert']}")  #Ausgabe der Fehlerbeschreibung
            print("Sie werden nun gebeten die Parameter erneut einzugeben\n")
            return None                                                                                 #keinen Wert zurueckgeben

        #Wird durch "raise ModusError" aufgerufen, falls ein ungueltiger Modus eingegeben wurde
        except ModusError:
            print("Der Modus wurde nicht zwischen 1-3 gewaehlt. Es wird sich im Folgenden die Auswahl oeffnen.\n")  #Ausgabe der Fehlerbeschreibung
            return values                                                                                           #Rueckgabe der Liste values
    
    return values   #Falls unerwartet kein Return ausgeloest wird, gilt dieses als Fallback, damit das Programm weiterhin ablaueft.


#Diese Funktion dient der Eingabe der Standard Parameter fuer den Timeout und die Anzahl der Iterationen
def enterArgs():
    values = []     #Initialisierung der Parameterliste(values)
 
    #Unendlichschleife bis die Funktion beendet wird durch die Rueckgabe der Parameterliste(values)
    while True:
        try:
            print("Der Timeout zwischen den Scans beschreibt die Zeit, welche zwischen den Scans gewartet wird.\n"
                  "Bei einem Timeout von 4000 und 2 Scans wird zwischen den 1. und 2. Scans 4 Sekunden gewartet\n\n")   #Anweisung zum Handling ausgeben
            values.append(int(input("Gebe den Timeout zwischen den Scans in ms an: ")))                                 #Eingabe als Integer
            values.append(int(input("Gebe die Anzahl der Scans ein: ")))                                                #Eingabe als Integer
            values.append(None)                                                                                         #Fuellen der Liste mit None
            values.append(None)
            values.append(None)
            print()                                                                                                     #Leerzeile
            return values                                                                                               #Rueckgabe der Parameter

        #Falls keine Ganzzahl als Wert eingegeben wird, werden die Parameter erneut abgefragt
        except ValueError:
            print("\nBitte beachten sie, dass alle Werte nur als Ganzzahlen angegeben werden.\n")                       #Ausgabe Fehlerbeschreibung


#Funktion um die Optionen des Programms zu Listen und die des Users gewuenschte Aktion abzufragen
def menu():
    
    #Endlosschleife bis eine gueltige Option eingegeben wurde
    while True:
        try:
            #Auflistung der Optionen
            print("1. Eingabe einer IP Adresse")
            print("2. Eingabe einer IP-Range")
            print("3. Eingabe eines Rechnernamens")
            print("4. Programm beenden")

            choice = int(input("Bitte gebe einer der Optionen (1-4) ein: "))    #Eingabe der Option als Integer
            print()                                                             #Ausgabe einer Leerzeile
            
            #Falls die angegeben Zahl nicht zwischen inklusive 1 und 4 liegt loese einen Fehler aus
            if choice not in range(1,5):
                raise FChoice                                                   #Ausloesen des Fehlers "FChoice" (FalseChoice)
            
            return choice                                                       #Rueckgabe der Option

        #Falls keine ganze Zahl eingegeben wurde wird dieser Fehler ausgeloest
        except ValueError:
            print(f"\nEs muss eine Zahl eingegeben werden.\n")                  #Ausgabe Fehlerbeschreibung
        
        #Falls keine gueltige Option ausgewaehlt wurde wird dieser Fehler ausgeloest.
        except FChoice:
            print(f"\nDie Zahl {choice} ist nicht als Option (1-4) gelistet.\n")      #Ausgabe Fehlerbeschreibung


#Funktion zur Eingabe und Validierung einer IP Adresse durch den User
def eingabeIP():
    
    #Endlosschleife bis eine gueltige IP-Adresse eingegeben wurde
    while True:
        try:
            ipadd = ipaddress.IPv4Address(input("Bitte gebe eine IP in dem Format AAA.BBB.CCC.DDD ein: "))  #Eingabeaufforderung der IP-Adresse
            return str(ipadd)                                                                               #Rueckgabe der IP-Adresse als String
        
        #Wenn die Eingegebene IP ungueltig ist, wird ein ungueltiger Datentyp fuer die Funktion ipaddress.IPv4Address an diese uebergen.
        #Dies loest diesen Fehler aus
        except Exception as e:
            print("\nDie IP adresse ist ungueltig. " + str(e) + "\n")                                       #Ausgabe Fehlerbeschreibung
    

#Funktion fuer die Eingabe eines Adress Bereiches. Hier sind ip und ip2 mit None vorparametrisiert, falls keine Werte fuer diese Uebergeben werden.
def eingabeIPRange(ip=None, ip2=None):
    
    #Endlosschleife bis eine gueltige IP Range angegeben wurde
    while True:
        try:
            #Wenn ip oder ip2 keinen Wert besitzt
            if ip == None or ip2 == None:
                ip = ipaddress.IPv4Address(input("Bitte geben Sie die erste IP-Adresse ein (X.X.X.X): "))   #Eingabe erste IP
                ip2 = ipaddress.IPv4Address(input("Bitte geben Sie die zweite IP-Adresse ein (X.X.X.X): ")) #Eingabe zweite IP
            
            #Wenn bereits Werte fuer die IP Adressen uebergeben wurden    
            else:
                ip = ipaddress.IPv4Address(ip)                                                              #Erste IP zu einem Objekt von ipaddress casten
                ip2 = ipaddress.IPv4Address(ip2)                                                            #Zweite IP zu einem Objekt von ipaddress casten
            ip_int = int(ip)                                                                                #IP Adresse in einen Integer casten
            ip2_int = int(ip2)                                                                              #Zweite IP Adresse in einen Integer casten
            
            #Wenn die erste Adresse ueber der zweiten Adresse liegt, wird ein entsprechender Fehler ausgeloest
            if ip_int >= ip2_int:
                raise StepFault
            ip_step = range(ip_int, ip2_int+1)                                                              #Liste mit differenz aller IPAdressen generieren
            ips = [str(ipaddress.IPv4Address(ip_int)) for ip_int in ip_step]                                #Alle IP Adressen als String in ips speichern
            return ips                                                                                      #Rueckgabe der Liste aller IP Adressen (ips)

        #Diese Exception wird ausgeloest, wenn die angegebenen IP Adressen gleich sind, oder die Startadresse ueberhalb der endadresse liegt
        except StepFault:
            print("\nDie erste IP-Adresse muss unter der zweiten IP-Adresse liegen!\n")                     #Ausgabe Fehlerbeschreibung
            ip, ip2 = None                                                                                  #Zuruecksetzen der IP Adressen
        
        #Diese Exception wird ausgeloest, wenn die angegebene IP ungueltig ist.
        except Exception as e:
            print("\nBitte geben Sie gueltige IP-Adressen ein!", str(e) + "\n")                             #Ausgabe Fehlerbeschreibung


#Funktion fuer die Eingabe eines Rechnernamens durch den User.
def eingabeRechnername():
    return input("Bitte gebe einen Rechnernamen ein: ")                                                     #Rueckgabe der Eingabe


#Diese Funktion ist für das Pingen der Rechner verantwortlich
def ping_devices(device_list, timeout=0, iteration=1):

    #Initialisierung des Dictionaries fuer die Werte im Scan, sowie Definition des Iterators i.
    results = {}
    i=1

    #Schleife zur Wiederholung der einzelenn Scans
    while i <= iteration:

        print(f'\nScanndurchgang ({i})\n')
        
        #Ausführen eines Scans, dh. für jedes Gerät in der übergebenen Liste
        for device in device_list:
            try:

                # Pinge das Gerät und speichere das Ergebnis in "result" zwischen
                result = ping3.ping(device, unit="ms", timeout=0.5)

                #Spezifizierung des Rueckgabewerts anhand des Variablen Werts von Result und dessen Speicherung im Dictionary.
                if result == None:
                    result = "Host ist nicht erreichbar (Request Timed out)"
                    results[device] = result
                elif result == False:
                    result = "Host ist nicht erreichbar (Host unknown, cannot resolve host)"
                    results[device] = result
                else:
                    result = f"{result}ms"
                    results[device] = result

                #Echtzeit Ausgabe der Ping Ergebnisse    
                print(f"{device}: {result}")

            except Exception as e:
                # Falls ein Fehler auftritt, speichere eine entsprechende Meldung im Dictionary
                results[device] = f"Fehler beim Pingen: {str(e)}"
                print(f"{device}: {result}")
        #Warte die angegebene Zeit vor dem nächsten Scan
        time.sleep(timeout)
        #Schleifendurchlauf +1
        i += 1


#Main Methode

#Pruefe ob die Parameterdatei vorhanden ist
if checkParamFile():
    args = parseParamFile()         #Parameter in args als Liste Speichern, oder bei fehlern args = None         
    print(args)

else:   
    args = None                     #Falls keine Parameterliste vorhanden ist wird args ohne Wert initialisiert

if args == None:                    #Falls args keinen Wert besitzt
    args = enterArgs()              #Parameter werden durch den User in enterArgs() eingegeben und als Rueckgabewert in args gespeichert

timeout = args[0] / 1000            #args[0] ist der Wert fuer den Timeout. Dieser wird in Sekunden umgerechnet und in timeout gespeichert
iteration = args[1]                 #args[1] ist der Wert fuer die Anzahl der Scans. Dieser wird in iteration gespeichert
choice = args[2]                    #args[2] ist der Wert für die Auswahl der Aktion. Dieser wird in choice gespeichert
ip = args[3]                        #args[3] ist die erste IP-Adresse, oder der Geraetename, welche vom Nutzer gepingt wird. Diese wird in IP gespeichert
ip1 = args[4]                       #args[4] ist die zweite IP-Adresse fuer die IP Range. Diese wird in ip1 gespeichert.

#Falls choice keinen Wert hat
if choice == None:
    choice = menu()                 #Rufe die Funktion menu() auf und speichere deren Rueckgabe Wert in choice

#Prueft den Wert von choice und fuehrt anhand des Wertes die von dem Nutzer gewuenschte Funktion aus.
if choice == 1:         
    if ip == None:                                  #Falls ip nicht vorher durch die Parametrisierung einen Wert zugewiesen wurde
        ip = eingabeIP()                            #ip den Rueckgabewert der Funktion eingabeIP() zuweisen
    ping_devices([ip], timeout, iteration)          #Aufruf des Funktion ping_devices() anhand der IP und der Parameter timeout und iteration
elif choice == 2:
    ips = eingabeIPRange(ip, ip1)                   #ips wird der Rueckgabewert von eingabeIPRange() zugewiesen. ip und ip1 sind entweder None oder gueltige IP Adressen
    ping_devices(ips, timeout, iteration)           #Aufruf der Funktion ping_devices() anhand der Liste ips und den Parametern timeout und iteration
elif choice == 3:
    if ip == None:                                  #Falls der IP nicht vorher durch die Parametrisierung einen Wert zugewiesen wurde
        ip = eingabeRechnername()                   #ip den Rueckgabewert der Funktion eingabeRechnernamen() zuweisen
    ping_devices([ip], timeout, iteration)          #Aufruf der Funktion ping_devices() anhand des Rechnernamens und den Parametern timeout und iteration
elif choice == 4:
    print("Das Programm wird beendet.")             #Ausgabe dass das Programm beendet wird
else:
    print("Unerwarteter Fehler")                    #Falls choice einen Wert, welcher nicht zwischen inklusive 1 und 4 ist, besitzt wird ein Fehler ausgegeben.

