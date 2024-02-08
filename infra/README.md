# Infrastructure code for running the bike-count app as an Azure Container App

### Manual steps

The following steps have been performed manually:

* Run script `initial-infra-bootstrap.sh` in a terminal.
  This ensures the required resource group is created and that GitHub actions can access Azure using workload identity / federated credentials.

* Then add required variables `AZ_CLIENT_ID`, `AZ_TENANT_ID`, `AZ_SUBSCRIPTION_ID` in GitHub (environment) settings.
