# Code-Hub-Gen2


## Tech Stack

 * Frontend: [Bootstrap5](https://getbootstrap.com/)
    * Data Dashboard: [Chart.js](https://www.chartjs.org/) or [Plotly](https://plotly.com/)
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
