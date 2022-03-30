# BBC: balancing Content Diversity and Autonomy


this will cause a merge conflict

# Install postgres 

Download [PostgresApp](https://postgresapp.com/downloads.html)

Follow the [Instructions](https://postgresapp.com/) steps.

Warning if you have already installed postgres consider [removing]( removing other PostgreSQL installations) old installations.

After setup install [pgadmin](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v6.7/macos/). This is the most popular graphical user interface for postgres.

After installing postgres make sure your Python interpreter has psycopg2 installed -> `pip install psycopg2`

# Setting Database up

Open pgAdmin and add New Server

![pgAdmin1](markdown_images/pgAdmin1.png)

Name the new server `bbc_recommender_system`

![pgAdmin2](markdown_images/pgAdmin2.png)

Click on Connection and enter `localhost` in Host name/address and `postgres` as Password.

![pgAdmin3](markdown_images/pgAdmin3.png)

In the end, click Save.

Now the database environment was created. Let's create the database we want to interact with.

Now make a right click on `Databases -> Create -> Database...`

![pgAdmin4](markdown_images/pgAdmin4.png)

Call the Database bbc and save.

![pgAdmin5](markdown_images/pgAdmin5.png)

Now everything is set up to work with our project.

Keep in mind I will have the password and all the other stuff in **plain text within the repository**. 
That is something we **!REALLY! do NOT want**! But due to convenience reasons for this project we make an excuse. 

# Database Schema

