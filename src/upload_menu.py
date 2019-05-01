import boto3
import pandas as pd
from decimal import *

session = boto3.Session(aws_access_key_id='XXXX',     aws_secret_access_key='XXXX', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('Trucks')
number_records = table.item_count;

truck_data = pd.read_csv('../data/menu.csv')




with table.batch_writer() as batch:
	for x in truck_data.index:
		item = {
		'Truck_Name':truck_data.loc[x,'Truck'],
		'Index':number_records,
		'Food':truck_data.loc[x,'Food'],
		'Price':Decimal(truck_data.loc[x,'Price'])
		}

		batch.put_item(Item=item)
		number_records += 1