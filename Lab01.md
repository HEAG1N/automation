# IW01: Scrierea unui script shell simplu pentru automatizarea sarcinilor

Obiectiv

Învațăm să cream și să executam scripturi Shell simple pentru a automatiza sarcini de rutină în sistemul de operare Linux.

# Ce Face Scriptul disk_usage.sh?

Acest script este un instrument automatizat pentru a monitoriza spațiul pe disc utilizat de un anumit director (folder).

Pe scurt, el face trei lucruri:

    Calculează cât spațiu (în Megabytes) ocupă directorul specificat.

    Înregistrează (scrie) această informație într-un fișier-jurnal numit disk_usage.log.

    Trimite o alertă pe e-mail dacă spațiul ocupat depășește un anumit prag procentual (de exemplu, 80%).

# Cum Funcționează

Să analizăm cele mai importante părți din scriptul disk_usage.sh.

1. Preluarea Argumentelor

Scriptul are nevoie de cel puțin două argumente pentru a funcționa: calea către director și dimensiunea maximă permisă. Al treilea argument (pragul) este opțional.

 Verificarea argumentelor obligatorii: Scriptul verifică mai întâi dacă a primit cel puțin două argumente. Dacă nu, afișează o eroare și se oprește.
    Bash

if [ "$#" -lt 2 ]; then
    echo " Error: Missing required arguments."
    exit 1
fi

Atribuirea argumentelor: Primul argument este calea, al doilea este dimensiunea maximă. Pentru al treilea (pragul), dacă nu este specificat, i se atribuie valoarea implicită de 80.
Bash

    MONITOR_DIR="$1"
    MAX_SIZE_MB="$2"
    THRESHOLD=${3:-80}

2. Calcularea Spațiului Utilizat

Aceasta este comanda cheie care măsoară dimensiunea directorului.

    Comanda du: Se folosește comanda du -sm pentru a calcula dimensiunea totală (-s) în Megabytes (-m). cut -f1 extrage doar valoarea numerică.
    Bash

CURRENT_USAGE_MB=$(du -sm "$MONITOR_DIR" | cut -f1)

Calcularea procentajului: După ce are dimensiunea curentă, scriptul folosește o formulă matematică simplă pentru a calcula procentajul de spațiu ocupat.
Bash

    USAGE_PERCENT=$((CURRENT_USAGE_MB * 100 / MAX_SIZE_MB))

3. Înregistrarea în Jurnal (Log)

Scriptul creează un mesaj detaliat și îl adaugă la sfârșitul fișierului disk_usage.log.

 Comanda echo >>: Data și ora curentă sunt adăugate la mesaj, iar operatorul >> asigură că informația este adăugată la fișier fără a șterge conținutul anterior.
    Bash

    LOG_FILE="disk_usage.log"
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    LOG_MESSAGE="[$TIMESTAMP] Directory '$MONITOR_DIR' is using $CURRENT_USAGE_MB MB of $MAX_SIZE_MB MB ($USAGE_PERCENT%)."

    echo "$LOG_MESSAGE" >> "$LOG_FILE"

4. Verificarea Pragului și Trimiterea Alertei

La final, scriptul compară procentajul calculat cu pragul stabilit.

    Condiția if: Dacă procentajul utilizat ($USAGE_PERCENT) este mai mare (-gt) decât pragul ($THRESHOLD), atunci se compune și se trimite un e-mail de avertizare folosind comanda mail.
    Bash

    if [ "$USAGE_PERCENT" -gt "$THRESHOLD" ]; then
    echo "Warning: Disk usage ($USAGE_PERCENT%) has exceeded the threshold of $THRESHOLD%."

    EMAIL_SUBJECT="Disk Usage Alert for $MONITOR_DIR"
    EMAIL_BODY="Warning: The directory '$MONITOR_DIR' is using $USAGE_PERCENT% of its allocated space..."

    echo -e "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "$ADMIN_EMAIL"
    fi

# Exemple de Utilizare

Introducem adresa de email.

<img width="974" height="89" alt="image" src="https://github.com/user-attachments/assets/c5ee860c-8911-4c6d-bc12-1fe6941a6fe6" />

Pentru a rula scriptul, mai întâi trebuie să-l faci executabil cu comanda: chmod +x disk_usage.sh

<img width="774" height="48" alt="image" src="https://github.com/user-attachments/assets/e6bdd3ba-ec73-4e2a-aa60-39eef591038f" />\

Monitorizăm directorul /var/log, care are o limită alocată de 500 MB. Scriptul va trimite o alertă dacă se ocupă mai mult de 80% din această valoare (400 MB).

<img width="974" height="148" alt="image" src="https://github.com/user-attachments/assets/6fde6fd3-0f9e-4d6b-a306-9d458f34e752" />

# Concluzii
În cadrul acestei lucrări practice, a fost dezvoltat cu succes un script shell (disk_usage.sh) capabil să automatizeze o sarcină esențială de administrare a sistemelor Linux: monitorizarea spațiului pe disc.

Obiectivul principal a fost atins prin implementarea unui script funcțional care îndeplinește următoarele sarcini:

Prelucrează argumente din linia de comandă, inclusiv argumente obligatorii (directorul și dimensiunea maximă) și opționale (pragul de alertă).

Utilizează comenzi standard Linux (du, cut, date) pentru a colecta și prelucra date în mod eficient.

Implementează logică condițională (if) pentru a evalua starea sistemului și a lua decizii, cum ar fi trimiterea unei alerte pe e-mail.

#Surse

https://www.tldp.org/

 https://www.gnu.org/software/bash/manual/
