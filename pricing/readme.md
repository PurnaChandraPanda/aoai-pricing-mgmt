## Pre-requisite
- Optional: register RP CostManagementExports
```
az provider register --namespace Microsoft.CostManagementExports
az provider show -n Microsoft.CostManagementExports
az provider show --namespace Microsoft.CostManagementExports --query "registrationState"
** wait it be Registered
```

## API details on Subscription Cost Management
[deprecated]
Microsoft.Consumption/usageDetails?api-version=2024-08-01

[use]
Microsoft.CostManagement/generateCostDetailsReport?api-version=2024-08-01

https://learn.microsoft.com/en-us/rest/api/cost-management/generate-cost-details-report/create-operation?view=rest-cost-management-2024-08-01&tabs=HTTP

## Run the app to get subscription cost details
- Feed the subscription id, usageFrom and usageTo, aoai resource name
- Run the app with cost management api invoke
```
python generate_cost_details.py
```


