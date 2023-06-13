# Provision EC2

Provides an EC2 instance with GPU using terraform, used to develop the AI module.

## Provision

1. Configure `config.tfvars` starting from `config.tfvars.template`:
    - Using local ssh keys:

        -   Create a ssh key pair:
            ```
            ssh-keygen -f <key-pair-name>
            ```

            Then set the variable `public_key_path` to the path of the generated key, ending with `.pub`.

            For example, run `ssh-keygen -f my-key-pair` and set `public_key_path = "my-key-pair.pub"`

        -   Use already existing AWS key pair:
            Set the variable `public_key_path` to `null`.

    - Note:
        - The key naming on AWS is automatically generated, but can be explicitely specified using the variable `key_name`.
        - All the variables are exposed in the `variables.tf` file

2. Set the backend values in `src/main.tf`:
    - `bucket`, `region`, `dynamodb_table`: with their respective values
    - `key`: `<NAMESPACE>` should be replaced with the namespace, or the name of the project — ideally should be equivalent to the `namespace` variable set in `src/configure.tf`

3. Run `terraform init`

4. Run `terraform plan`

5. Run `terraform apply`

6. To destroy, run `terraform destroy`

## How to connect

Once the EC2 instance is provisioned, it is possible to connect through `ssh`, and to start and stop it using the [AWS Console](https://us-east-1.console.aws.amazon.com/ec2/)