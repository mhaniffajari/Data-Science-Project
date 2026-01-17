1. Enable API:
```
gcloud services enable documentai.googleapis.com      
gcloud services enable cloudfunctions.googleapis.com  
gcloud services enable cloudbuild.googleapis.com    
gcloud services enable geocoding-backend.googleapis.com   
```

2. finance-processor: a505dd9422616889

3. Create Bucket:
export PROJECT_ID="qwiklabs-gcp-01-2d42b886f98a"
export BUCKET_LOCATION="us-east4"
gsutil mb -c standard -l ${BUCKET_LOCATION} -b on \
  gs://${PROJECT_ID}-input-invoices
gsutil mb -c standard -l ${BUCKET_LOCATION} -b on \
  gs://${PROJECT_ID}-output-invoices
gsutil mb -c standard -l ${BUCKET_LOCATION} -b on \
  gs://${PROJECT_ID}-archived-invoices

4. Create Table:
bq --location="US" mk  -d \
    --description "Form Parser Results" \
    ${PROJECT_ID}:invoice_parser_results
cd ~/documentai-pipeline-demo/scripts/table-schema/
bq mk --table \
  invoice_parser_results.doc_ai_extracted_entities \
  doc_ai_extracted_entities.json
bq mk --table \
  invoice_parser_results.geocode_details \
  geocode_details.json

5. Activate Cloud Function
gcloud storage service-agent --project=$PROJECT_ID

PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud iam service-accounts create "service-$PROJECT_NUMBER" \
  --display-name "Cloud Storage Service Account" || true

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:service-$PROJECT_NUMBER@gs-project-accounts.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:service-$PROJECT_NUMBER@gs-project-accounts.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountTokenCreator"

PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format='value(project_number)')

SERVICE_ACCOUNT=$(gcloud storage service-agent --project=$PROJECT_ID)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SERVICE_ACCOUNT \
  --role roles/pubsub.publisher

  export CLOUD_FUNCTION_LOCATION=us-east4
  gcloud functions deploy process-invoices \
  --gen2 \
  --region=${CLOUD_FUNCTION_LOCATION} \
  --entry-point=process_invoice \
  --runtime=python313 \
  --service-account=${PROJECT_ID}@appspot.gserviceaccount.com \
  --source=cloud-functions/process-invoices \
  --timeout=400 \
  --env-vars-file=cloud-functions/process-invoices/.env.yaml \
  --trigger-resource=gs://${PROJECT_ID}-input-invoices \
  --trigger-event=google.storage.object.finalize\
  --service-account $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --allow-unauthenticated


6. Testing File

gcloud storage cp 279-en-invoice-commercial-ty.pdf gs://qwiklabs-gcp-01-2d42b886f98a-input-invoices/
