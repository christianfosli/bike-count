# Infrastructure code for running the bike-count app as an Azure Container App

### Manual steps

The following steps have been performed manually:

* Run script `initial-infra-bootstrap.sh` in a terminal.
  This ensures the required resource group is created and that GitHub actions can access Azure using workload identity / federated credentials.

* Then add required variables `AZ_CLIENT_ID`, `AZ_TENANT_ID`, `AZ_SUBSCRIPTION_ID` in GitHub (environment) settings.

* [After pipeline has run at least once] Add CNAME records for custom domain with domain registrar

  * Note that the custom domain related infra in main.bicep probably must be commented out when running this for the first time in a a new subscription

  * Also note that as of Feb 2024 adding custom domains to containerapps using Bicep is kind of tricky,
    see [this blog post](https://johnnyreilly.com/azure-container-apps-bicep-managed-certificates-custom-domains) for instructions.
