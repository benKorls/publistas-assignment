import json
import urllib.request
import psycopg2
import boto3


# Send response to the pre-signed S3 URL
def send_response(event, context, response_status, response_data):
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": response_data
    })

    print("RESPONSE BODY:\n", response_body)

    headers = {
        "content-type": "",
        "content-length": str(len(response_body))
    }

    request = urllib.request.Request(event["ResponseURL"], method="PUT", headers=headers, data=response_body.encode())
    with urllib.request.urlopen(request) as response:
        print("STATUS: " + str(response.getcode()))
        print("HEADERS: " + str(response.info()))

    # Tell AWS Lambda that the function execution is done
    context.done()


def lambda_handler(event, context):
    print("REQUEST RECEIVED:\n" + json.dumps(event))

    # For Delete requests, delete the entry for the stack being deleted from the database.
    if event["RequestType"] == "Delete":
        
        # Get groupId from the event object
        groupId = event["ResourceProperties"]["GroupId"]

        # prepare the sql statement
        sqlDelete = "DELETE FROM groups WHERE id={}".format(groupId)

        try:
            # Connect to the AWS RDS PostgreSQL database
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()

            # Execute the SQL command
            cursor.execute(sqlDelete)

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
            send_response(event, context, "SUCCESS")
            return

    response_status = "FAILED"
    response_data = {}

    # For Create requests, update the database with the customer domain.
    if event["RequestType"] == "Create":
        
        # Get groupId from the event object
        groupId = event["ResourceProperties"]["GroupId"]
        CustomDomain = event["ResourceProperties"]["CustomDomain"]

        # prepare the sql statement
        sqlCreate = "UPDATE groups SET custom_domain_hostname={}, custom_domain_enabled=True, custom_domain_cloudfront_id='E68O53O6HN10E',custom_domain_supports_https=True where id={}".format(CustomDomain, groupId)

        try:
            # Connect to the AWS RDS PostgreSQL database
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()

            # Execute the SQL command
            cursor.execute(sqlDelete)

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
            send_response(event, context, "SUCCESS")
            return

