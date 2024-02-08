#!/usr/bin/env bash
set -eo pipefail

az account show && echo 'Resources will be created in above subscription. Starting in 5 seconds. Press Ctrl-C to cancel.' && sleep 5

echo 'Creating resource groups'
az group create -n rg-bikecount-dev -l norwayeast
az group create -n rg-bikecount-prod -l norwayeast

echo 'Creating apps in Entra ID'
az ad app create --display-name christianfosli/bikecount-dev
az ad app create --display-name christianfosli/bikecount-prod

echo 'Creating federated credentials for GitHub Actions'

cat << EOF > creds-dev.json
{
  "audiences": [
    "api://AzureADTokenExchange"
  ],
  "description": "Permission to access Azure from GitHub actions workflows - dev",
  "issuer": "https://token.actions.githubusercontent.com",
  "name": "christianfosli-bikecount-github-actions-dev",
  "subject": "repo:christianfosli/bike-count:environment:dev"
}
EOF
objectIdDev="$(az ad app list --display-name christianfosli/bikecount-dev --query [0].id -o tsv)"
az ad app federated-credential create --id $objectIdDev --parameters creds-dev.json

cat << EOF > creds-prod.json
{
  "audiences": [
    "api://AzureADTokenExchange"
  ],
  "description": "Permission to access Azure from GitHub actions workflows - prod",
  "issuer": "https://token.actions.githubusercontent.com",
  "name": "christianfosli-bikecount-github-actions-prod",
  "subject": "repo:christianfosli/bike-count:environment:prod"
}
EOF
objectIdProd="$(az ad app list --display-name christianfosli/bikecount-prod --query [0].id -o tsv)"
az ad app federated-credential create --id $objectIdProd --parameters creds-prod.json

rm creds-dev.json creds-prod.json

echo 'Creating service principals for apps (needed to do role assignments)'
appIdDev="$(az ad app list --display-name christianfosli/bikecount-dev --query [0].appId -o tsv)"
az ad sp create --id "$appIdDev"
appIdProd="$(az ad app list --display-name christianfosli/bikecount-prod --query [0].appId -o tsv)"
az ad sp create --id "$appIdProd"

echo 'Granting service pricipals contributor access to resource group'
subsId="$(az account show --query 'id' -o tsv)"
az role assignment create --assignee "$appIdDev" --role Contributor --scope "/subscriptions/$subsId/resourceGroups/rg-bikecount-dev"
az role assignment create --assignee "$appIdProd" --role Contributor --scope "/subscriptions/$subsId/resourceGroups/rg-bikecount-prod"

echo "Success"
