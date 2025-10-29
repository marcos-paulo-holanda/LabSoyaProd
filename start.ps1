docker-compose up --build -d minio postgres
docker-compose up --build -d faostat_ingestor
Start-Sleep -Seconds 70
docker-compose up --build -d model_features
Start-Sleep -Seconds 5
docker-compose up --build -d model_trainer
