import boto3
import datetime
import os
import psycopg2

# Get the database connection details from environment variables
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT', 5432)

def is_timestamp_less_than_two_days_old(timestamp):
    current_time = datetime.datetime.utcnow()
    timestamp_time = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    delta = current_time - timestamp_time
    return delta < datetime.timedelta(days=2)
    
def lambda_handler(event, context):
    
    # Create a CloudFormation client
    client = boto3.client('cloudformation')

    # Identify the cloudfront custom domain stacks using the description
    stack_description = 'Publitas AWS CloudFormation Template for custom domain CloudFront distribution setup'

    # Call the describe_stacks() method to get the stack details
    response = client.describe_stacks()

    # Store the stack details in a variable called 'stacks'
    stacks = response['Stacks']
    
    group_Id = ""
    customer_domain = ""
    
    # filter stacks based on description and created within the last two days.
    for stack in stacks:
        try:
            if stack['Description'] == stack_description and stack['StackStatus'] == 'CREATE_COMPLETE':
                # check if the stack is created less than two days ago and append to the filtered list.
                if is_timestamp_less_than_two_days_old(creation_time_str):
                    
                    # get the customer domain and groupId form the stack parameters
                    for parameter in stack['Parameters']:
                        if parameter['ParameterKey'] == 'Cidr':
                            group_Id = parameter['ParameterValue']
                        if parameter['ParameterKey'] == 'Tag':
                            customer_domain = parameter['ParameterValue']
                    
                    # write to the database    
                    print("group_ID: {}, customerDomain: {}".format(group_Id, customer_domain))

                    # SQL command to be executed
                    sql = "UPDATE groups SET custom_domain_hostname={}, custom_domain_enabled=True, custom_domain_cloudfront_id='E68O53O6HN10E',custom_domain_supports_https=True where id={};".format(group_Id, customer_domain)

                    try:
                        # Connect to the AWS RDS PostgreSQL database
                        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

                        # Create a cursor object to execute SQL commands
                        cursor = conn.cursor()

                        # Execute the SQL command
                        cursor.execute(sql)

                        # Commit the changes to the database
                        conn.commit()

                        # Close the cursor and database connection
                        cursor.close()
                        conn.close()

                        # Return success message
                        return {
                            'statusCode': 200,
                            'body': 'SQL command executed successfully'
                        }
                    
                    except Exception as e:
                        # Return error message
                        return {
                            'statusCode': 500,
                            'body': 'Error executing SQL command: {}'.format(str(e))
                        }

        except Exception as e:
            print(e)
