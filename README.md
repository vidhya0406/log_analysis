### Log Analysis

## Project Overview
The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

## Steps to setup the project


#### Installing dependencies

- Install [Vagrant](https://www.vagrantup.com/)
- Install [VirtualBox](https://www.virtualbox.org/)
- Download the vagrant setup files from [Udacity's Github](https://github.com/udacity/fullstack-nanodegree-vm)

These files configure the virtual machine and install all the tools needed to run this project.

- Download the database setup: [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- Unzip the same to get the newsdata.sql file.
- Put the newsdata.sql file into the vagrant directory. This will automatically be available inside the virtual machine.
- Download this project in the vagrant directory

#### In VM:

- Navigate to the directory that has the `vagrant` file.
- ``` vagrant up ``` to build the VM. (Required only during the first run)
- ``` vagrant ssh ``` to connect.
- ``` cd /vagrant/log_analysis ```
- ``` psql -d news -f newsdata.sql ``` to load the data.
- ``` python log_analysis.py```



## Views created to make query easier
```
CREATE VIEW requests AS
SELECT time::date AS day, count(*)
            FROM log
            GROUP BY time::date
            ORDER BY time::date;

create view errors as
SELECT time::date AS day, count(*)
                FROM log
                WHERE status != '200 OK'
                GROUP BY time::date
                ORDER BY time::date;

CREATE VIEW err_rate AS
SELECT requests.day,
        errors.count::float / requests.count::float * 100
        AS percentage
    FROM requests, errors
    WHERE requests.day = errors.day;
```
