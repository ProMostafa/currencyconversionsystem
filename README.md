## Currency Conversion System
System that allows a partner to integrate with in order to get the conversion rate between 
currencies that supported with system

## Currency Conversion System requirements (suppose it some characteristics that effect design)
### should be take into considerations this aspects in system
1. system can set supported currencies that customers used to conversions
2. system save exchange rates updated for futures reports and analytics
3. system restrictions on data consistency
4. should be balance between data storage and system performance when integrate with high intensity exchange rates API
5. handel periodic task failure very trick and work with this careful and handle most scenarios that can make this tasks fails
6. which broker should be selected in this project use redis instead of rabbitmq cause of some factors
7. build strong retries mechanism if we integrate with 3 part through restFul APIs **(not implement)**
8. build cashe mechanism for system performace **(not implement)**
9. build logs mechanism for catch and debugging future errors **(not implement)**

## technologies
1. django and django rest framework
2. postgreSQL
3. redis
4. celery
5. celery beat
6. swagger
7. docker 
8. docker compose 

## Currency Conversion System features
1. authentication and authorization with JWT
2. Can add/delete/update currencies that system will supported
3. Exchanges rate updates always up to date periodical based on integration updates
4. Currency Conversion operation 
5. Conversion status update periodical
6. Customer history data
7. Dashboard for monitoring background tasks 

## Feature help people to use project easily without need to configure any data
1. Add fixtures to pre-populate database with data to provide some initial data any easy use project **(not implement)**

## project layout structure
use **two-tier** approch try to follow **separation of concerns principle** like<br>
<respository_root>/<br>
-----<configuration_root>/<br>
-----<django_project_root>/<br>
-----files/<br>
-----requirement.txt/<br>
### Top level: Repository Root
directory is the absolute root directory of project 
That contains high-level files that are requied for deployment & running project

### Second Level: Django Project Root
directory that contains django applications.

### Second Level: Configuration Root
directory that contains settings module and configuration files.
By follow separation of concerns principle this has more benefits for example in scale project and make deployment easy and more

## postgresql
main project database

## redis
use redis in two usecase 
1. Using as Broker for celery
1. implement simple cache mechanism (later)
2. using redis lock to prevent race condition (if occurrence later)

## celery
use for backgroud task

## celery beat
use for periodical background tasks

## flower
use for monitoring background tasks

## docker & docker compose 
for isoluate project and its dependencies and build identical environment that can work on any device or clould that install docker and docker compose tools

## swagger
use for document APIs

## use test driven development (TDD) in development
Add simple unit test just example not all use case for conversion operation that cover simple use case

## Now can go to installation guide [link](https://github.com/ProMostafa/currencyconversionsystem/blob/main/installation_guide.md)