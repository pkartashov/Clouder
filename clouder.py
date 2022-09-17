import unittest
import pytest
import api
import dataio
import requests
import boto3
from google.cloud import functions_v1
from google.cloud import datastore
from google.cloud import storage
from azure.storage.file import ContentSettings
from azure.storage.file import FileService
from azure.data.tables import TableClient
from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode

class Clouder:
    CloudName =""
    def __init__(self, name):
        self.name = name

    def run_cloud_function (self):
        pass
    def query_cloud_data(self):
        pass
    def save_cloud_data(self):
        pass
    def create_cloud_data_item(self):
        pass
    def delete_cloud_data_item(self):
        pass
    def upload_cloud_file(self):
        pass
    def download_cloud_file(self):
        pass
    def __str__(self):
        return self.name


class AWS_tester (Clouder):
    def __init__(self, length):
        super().__init__("AWS_tester")
        self.cloud_settings_json = cloud_settings_json

    def run_cloud_function (func_name)
        lambda_client = boto3.client('lambda')
        response = lambda_client.invoke(FunctionName=func_name,
                         InvocationType='RequestResponse', #'Event'|'RequestResponse'|'DryRun',
                         LogType='Tail', #'None'|'Tail',
                         ClientContext='string',
                         Payload=b'bytes',
                         Qualifier='string')
        return response['Payload'].read().decode("utf-8")

    def query_cloud_data(table_name, key_id, region):
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(table_name)
        response = table.query(
            KeyConditionExpression=Key(key.ide).eq(1)
        )

        return response

    def create_cloud_data_item (table_name, item_json, region):
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(table_name)
        response = table.put_item(item_json)
        return response

    def update_cloud_data_item (table_name, key_json, update_expression, values_json, region):
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(table_name)
        response = table.update_item(key_json,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=values_json,
        ReturnValues = "UPDATED_NEW"
        )
        return response

    def delete_cloud_data_item(table_name, key_val_json, region, key_val_json):
        dynamodb = boto3.resource('dynamodb', table_name, key_val_json, region_name=region)
        table = dynamodb.Table(table_name)
        response = table.table.delete_item(Key=key_val_json)
        return response

    def upload_cloud_file (bucket_name, file_path_from, to_cloud_file_name)
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(file_path_from, bucket_name, to_cloud_file_name)

    def download_cloud_file (bucket_name, file_path_to, cloud_file_name_from)
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(bucket_name, cloud_file_name_from, file_path_to)

class GCP_tester (Clouder):
    def __init__(self, length):
        super().__init__("GCP_tester")
        self.cloud_settings_json = cloud_settings_json

    def run_cloud_function (func_name_value, func_data_value)
        gcp = functions_v1.CloudFunctionsServiceClient()
        request = functions_v1.CallFunctionRequest(func_name_value, func_data_value)
        response = gcp.call_function(request=request)
        return response

    def query_cloud_data(table_name, key_id, key_val):
        gcp = datastore.Client()
        key = gcp.key(key_id, key_val)
        task = gcp.get(key)

        return task

    def create_cloud_data_item (table_name, item_json):
        gcp = datastore.Client()
        with gcp.transaction():
            incomplete_key = gcp.key("Task")
            task = datastore.Entity(key=incomplete_key)
            task.update(item_json)
            gcp.put(task)
        return task

    def update_cloud_data_item (self, table_name, key_id, key_val):
        gcp = datastore.Client()
        with gcp.transaction():
            key = gcp.key(key_id, key_val)
            task = gcp.get(key)
            task["done"] = True
            gcp.put(task)
        return task

    def delete_cloud_data_item(table_name, key_id, key_val):
        gcp = datastore.Client()
        key = gcp.key(key_id, key_val)
        gcp.delete(key)
        return 0

    def upload_cloud_file (bucket_name, source_file_name, destination_blob_name)
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
        except Exception as e:
            print(e)

    def download_cloud_file (bucket_name, destination_file_name, source_blob_name)
        try:
            storage_client = storage.Client()

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
        except Exception as e:
            print(e)

class Azure_tester (Clouder):
    def __init__(self, length):
        super().__init__("Azure_tester")
        self.cloud_settings_json = cloud_settings_json

    def run_cloud_function (self, func_url)
        return requests.get(func_url)

    def query_cloud_data(connection_string, table_name, query_filter):
        table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
        items_json = table_client.query_entities(query_filter)
        return items_json

    def create_cloud_data_item (connection_string, table_name, item_json):
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        table_client = table_service_client.get_table_client(table_name=table_name)
        item = table_client.create_entity(entity=item_json)

        return item


    def update_cloud_data_item(connection_string, table_name, entity_json):
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        table_client = table_service_client.get_table_client(table_name=table_name)
        insert_entity = table_client.upsert_entity(mode=UpdateMode.REPLACE,
                                                   entity=entity_json)  # e.g. entity_json = {"PartitionKey": "color2","RowKey": "sharpie","text": "Marker","price": 7.99,}
        return insert_entity

    def delete_cloud_data_item(connection_string, table_name, row_key_id, partition_k ):
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        table_client = table_service_client.get_table_client(table_name=table_name)
        item = table_client.delete_entity(row_key=row_key_id, partition_key=partition_k)
        return item

    def upload_cloud_file (account_name, account_key, share_name, source_file_path, destination_file_name)
        try:
            file_service = FileService(account_name=account_name, account_key=account_key)
            file_service.create_file_from_path(
                share_name,
                None,
                destination_file_name,
                source_file_path)
        except Exception as e:
            print(e)

    def download_cloud_file (account_name, account_key, share_name, source_file_name, destination_file_path)
        try:
            file_service = FileService(account_name=account_name, account_key=account_key)
            file_service.get_file_to_path(
                share_name,
                None,
                source_file_name,
                destination_file_path)
        except Exception as e:
            print(e)

class SuiteBuilder:

    @staticmethod
    def _build ():
        return ("build")

    @staticmethod
    def deploy ():
        return ("deploy")

    @staticmethod
    def _run ():
        return ("run")

    @staticmethod
    def _ignore ():
        return ("ignore")

    @staticmethod
    def _retry ():
        return ("retry")

    @staticmethod
    def _pause ():
        return ("pause")

    @staticmethod
    def _restart_override ():
        return ("restart_overrid")

    @staticmethod
    def _restart_append ():
        return ("restart_append")




class TestClass(unittest.TestCase):

    def setUp(self):
        self.test_data = dataio.get_test_data_arr("TestData.xsls", "data", 0)

        self.clouds_in_test = ['gcp', 'aws', 'azure']
        cloud_settings_json = {"key1": "val1"}
        if self.clouds_in_test[0] in clouds_in_test:
            GCP_tester(cloud_settings_json)
        if self.clouds_in_test[0] in clouds_in_test:
            AWS_tester(cloud_settings_json)
        if self.clouds_in_test[0] in clouds_in_test:
            Azure_tester(cloud_settings_json)

    #Run GCP function, obtain its result and save the result into AWS dynamodb.
    #Verify inserted data equals to GCP fuction output
    def test_gcp_function_inserts_data_to_aws(self):
        a = GCP_tester.run_cloud_function("my_gcp_function", "param=2")
        item = AWS_tester.create_cloud_data_item("my_table", a, "US-East")
        assert AWS_tester.query_cloud_data("my_table", item, "US-East") == a

    #Upload file to both AWS and Azure cloud
    #Download files from both clouds and verify they are the same
    def test_azure_aws_file_upload_synch(self):
        Azure_tester.upload_cloud_file("key=azure_key", "root", "documents/server-log-02022021.txt", "server-log-02022021.txt")
        AWS_tester.upload_cloud_file("bucket0", "documents/server-log-02022021.txt", "server-log-02022021.txt")
        azure_file = "documents/server-log-02022021_azure.txt"
        Azure_tester.download_cloud_file("key=azure_key", "root", "server-log-02022021.txt", azure_file)
        aws_file = "documents/server-log-02022021_aws.txt"
        AWS_tester.download_cloud_file("bucket0", "server-log-02022021.txt", aws_file)

        f1 = open(azure_file, 'r')
        f2 = open(aws_file, 'r')
        f1_l = f1.readlines()
        f2_l = f2.readlines()
        match=True
        for i in range(len(f1_l)):
            if f1_l[i] != f2_l[i]:
                match = False

        f1.close()
        f2.close()
        assert match==True


    def tearDown(self):
        self.testdata = []

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestClass('test_gcp_function_inserts_data_to_aws'))
    suite.addTest(TestClass('test_azure_aws_file_upload_synch'))

    return suite

cloud_settings_json={}
clouds_in_test = ['gcp', 'aws', 'azure']
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())