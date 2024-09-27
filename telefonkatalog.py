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
