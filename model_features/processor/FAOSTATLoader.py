import boto3
import os
from processor.Features import *

class FAOSTATLoader:
    def __init__(self):
        self.bucket = os.getenv('MINIO_BUCKET', 'raw-data')
        self.minio_client = boto3.client(
            's3',
            endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT', 'minio:9000')}",
            aws_access_key_id=os.getenv('MINIO_ACCESS_KEY', 'minio'),
            aws_secret_access_key=os.getenv('MINIO_SECRET_KEY', 'minio123')
        )
        self.processors = {
            'qcl': SoyaProcessor,
            'rfn': FertilizersProcessor,
            'et': ETProcessor,
            'ic': ICProcessor,
            'oa': OAPopulationProcessor,
            'pp': PricesProcessor,
        }

    def load_dataframe(self, code):
        filename = f"{code}.parquet"
        processor_class = self.processors[code]
        processor = processor_class(self.minio_client, self.bucket, filename)
        processor.executar()
        return processor.df_pivot