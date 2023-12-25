# TechPoint

TechPoint is the ultimate solution for supply chain and electronics
manufacturing management. It's the smart way to transform your supply chain
and achieve competitive advantage.

## Installation

### Pre-requisites

To install TechPoint make sure that you already have Docker and Docker Compose
installed on your local machine.
Check out docker documentation to install:
- Docker: https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

### Clone the repository to your local machine

`git clone https://github.com/AndrewYatskevich/tech-point.git`

### Move to the root folder of the project

`cd tech-point/`

### Create the .env file and fill it out

- Create the .env file `touch .env`
- Fill out the .env file by referring to .env.example

### Run Docker Compose to spin up the application

`docker compose -f docker-compose.yaml up -d`

## Usage

The application is available on 0.0.0.0:8000 host.
The following functionality has been implemented:
- API Token authentication
- Admin panel for managing project data and performing administrative tasks
- CRUD operations with supply chains and links
- Ability to filter data based on address or products

## Features

The following features have been implemented:
- Automatic generation of fake data for testing
- Background tasks to change data and send emails

## License
MIT © [Andrew Yatskevich](https://github.com/AndrewYatskevich)
