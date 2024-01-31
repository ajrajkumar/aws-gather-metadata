import boto3
import json

def main():

    # Getting the account name

    client = boto3.client("sts")
    response = client.get_caller_identity().get('Account')
    account_id=response
    client = boto3.client("organizations")
    response = client.describe_account(AccountId=account_id)
    account_name = response['Account']['Name']

    with open("region.lst") as fp:
        region_list = fp.readlines()

    for region in region_list:
        client = boto3.client("rds",region_name = region.strip())
        response = client.describe_db_instances()
        for db in response['DBInstances']:
            env=None
            for tag in db['TagList']:
               if tag['Key'] == 'Env' :
                   env = tag['Value']

            print("{},{},{},{},{},{},{},{}".format(account_id, account_name, region.strip(),db['DBInstanceIdentifier'], db['Endpoint']['Port'], db['Engine'], db['MasterUsername'],env))

if __name__ == "__main__":
    main()
