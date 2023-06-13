# Provision endpoint

Provides the endpoint, optionally with data capture and autoscaling, using terraform.
The files should not be executed directly, but through the CD pipeline that executes the script `scripts/get_latest_approved_model.py.py` first.

## Settings

1. Set the backend values in `src/terraform/main.tf`:

   - `bucket`, `region`, `dynamodb_table`: with their respective values
   - `key`: `<NAMESPACE>` should be replaced with the namespace, or the name of the project — ideally should be equivalent to the `namespace` variable set in `src/terraform/variables.tf`

2. Set the variables in `src/config-dev.yaml` and `src/config-prod.yaml`. A template can be found in `.templates/config-template.yaml`

3. Set the values for the github action workflows: `endpoint-destroy.yaml`, `endpoint-provision.yaml`, `endpoint-plan.yaml`, `terraform-validate.yaml`:
   - `aws_role`, and `aws_role_region`: with the role configured to work with github actions. Check [here](https://github.com/pietrobolcato/aws-tests/blob/main/notes/configure_aws_credential_gh_actions.md) for how to do it.
   - `root_folder`: with the root folder where the configurations file lie. Eg for: `src/config-dev.yaml` the `root_folder` would be `src`.

## How to run

Run the CD pipeline, either automatically on push, or manually using the Github actions UI.
