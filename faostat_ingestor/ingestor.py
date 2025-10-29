import os
import requests
import zipfile
import pandas as pd
import boto3
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

"""FAOSTAT Data Ingestor. Esse script baixa dados do FAOSTAT, processa e envia para um bucket MinIO.
"""
class FAOSTATIngestor:
    def __init__(self):
        self.urls = {
            'qcl': 'https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip',
            'rfn': 'https://bulks-faostat.fao.org/production/Inputs_FertilizersNutrient_E_All_Data_(Normalized).zip',
            'et':  'https://bulks-faostat.fao.org/production/Environment_Temperature_change_E_All_Data_(Normalized).zip',
            'ic':  'https://bulks-faostat.fao.org/production/Investment_CreditAgriculture_E_All_Data_(Normalized).zip',
            'oa':  'https://bulks-faostat.fao.org/production/Population_E_All_Data_(Normalized).zip',
            'pp':  'https://bulks-faostat.fao.org/production/Prices_E_All_Data_(Normalized).zip'
        }

        self.minio_endpoint = os.getenv('MINIO_ENDPOINT')
        self.minio_key = os.getenv('MINIO_ACCESS_KEY')
        self.minio_secret = os.getenv('MINIO_SECRET_KEY')
        self.minio_bucket = os.getenv('MINIO_BUCKET')

        self.s3 = boto3.client(
            's3',
            endpoint_url=f'http://{self.minio_endpoint}',
            aws_access_key_id=self.minio_key,
            aws_secret_access_key=self.minio_secret
        )
        self._create_bucket()

    def _create_bucket(self):
        try:
            self.s3.head_bucket(Bucket=self.minio_bucket)
        except:
            self.s3.create_bucket(Bucket=self.minio_bucket)

    def download_and_extract(self, url):
        response = requests.get(url)
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        for file in zip_file.namelist():
            if file.endswith('.csv'):
                with zip_file.open(file) as f:
                    df = pd.read_csv(f, encoding="latin1", dtype={'Value': str}, low_memory=False)
                    return df
        return None

    def process_and_upload(self):
        for key, url in self.urls.items():
            df = self.download_and_extract(url)
            if df is not None:
                buffer = BytesIO()
                df.to_parquet(buffer, index=False)
                buffer.seek(0)
                filename = f"{key}.parquet"
                self.s3.upload_fileobj(buffer, self.minio_bucket, filename)
                print(f"✅ Arquivo {filename} enviado.")
            else:
                print(f"⚠️ Falha ao processar {key}.")

if __name__ == '__main__':
    ingestor = FAOSTATIngestor()
    ingestor.process_and_upload()
