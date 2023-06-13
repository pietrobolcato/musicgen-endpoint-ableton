# Image generation endpoint

This repo is a general template to develop AI module and provision them as Sagemaker
endpoint. The folder `aws` is defined as follows:

```
aws
├── endpoint
│   ├── model
│   ├── notebooks
│   ├── src
│   │   ├── code
│   │   └── helpers
│   └── tests
│       └── support
│           ├── expected_output
│           ├── input
│           └── predicted_output
└── terraform
    ├── provision_ec2
    │   └── src
    └── provision_endpoint
        └── src
            ├── scripts
            └── terraform
```

Where:

- `endpoint` contains all the endpoint-related code. This include:

  - `model`: this folder includes the `model.tar.gz` file, and the bash script to
    create it
  - `notebooks`: this folder includes the notebooks used to test the model locally, to
    register the model in the model registry, and test the deployment online.
  - `src`: this folder includes the inference code, as well scoring-specific helper
    libraries and functions.
  - `tests`: this folder includes the tests for the functions defined in
    the `inference.py` code. These tests are fundamental in the development workflow.
    For more information, check the [Development workflow](#development-workflow)
    section below.

- `terraform`: contains the terraform code to provision the ec2 instance as well as the
  endpoint during CD. Check the readme of the invidual folders for more information.

## Development workflow

The development workflow is as following:

- All the development happens inside the dev container
- Only when there is the need to run the notebook, this is run from another vscode
  window connected with ssh only
- The `inference.py` script should be tested with their invidual functions, eg: as shown
  in the `aws/endpoint/src/tests/` folder. Once these work as expected, only then the you
  should execute the local deploymnt notebook. This is a huge time-saver, because the
  notebook can be very slow to run.

## Get started

1.  Login to AWS:

    ```
    aws sso login
    ```

2.  Change the configuration in `aws/terraform/provision_ec2/src/config.tfvars`, and
    update the `main.tf` backend as needed, especially in the terraform state `key`.
    Also, change `locals.tf`. Then create the ec2 dev instance:

    ```bash
    cd aws/terraform/provision_ec2/
    terraform init
    terraform plan -out=out.tfplan
    terraform apply out.tfplan
    ```

3.  Connect to the ec2 dev instance using vscode remote ssh server

4.  Create and activate dev env

    ```
    conda env create -f envs/dev.yaml -n dev
    conda activate dev
    ```

5.  Develop the `inference.py` code, using `aws/endpoint/src/tests/` to ensure that
    all the methods work as expected.

6.  Test the endpoint using the `deployment.ipynb` notebook.

7.  Repeat step 5 and 6 until ready.

8.  Change the configuration in `aws/terraform/provision_ec2/src/config-dev.yaml` and
    `aws/terraform/provision_ec2/src/config-prod.yaml`. Also update the `main.tf`
    backend as needed, especially in the terraform state `key`. Finally, change
    `locals.tf` as needed.

9.  Use github actions defined in `.github/workflows/` to execute the CD pipeline and
    provision / destroy the endpoint.
