\# Containerized Sales Analytics API



A REST API built using Python Flask and PostgreSQL, containerized with Docker and managed using Docker Compose.



\## Features



\- Health check endpoint

\- Create and retrieve sales records

\- Sales summary with total orders, units sold, and revenue

\- PostgreSQL database integration

\- Persistent database storage using Docker volumes

\- Docker Compose service orchestration



\## Tech Stack



\- Python

\- Flask

\- PostgreSQL

\- Docker

\- Docker Compose

\- PowerShell



\## Project Architecture



PowerShell Client → Flask REST API → PostgreSQL Database



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| GET | `/health` | Check API and database connectivity |

| GET | `/sales` | Retrieve sales records |

| POST | `/sales` | Add a sales record |

| GET | `/summary` | Calculate sales metrics |



\## Run the Project



```powershell

docker compose up --build -d

```



Check running services:



```powershell

docker compose ps

```



Test the API:



```powershell

Invoke-RestMethod http://localhost:5000/health

Invoke-RestMethod http://localhost:5000/sales

Invoke-RestMethod http://localhost:5000/summary

```



Stop the project:



```powershell

docker compose down

```



\## Learning Outcomes



\- Building REST APIs with Flask

\- Connecting Python applications to PostgreSQL

\- Containerizing applications with Docker

\- Managing multiple services using Docker Compose

\- Configuring service networking, health checks, and persistent storage



