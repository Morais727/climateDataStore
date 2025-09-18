#!/bin/bash

# ------------------------
# CONFIGURAÇÃO
# ------------------------
REMOTE_USER="marcosmorais"
REMOTE_HOST="177.105.35.229"

REMOTE_DIR_DAGS="/home/marcosmorais/airflow/dags/"
LOCAL_DIR_DAGS="/home/marcos-morais/Documentos/ZETTA/climateDataStore/airflow/dags/"

REMOTE_DIR_SCRIPTS="/home/marcosmorais/airflow/scripts/"
LOCAL_DIR_SCRIPTS="/home/marcos-morais/Documentos/ZETTA/climateDataStore/airflow/scripts/"

LOG_FILE="$HOME/sync_bidirectional.log"
INTERVAL=60  # intervalo em segundos entre sincronizações

RSYNC_OPTS="-avz --update --ignore-errors"

while true; do
    DATE=$(date +"%Y-%m-%d %H:%M:%S")
    
    echo "[$DATE] Sincronizando DAGS (servidor → local)..." | tee -a $LOG_FILE
    rsync $RSYNC_OPTS ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_DAGS} ${LOCAL_DIR_DAGS} | tee -a $LOG_FILE
    
    echo "[$DATE] Sincronizando DAGS (local → servidor)..." | tee -a $LOG_FILE
    rsync $RSYNC_OPTS ${LOCAL_DIR_DAGS} ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_DAGS} | tee -a $LOG_FILE

    echo "[$DATE] Sincronizando SCRIPTS (servidor → local)..." | tee -a $LOG_FILE
    rsync $RSYNC_OPTS ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_SCRIPTS} ${LOCAL_DIR_SCRIPTS} | tee -a $LOG_FILE
    
    echo "[$DATE] Sincronizando SCRIPTS (local → servidor)..." | tee -a $LOG_FILE
    rsync $RSYNC_OPTS ${LOCAL_DIR_SCRIPTS} ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR_SCRIPTS} | tee -a $LOG_FILE

    echo "[$DATE] Sincronização concluída. Aguardando ${INTERVAL}s..." | tee -a $LOG_FILE
    sleep $INTERVAL
done


# ssh -L 8080:localhost:8080 marcosmorais@177.105.35.229
