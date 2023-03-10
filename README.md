# publistas-assignment

Implementation Plan:

I have come up with two approaches to automating this task. 
Approach-1: 
The approach works within the confines of the accesses and restriction given for the tasks and automates the periodical parsing of stacks created within the last 2 days and updating the RDS database with the custom domain names and group IDs created within last two days.
1.	Write a lambda function that implements the logic below:
a.	Use the boto3 SDK to describe the cloudformation stacks
b.	Filter the stacks based on Stack Creation Status, Description and Creation Time to identify recently created Cloudfront distribution stacks.
c.	Retrieve the custom domain name and group id from the stack parameters and write to the RDS Database.
d.	Schedule the lambda function to run every 2 days with Cloudwatch events Cron.
   This approach is a direct automation of the manual approach currently being used. With the major limitation being that a separate clean up logic/lambda function would have to be written to clean up the database when customers/cloudfront distributions are deleted.
   
Installing dependencies and packaging the lambda code.
a. Open a command prompt and create a my-sourcecode-function project directory. For example
   mkdir my-sourcecode-function
b. Navigate to the my-sourcecode-function project directory
   cd my-sourcecode-function
c. Download the lambda_function_approach1.py into the project directory
d. Create a directory 'package' in the project directory 
e. Download the psycopg2 from  into the package directory from https://github.com/jkehler/awslambda-psycopg2 
f. zip -r ../my-deployment-package.zip . This generates a my-deployment-package.zip file in your project directory.
g. Add the lambda_function_approach1.py to the zip file.
h. zip my-deployment-package.zip lambda_function_approach1.py
i. Create a lambda function using the zip package.
j. Setup a cloudwatch events cron job that runs the lambda function every two days.

Approach-2:
This approach seeks to leverage cloudformation custom resource feature but requires modifying the cloudformation template used to provision the cloudfront distribution to include a lambda backed custom resource like so.
1.	Modify the cloudformation template to include a lambda backed custom resource. Using the dependsOn attribute to ensure that the cloudfront distribution is successfully created before the lambda custom resource is triggered.
2.	Write the backing lambda function to read the event type (Create or Delete) and parameters from the cloudformation stack and Update/Delete from the RDS Database as required.
This is a somewhat elegant approach as updating the database and cleaning up can be implemented using the same lambda function.

Installing dependencies and packaging the lambda code.
a. Open a command prompt and create a my-sourcecode-function project directory. For example
   mkdir my-sourcecode-function
b. Navigate to the my-sourcecode-function project directory
   cd my-sourcecode-function
c. Download the lambda_function_approach1.py into the project directory
d. Install the urllib3 dependency into the package directory 
   pip install --target ./package urllib3
e. Download the psycopg2 from  into the package directory from https://github.com/jkehler/awslambda-psycopg2 
f. zip -r ../my-deployment-package.zip . This generates a my-deployment-package.zip file in your project directory.
g. Add the lambda_function_approach1.py to the zip file.
h. zip my-deployment-package.zip lambda_function_approach1.py
i. Create a lambda function using the zip package.
j. Use the modified_cf_template.yaml to crate the Cloudfront distribution.
