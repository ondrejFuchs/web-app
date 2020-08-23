# web-app

## Practical assignment:
Remember to take notes and document your process. You could also see if some of these tasks are easily done with the AWS CLI.

It’s okay to use the default VPC in AWS, that way you can save time.

1. In a language of your choice, make a simple web app that connects to a database (MySQL or PostgreSQL) and does the following:

  * Reads the hostname, database name, username and password from
environment variables (i.e. DB_HOSTNAME, DB_NAME, DB_USERNAME, DB_PASSWORD) at startup.
  * When the application receives a request at /, return “Hello {word from the
database}” to the user. The word can be anything; “World”, your name, etc.
To do the setup of the database, create a script that creates a table and inserts the word you have chosen, let the script use the DB_HOSTNAME/NAME/USERNAME/PASSWORD environment variables.

2. Make a Docker image with your application and the setup script

  * Where all requests are logged to stdout during runtime

3. In AWS

  * Setup a hosted database server in your VPC
  * Upload your Docker image to ECS
  * Setup a ECS Fargate service that runs your Docker image, where the application connects to the database server.
  * Run the setup script as a task in ECS, and populate the database server with data.
  * Ensure that the application is reachable over HTTP from the outside
  * Setup a ALB in front of the server, with HTTPS