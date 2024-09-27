

# Självutvärdering


## Utmaningar du haft under arbetet samt hur du hanterat dem

Det har varit roligt att få allt att fungera. Jag hade dock, som vanligt, större planer för vad det centrala textbearbetningsskriptet skulle göra, men jag fick justera mina ambitioner och istället fokusera på att få testerna, loggningen och flödet att fungera som de skulle.

Jag jobbade i WSL och det var en utmaning att få skripten att köras automatiskt i Windows Task Scheduler. Jag förstår att det finns andra och bättre sätt att köra Linux-filer än genom Task Scheduler, men jag hann inte undersöka det närmare. Lösningen blev att jag skapade en något reducerad version av main.py-filen (main_windows.py), som inte importerar modulen load_från_repo.py, men hanterar texter från ett katalog som är laddad ner via ett shell-skript från kbs repository.

En annan utmaning var att avgöra vad jag skulle logga till en loggfil och vad som var viktigt att testa. Det var utmanande, men också kul.


## Vilket betyg du anser att du skall ha och varför

Programmet kan köras automatiskt, data laddas ner (i Linux-versionen av main.py), bearbetas genom ett textbearbetningsskript och sparas slutligen i en SQLite-databas.

Jag har försökt kommentera koden tydligt, ge funktionerna beskrivande namn och hålla koden enkel så att det är lätt att förstå vad som händer. Jag har också skrivit tester med pytest för skripten och loggningsmeddelandena. Därför anser jag att jag har uppfyllt kraven för att få VG.


## Något du vill lyfta fram till Linus och Antonio?

Tack för en bra kurs och en bra bok. Jag fick ut mycket av både lektionerna, att läsa boken och att genomföra projektet. Jag skulle gärna vilja få feedback på hur jag kan förbättra koden och strukturen.


##Något du vill lyfta fram till Linus och Antonio?

Tack för en bra kurs och en bra bok. Jag fick ut mycket av både lektionerna, att läsa boken och att genomföra projektet. Jag skulle gärna vilja få feedback på hur jag kan förbättra koden och strukturen.