# Raport Laborator nr. 3: Automatizarea Scripturilor cu Cron

# Obiectiv

Învățați cum să configurați planificatorul de activități (cron) pentru automatizarea execuției scripturilor.

# Pregătire

Această temă se bazează pe lucrarea de laborator nr. 2. Copiați fișierele din lucrarea de laborator nr. 2 într-un nou director lab03 pentru lucrări ulterioare.

# Structura Proiectului și Scopul Fiecărui Fișier

Proiectul lab03 este organizat în următoarea structură de fișiere, fiecare având un rol specific:

    docker-compose.yml: Fișierul principal de orchestrarare. Acesta definește, configurează și leagă cele două servicii ale aplicației: api_server și cron_runner.

    Dockerfile: Conține setul de instrucțiuni pentru a construi imaginea Docker personalizată pentru serviciul cron_runner. Acesta instalează sistemul de operare de bază, Python, cron și dependențele necesare.

    cronjob: Un fișier text care conține definițiile sarcinilor ce trebuie executate automat de cron. Aici sunt specificate periodicitatea, utilizatorul și comanda pentru fiecare sarcină.

    entrypoint.sh: Un script shell care se execută la pornirea containerului cron_runner. Acesta pregătește mediul (de exemplu, exportă variabilele de mediu pentru cron) și pornește serviciul cron în prim-plan.

    currency_exchange_rate.py: Scriptul Python care este executat de cron. Acesta extrage ratele de schimb valutar de la api_server și salvează rezultatele într-un fișier JSON.

    app/ și data.json: Acestea conțin codul sursă și datele pentru serviciul api_server, moștenite din laboratorul nr. 2.

    data/: Directorul (creat automat) în care scriptul currency_exchange_rate.py salvează fișierele JSON cu ratele de schimb obținute.

    .env: Fișier de configurare pentru variabilele de mediu, cum ar fi API_KEY, utilizat de ambele servicii.

# Cum se Construiește și se Rulează Containerul

Pentru a construi imaginea Docker și a rula containerele, urmați acești pași:

    Asigurați-vă că Docker și Docker Compose sunt instalate pe sistemul dumneavoastră.

    Navigați în terminal în directorul rădăcină al proiectului lab03.

    Asigurați-vă că fișierul .env există și conține cheia API necesară.

    Rulați următoarea comandă:
    Bash

docker-compose up --build -d

<img width="974" height="411" alt="image" src="https://github.com/user-attachments/assets/9ccace5a-dfa0-4529-b745-c3395b26fc2b" />

    Opțiunea --build forțează Docker să reconstruiască imaginea pentru cron_runner, asigurând că orice modificare adusă fișierelor (Dockerfile, cronjob, entrypoint.sh) este aplicată.

    Opțiunea -d (detached) pornește containerele în fundal, lăsând terminalul liber.
    
# Cum se Verifică Execuția Sarcinilor Cron

Verificarea Fișierului de Log

Ieșirea standard și erorile fiecărei comenzi cron sunt redirecționate către fișierul /var/log/cron.log în interiorul containerului cron_runner.

Pentru a vizualiza log-urile în timp real (atât de la cron, cât și de la script), puteți folosi comanda:
Bash

docker-compose logs --follow cron_runner

<img width="1280" height="99" alt="image" src="https://github.com/user-attachments/assets/c71e61dd-de62-4914-ae24-89e2ce4b8a02" />

# Concluzii

În cadrul acestui laborator, am învățat cu succes cum să configurez și să utilizez serviciul cron într-un mediu containerizat Docker pentru a automatiza sarcini repetitive. Am dezvoltat abilități practice în crearea de imagini Docker personalizate folosind un Dockerfile, orchestratea serviciilor cu docker-compose.yml și definirea corectă a sarcinilor programate.

Procesul de depanare (debugging) a scos în evidență provocări comune în lucrul multi-platformă (Windows-Linux), cum ar fi importanța formatului sfârșitului de linie (LF vs. CRLF) și sintaxa specifică fișierelor de configurare cron din directorul /etc/cron.d/, care necesită specificarea unui utilizator pentru fiecare comandă.

Proiectul final este un sistem funcțional și robust, capabil să execute automat scripturi la intervale de timp predefinite, demonstrând o înțelegere solidă a conceptelor de automatizare și containerizare.

# Surse Bibliografice

Pentru realizarea acestui laborator, au fost consultate implicit documentațiile oficiale ale tehnologiilor utilizate:

Docker Documentation: Pentru sintaxa Dockerfile și docker-compose.yml.
 https://docs.docker.com/

Cron (Manual Pages): Pentru sintaxa și configurarea sarcinilor cron.
https://man7.org/linux/man-pages/man5/crontab.5.html

Python Documentation: Pentru informații legate de limbajul de programare Python.
https://docs.python.org/3/
