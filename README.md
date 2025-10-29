# LabSoya - Sistema de Predição de Produção de Soja

Sistema de Machine Learning para predição de produção de soja utilizando dados do FAOSTAT (Food and Agriculture Organization). O projeto implementa um pipeline completo de dados, desde a ingestão até a geração de previsões, seguindo uma arquitetura de dados em camadas (bronze, silver, gold).

## 📋 Sobre o Projeto

Este projeto é parte de um TCC que visa desenvolver um sistema capaz de prever a produção de soja em diferentes países utilizando técnicas de aprendizado de máquina. O sistema processa dados públicos do FAOSTAT e gera previsões futuras baseadas em features como:

- Área colhida
- Produção histórica
- Rendimento (yield)
- Uso agrícola
- Mudanças de temperatura
- Investimentos em dólares
- População rural
- Preços do produtor

## 🏗️ Arquitetura

O projeto segue uma arquitetura de dados em camadas:

- **Camada Bronze (MinIO)**: Armazenamento dos dados brutos do FAOSTAT em formato Parquet
- **Camada Silver (PostgreSQL)**: Dados processados e features extraídas
- **Camada Gold**: Dados semânticos finais com previsões do modelo

### Componentes

1. **faostat_ingestor**: Baixa dados do FAOSTAT e armazena no MinIO
2. **model_features**: Processa dados brutos e gera features de soja no PostgreSQL
3. **model_trainer**: Treina modelos de ML e gera previsões futuras
4. **powerbi**: Dashboard para visualização dos resultados

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e em execução
- PowerShell (Windows)
- Arquivo `.env` configurado (se necessário)

### Executando o Projeto

No Windows, abra o PowerShell na pasta raiz do projeto e execute:

```powershell
.\start.ps1
```

Este script irá:
1. Iniciar os serviços MinIO e PostgreSQL
2. Executar o ingestor de dados do FAOSTAT
3. Processar as features de soja
4. Treinar o modelo de Machine Learning

### Executando Manualmente com Docker Compose

Se preferir executar manualmente:

```bash
# 1. Iniciar serviços base (MinIO e PostgreSQL)
docker-compose up --build -d minio postgres

# 2. Executar ingestor de dados
docker-compose up --build -d faostat_ingestor

# Aguardar alguns segundos para o ingestor processar os dados...

# 3. Processar features
docker-compose up --build -d model_features

# 4. Treinar modelo
docker-compose up --build -d model_trainer
```

## 📊 Estrutura do Projeto

```
.
├── db/
│   └── init.sql                 # Script de inicialização do banco de dados
├── faostat_ingestor/
│   ├── Dockerfile
│   ├── ingestor.py              # Script de ingestão de dados do FAOSTAT
│   └── requirements.txt
├── model_features/
│   ├── Dockerfile
│   ├── main.py                  # Orquestrador de processamento de features
│   ├── processor/
│   │   ├── BaseProcessor.py
│   │   ├── DatasetBuilder.py
│   │   ├── FAOSTATLoader.py
│   │   └── Features.py
│   ├── queries.py               # Queries SQL para criação de tabelas
│   └── requirements.txt
├── model_trainer/
│   ├── Dockerfile
│   ├── main.py                  # Orquestrador de treinamento do modelo
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── model.py
│   ├── eda.py                   # Análise exploratória de dados
│   ├── pycaret_trainer.py
│   ├── persistence.py
│   ├── eda_outputs/             # Visualizações geradas pelo EDA
│   └── requirements.txt
├── powerbi/
│   └── DASHBOARD.pbix           # Dashboard PowerBI
├── docker-compose.yml           # Configuração dos serviços Docker
└── start.ps1                    # Script de inicialização do projeto
```

## 🔧 Serviços e Portas

- **MinIO Console**: http://localhost:9001
  - Usuário: `minio`
  - Senha: `minio123`
  - Endpoint: `localhost:9000`
- **PostgreSQL**: `localhost:5432`
  - Database: `faostat`
  - Usuário: `postgres`
  - Senha: `postgres`

## 📈 Análise Exploratória de Dados (EDA)

O módulo `model_trainer` gera automaticamente visualizações e análises exploratórias, incluindo:

- Matriz de correlação
- Distribuições univariadas
- Gráficos de dispersão (scatter plots)
- KDE plots (Kernel Density Estimation)
- Pair plots
- Análise de valores faltantes

Todas as visualizações são salvas na pasta `model_trainer/eda_outputs/`.

## 🤖 Modelo de Machine Learning

O sistema utiliza modelos de Machine Learning para prever a produção futura de soja baseado nas features extraídas. O modelo é treinado e avaliado automaticamente, gerando previsões para os próximos anos.

## 📱 Visualização

O dashboard PowerBI está localizado em `powerbi/DASHBOARD.pbix` e pode ser aberto no PowerBI Desktop para visualizar os resultados e previsões geradas pelo modelo.

## 📝 Observações

- Certifique-se de que o Docker Desktop está em execução antes de iniciar o projeto
- O primeiro processamento pode levar alguns minutos devido ao download dos dados do FAOSTAT
- Os dados são persistidos em volumes Docker, então os dados permanecerão entre execuções

## 📄 Licença

Este projeto faz parte de um trabalho de conclusão de curso (TCC).

