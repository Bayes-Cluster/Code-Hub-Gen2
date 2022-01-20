# Code-Hub-Gen2


## Tech Stack

 * Frontend: [Bootstrap5](https://getbootstrap.com/)
    * Data Dashboard: [bokeh](https://docs.bokeh.org/en/2.4.1/index.html)
    * Editor: [Manacco Editor](https://microsoft.github.io/monaco-editor/)
    * Web Terminal: [Xterm.js](https://xtermjs.org/)
 * Backend: [Flask](https://flask.palletsprojects.com/en/2.0.x/)
 * Database: [MariaDB](https://mariadb.org/)

## Components

Basically, the Code-Hub has(will have) these three main components:

1. User Management: Authentication, Authorization and Questioning System
    1. *account application form* collection
    2. Single Sign ON (OpenLDAP + JWT)
    3. Time-based One-Time Password
    3. Ticket System
2. System Security Cluster Status and User (danger operation) Monitoring
    1. Server current usage and historical usage - (optional: [netdata](https://www.netdata.cloud/))
    2. Auditing ([Asciinema](https://asciinema.org/))
    3. Auto Blocking (Crypto-mining and etc.)
3. Web-based Coding Interface
    1. Web Terminal ([Xterm.js](https://xtermjs.org/) with `socketio`) - optional
    2. Files Management (simple upload + download)
    2. Proxy Service (for `code-server`, `MATLAB`, `RStudio`, and etc.)

## Installation

```bash
git clone git@github.com:Bayes-Cluster/Code-Hub-Gen2.git
cd Code-Hub-Gen2
conda creaet -n CodeHub python=3.7
python -m pip install -r requirements.txt
gunicorn --bind 127.0.0.1:5000 run:app
```

For production, we choose MariaDB as the database:

```bash
sudo apt-get update        
sudo apt-get install mariadb-server libmariadb3 libmariadb-dev
python -m pip install mariadb
```

Then create a database called: CodeHub and user codehub:

```bash 
sudo maraidb -u root -p 

CREATE DATABASE CodeHub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'codehub'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON codehub. * TO 'codehub'@'localhost';
FLUSH PRIVILEGES;
```

## Acknowledgement
* <img src="uic.png" alt="BNU-HKBU United International College" width="150"/>
* ![python-version](https://img.shields.io/badge/python-v3.7-blue)
* <img src="https://jwt.io/img/badge-compatible.svg" alt="jwt" width="150"/>
* <img src="images/flask.png" alt="flask" width="150"/>
* <img src="images/mariadb.png.webp" alt="mariadb" width="150"/>