# Installasjon av telefonkatalog og database på Raspberry Pi

*Her skal du lære hvordan man setter opp en Raspberry Pi og hvordan man setter opp en database til en telefonkatalog.*

## Raspberry Pi installasjon

Først og fremst må du vite at du har alt du trenger. Dette inkluderer en Raspberry Pi, en annen datamaskin, en mikro-HDMI ledning og en monitor for å koble til Raspberry Pien.

1. Plugg inn strøm i Raspberry Pien og koble den til en monitor med mikro-HDMI ledningen.
2. Når du er inne, vil du få mulighet til å velge hvilket operativsystem (OS) du vil installere. Velg **Raspbian Full** og følg instruksjonene som vises på skjermen.
3. Det er lurt å koble til internett. Plugg inn en ethernet ledning i Raspberry Pien, eller koble til Wi-Fi.

## Installere programmer

1. Åpne terminalvinduet ved å finne det i oppgavelinjen eller ved å trykke `Ctrl + Alt + T`.
2. Kjør følgende kommandoer for å oppdatere programmene på Pien:
    ```shell
    sudo apt update
    sudo apt upgrade
    ```

3. Deretter installer filene som trengs for dette prosjektet:
    ```shell
    sudo apt install openssh-server
    sudo apt install mariadb
    sudo apt install ufw # Brannmur
    ```

4. For å sjekke om programmene er installert, kan du bruke which-kommandoen. Dette vil vise deg hvor programmet er installert:
    ```shell
    which openssh-server
    which mariadb
    which ufw
    ```

## Sett opp brannmur

1. Start brannmuren for å sikre at endringene dine blir brukt:
    ```shell
    sudo ufw enable
    ```

2. Velg hvilke porter som skal være åpne. I ditt tilfelle vil dette være portene for SSH og databasen:
    ```shell
    sudo ufw allow 22/tcp # SSH
    sudo ufw allow 3306/tcp # MariaDB
    ```

## Koble til Pi med SSH

Hvis du vil bruke Raspberry Pien uten å måtte koble den til en skjerm, kan du bruke SSH. Dette lar deg bruke terminalen til Pien fra en annen datamaskin.

1. Start SSH-serveren ved oppstart av Pi:
    ```shell
    sudo systemctl enable ssh
    sudo systemctl start ssh
    ```

2. For å koble til Pien med SSH, må du vite hva IP-adressen er. Skriv inn følgende kommando for å se IPv4-adressen du skal bruke:
    ```shell
    hostname -I # Viser alle aktive IPv4-adresser
    ```

3. Åpne terminalen på PCen du vil bruke for å koble til Raspberry Pien med SSH. Skriv inn følgende:

    ```shell
    ssh brukernavn@ipv4 # Bytt ut 'brukernavn' med ditt Raspberry Pi-brukernavn og 'ipv4' med Raspberry Pi IP-adressen 
    ```
    Du vil bli bedt om å skrive inn passordet for Raspberry Pien. Når du får spørsmål om fingeravtrykket, skriver du "yes".

## Oppsett av database på Pi med SSH

1. Åpne MariaDB med sudo:

    ```shell
    sudo mariadb
    ```

2. Lag en bruker med et passord:
    ```sql
    CREATE USER '[brukernavn]'@'%' IDENTIFIED BY '[passord]'; -- Bytt ut [brukernavn] og [passord] med ønsket brukernavn og passord
    ```

3. Gi denne brukeren tilgang til alle MariaDB-kommandoer:
    ```sql
    GRANT ALL PRIVILEGES ON *.* TO '[brukernavn]'@'%' IDENTIFIED BY '[passord]'; -- Bytt ut [brukernavn] og [passord]
    FLUSH PRIVILEGES;
    ```

4. Logg ut av MariaDB ved å skrive:
    ```sql
    exit
    ```

5. Logg inn med den nye MariaDB-brukeren:
    ```shell
    mariadb -u [brukernavn] -p # Bytt ut [brukernavn]
    ```
    Skriv inn passordet til brukeren.

6. Nå som du er logget inn, kan vi sette opp databasen:
    ```sql
    CREATE DATABASE telefonkatalog; -- Lager telefonkatalog-databasen
    USE telefonkatalog; -- Bruk den nye databasen

    -- Lag tabellen hvor du legger inn data
    CREATE TABLE person (
        id INT NOT NULL AUTO_INCREMENT,
        fornavn VARCHAR(255) NOT NULL,
        etternavn VARCHAR(255) NOT NULL,
        telefonnummer CHAR(8),
        PRIMARY KEY (id)
    );

    -- Legg inn testdata i tabellen
    INSERT INTO person (fornavn, etternavn, telefonnummer) VALUES ('Erik', 'Perik', '12345678');
    INSERT INTO person (fornavn, etternavn, telefonnummer) VALUES ('Lise', 'Pise', '22334455');
    INSERT INTO person (fornavn, etternavn, telefonnummer) VALUES ('Testus', 'Jensen', '11114444');
    INSERT INTO person (fornavn, etternavn, telefonnummer) VALUES ('Knut', 'Donald', '31415926');
    ```

## Sett opp telefonkatalog.py med tilgang til database
Last ned telefonkatalog.py som ligger i GitHub repositoriet, ellers kan du laget det selv:

1. Lag en ny Python-fil hvor som helst på PCen din. Høyreklikk og velg ny, deretter tekst dokument. Endre navnet på filen til telefonkatalog.py.

2. Høyreklikk på telefonkatalog-filen og velg rediger med Notepad.

3. Skriv inn følgende kode i telefonkatalog.py:

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

Nå skal du ha en telefonkatalog med en fungerende database og mulighet til å legge til og søke opp personer!