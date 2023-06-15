# Provision endpoint

Provides the endpoint, optionally with data capture and autoscaling, using terraform.
The files should not be executed directly, but through the CD pipeline that executes the script `scripts/get_latest_approved_model.py.py` first.

## Settings

1. Set the backend values in `src/terraform/main.tf`:

   - `bucket`, `region`, `dynamodb_table`: with their respective values
   - `key`: `<NAMESPACE>` should be replaced with the namespace, or the name of the project — ideally should be equivalent to the `namespace` variable set in `src/terraform/variables.tf`

2. Set the variables in `src/config-dev.yaml` and `src/config-prod.yaml`. A template can be found in `.templates/config-template.yaml`

## How to run

Run the CD pipeline, either automatically on push, or manually using the Github actions UI.
