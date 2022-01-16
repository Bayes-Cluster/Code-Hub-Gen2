# Code-Hub-Gen2


## Tech Stack

 * Frontend: [Bootstrap5](https://getbootstrap.com/)
    * Data Dashboard: [Chart.js](https://www.chartjs.org/)
 * Backend: [Flask](https://flask.palletsprojects.com/en/2.0.x/)
 * Database: [MariaDB](https://mariadb.org/)

## Components

Basically, the Code-Hub has(will have) these three main components:

1. Authentication and Authorization
    1. *account application form* collection
    2. Single Sign ON (OpenLDAP + JWT)
    3. Time-based One-Time Password
    3. Ticket System
2. Cluster Monitoring
    1. Server current usage and historical usage
    2. Auditing
    3. Auto Blocking (Crypto-mining and etc.)
3. Web-based Coding Interface
    1. Web Terminal
    2. Files Management
    2. Proxy Service (for `code-server`, `matlab`, `RStudio`, and etc.)