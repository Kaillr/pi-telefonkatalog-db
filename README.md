# Installasion av telefonkatalog og database på Raspberry Pi

<em>Her skal du lære hvordan man setter opp en Raspberry Pi og hvordan man setter opp en database til en telefonkatalog.</em>


### Raspberry Pi installasjon
Først og fremst må du vite at du har alt du trenger. Dette er en Raspberry Pi, en annen datamaskin, en mikro-HDMI ledning og en monitor for å koble til Raspberry Pien.

1. Plugg inn strøm i Raspberry Pien og koble den til en monitor med mikro-HDMI ledningen.
2. Nå vil du få mulighet til å velge hvilket OS (opperativsystem) du vil installere. Velg Raspbian Full og følg stegene som blir vist på skjermen.
3. Da du er inne, så er det ganske lurt å koble til internett. Plugg inn en ethernet ledning i Raspberry Pien om du har det. Hvis ikke han du koble til WiFi.

### Installere programmer
1. Åpne terminal vinduet vet å finne den i taskbaren eller ved å trykke ```ctrl + alt + t```.
2. Start med å kjøre disse kommandene for å få de seneste versjonene av programmene på Pien:
```shell
sudo apt update
sudo apt upgrade
```
\
3. Deretter installer filene som trengs for dette prosjektet
```shell
sudo apt install openssh-server
sudo apt install mariadb
sudo apt install ufw # Brannmur
```
\
4. For å sjekke om programmene er installert, så er det lurt å kjøre which kommandoen. Da vil du se hvor programmet er installert.
```shell
which openssh-server
which mariadb
which ufw
```
### Sett opp Brannmur
1. Start med å skru på brannmuren for å sikre at endringene dine vil bli brukt.
```shell
sudo ufw enable
```
\
2. Nå må du velge hvilke porter som skal være åpne. I ditt tilfelle vil dette være port for ssh og database.
```shell
sudo ufw allow 22/tcp # ssh
sudo ufw allow 3306/tcp # MariaDB
```
### Koble til Pi med ssh

Om du vil bruke Raspberry Pien uten å tenge å koble den til en skjerm, så burde du bruke ssh. Dette lar det bruke terminalen til Pien fra en annen datamaskin.

1. Skru på ssh for å kunne koble til fra en annen datamaskin.
```shell
# Start ssh server ved oppstart av Pi
sudo systemctl enable ssh

# Starter ssh nå
sudo systemctl start ssh
```
\
2. Om du vil koble til Pien med ssh, så er det viktig å vite hva ip adressen er. Skriv denne kommandoen for å se IPv4 adressen du skal bruke til å koble til.
```shell
hostname -I # Viser alle aktive IPv4 adresser
```
\
3. Åpne terminalen på PCen du vil bruke for å koble til Raspberry Pien med ssh. Deretter skriv dette.
```shell
ssh brukernavn@ipv4 # Bytt ut brukernavnet med ditt Raspberry Pi brukernavn og IPV4 med Raspberry Pi ip adressen 
```
Du vil få spørsmål om å skrive inn passordet, da må du skrive inn passordet til Raspberry Pien. Deretter når den spør om fingerprint, skriver du "yes".

### Oppsett av database på Pi med ssh

1. Åpne MariaDB med sudo
```shell
sudo mariadb
```
2. Lag en bruker med et passord
```sql
CREATE USER '[brukernavn]'@'%' IDENTIFIED BY '[passord]'; -- Bytt ut [brukernavn] og [passord] med brukernavnet og passordet du vil lage 
```
3. Gi denne brukeren tillgang til alle mariadb kommandoer.
```sql
GRANT ALL PRIVILEGES ON *.* TO '[brukernavn]'@'%' IDENTIFIED BY '[passord]'; -- Bytt ut [brukernavn] og [passord]

FLUSH PRIVILEGES;
```
4. Logg ut av MariaDB ved å skrive:
```sql
exit
```
5. Logg inn i din nye MariaDB bruker
```shell
mariadb -u [brukernavn] -p # Bytt ut [brukernavn]
```
Skriv inn passordet til brukeren.

7. Nå som du er logget inn så kan vi sette opp databasen
```sql
CREATE DATABASE telefonkatalog; -- Lager telefonkatalog databasen

USE telefonkatalog; -- Bruk den nye databasen

-- Lag tabellen hvor du putter inn data
CREATE TABLE person (
    id int NOT NULL AUTO_INCREMENT,
    fornavn VARCHAR(255) NOT NULL,
    etternavn VARCHAR(255) NOT NULL,
    telefonnummer CHAR(8),
    PRIMARY KEY (id)
);

-- Legg inn test data i tabellen
INSERT INTO person (fornavn, etternavn, telefonnummer)
VALUES ('Erik', 'Perik', '12345678');
INSERT INTO person (fornavn, etternavn, telefonnummer)
VALUES ('Lise', 'Pise', '22334455');
INSERT INTO person (fornavn, etternavn, telefonnummer)
VALUES ('Testus', 'Jensen', '11114444');
INSERT INTO person (fornavn, etternavn, telefonnummer)
VALUES ('Knut', 'Donald', '31415926');
```

### Sett opp telefonkatalog.py med tillgang til database

1. Lag en ny python fil hvor som heldst på PCen din ved å høyre-trykke musen din, og trykk ny, tekstdokument. Endre navnet på denne filen til "telefonkatalog.py".
2. Høyretrykk telefonkatalog filen, og trykk rediger med notepad.
3. Skriv dette inn i telefonkatalog.py
```python
import mysql.connector
import os

mydb = mysql.connector.connect(
    host="10.2.4.40",
    user="pi",
    password="pass123",
    database="telefonkatalog"
)

def printMeny():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("------------------- Telefonkatalog -------------------")
    print("| 1. Legg til ny person                              |")
    print("| 2. Søk opp person eller telefonnummer              |")
    print("| 3. Vis alle personer                               |")
    print("| 4. Avslutt                                         |")
    print("------------------------------------------------------")
    menyvalg = input("Skriv inn tall for å velge fra menyen:")
    utfoerMenyvalg(menyvalg)

def utfoerMenyvalg(valgtTall):
#input returnerer string
    if(valgtTall == "1"):
        registrerPerson()
    elif(valgtTall == "2"):
        sokPerson()
        printMeny()
    elif(valgtTall == "3"):
        visAllePersoner()
    elif(valgtTall == "4"):
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N")
        if(bekreftelse == "J" or bekreftelse == "j"):
            exit()
            #Gidder ikke sjekk for n. Fortsetter hvis ikke j
        else:
            printMeny()             
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-4.")
        utfoerMenyvalg(nyttForsoek)

def registrerPerson():
    fornavn = input("Skriv inn fornavn:")
    etternavn = input("Skriv inn etternavn:")
    telefonnummer = input("Skriv inn telefonnummer:")

    lagreIDatabase(fornavn, etternavn, telefonnummer)

    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()

def visAllePersoner():

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM person")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    mydb.close()
    printMeny()

def sokPerson():
    print("1. Søk på fornavn")
    print("2. Søk på etternavn")
    print("3. Søk på telefonnummer")
    print("4. Tilbake til hovedmeny")
    sokefelt = input("Skriv inn ønsket søk 1-3, eller 4 for å gå tilbake:")
    if(sokefelt == "1"):
        navn = input("Fornavn:")
        finnPerson("fornavn", navn)
    elif(sokefelt == "2"):
        navn = input("Etternavn:")
        finnPerson("etternavn", navn)
    elif(sokefelt == "3"):
        tlfnummer = input("Telefonnummer:")
        finnPerson("telefonnummer", tlfnummer)
    elif(sokefelt == "4"):
        printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-4.")
        sokPerson()

        
#typeSok angir om man søker på fornavn, etternavn, eller telefonnumer
def finnPerson(typeSok, sokeTekst):
    global mydb

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM person where " + typeSok + " ='" + sokeTekst + "'")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
    
    

def lagreIDatabase(fornavn, etternavn, telefonnummer):
    global mydb

    mycursor = mydb.cursor(fornavn, etternavn, telefonnummer)

    sql = "INSERT INTO person (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)"
    val = (fornavn, etternavn, telefonnummer)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")



printMeny() #Starter programmet ved å skrive menyen første gang
```
4. Endre informasjonen i ```mysql.connector.connect()``` til din database
```python
mydb = mysql.connector.connect(
    host="0.0.0.0", # Bruk ip adressen til Raspberry Pien
    user="brukernavn", # Bruk ditt MariaDB brukernavn
    password="passord", # Bruk ditt MariaDB passord
    database="telefonkatalog" # Database navnet
)
```

### Kjør telefonkatalog.py
1. Last ned Pyhton fra https://www.python.org/downloads/ om du allerede ikke har det på PCen din.
2. Kjør telefonkatalog.py og test de forskjellige funksjonene i programmet.

Om du har gjort alt rett, så vil programmet kunne kjøre, og ha tilgang til databasen på Pien din!