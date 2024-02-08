@description('Environment e.g. "dev", "test", "prod"')
param environment string
param location string = resourceGroup().location
param imageVersion string = 'latest'
param tags object = {
  Application: 'bike-count'
  Environment: environment
  CreatedBy: 'bicep'
  Owner: 'Christian Fosli'
}

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-bikecount-${environment}'
  location: location
  tags: tags
  properties: {
    retentionInDays: 14
    sku: {
      name: 'Free'
    }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-bikecount-${environment}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
  }
}

resource appEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'cae-bikecount-${environment}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

resource app 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'ca-bikecount-${environment}'
  location: location
  tags: tags
  properties: {
    environmentId: 'TODO'
    configuration: {
      ingress: {
        targetPort: 8501
        external: true
      }
    }
    template: {
      containers: [
        {
          name: 'bike-count-app'
          image: 'ghcr.io/christianfosli/bike-count/app:${imageVersion}'
          probes: [
            {
              type: 'Readiness'
              httpGet: {
                path: '/healthz'
                port: 8501
              }
            }
            {
              type: 'Liveness'
              httpGet: {
                path: '/healthz'
                port: 8501
              }
            }
          ]
        }
      ]
    }
  }
}
