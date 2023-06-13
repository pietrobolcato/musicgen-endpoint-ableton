"""
From a model group, get the ARN of the latest approved one, and extends the input config
yaml file with this fetched information
"""

import argparse
import logging

import boto3
import ruamel.yaml

logger = logging.getLogger(__name__)
client = boto3.client(service_name="sagemaker")
yaml = ruamel.yaml.YAML()
yaml.width = float("inf")


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments

    Returns
    -------
    argparse.Namespace
        An object containing the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        required=True,
        help="The path to the input YAML file to extend",
    )

    args = parser.parse_args()
    return args


def get_latest_approved_model_arn(model_group_name: str) -> str:
    """
    Get the latest approved model ARN of a model group

    Parameters
    ----------
    model_group_name : str
        The name of the model group

    Returns
    -------
    str
        The ARN of the latest approved model
    """
    response = client.list_model_packages(
        ModelPackageGroupName=model_group_name,
        ModelApprovalStatus="Approved",
        SortBy="CreationTime",
        MaxResults=100,
    )
    approved_packages = response["ModelPackageSummaryList"]

    # fetch more packages if none returned with continuation token
    while len(approved_packages) == 0 and "NextToken" in response:
        logger.debug(f"Getting more packages for token: {response['NextToken']}")

        response = client.list_model_packages(
            ModelPackageGroupName=model_group_name,
            ModelApprovalStatus="Approved",
            SortBy="CreationTime",
            MaxResults=100,
            NextToken=response["NextToken"],
        )
        approved_packages.extend(response["ModelPackageSummaryList"])

    # return error if no packages found
    if len(approved_packages) == 0:
        error_message = f"No approved ModelPackage found for: {model_group_name}"
        logger.error(error_message)
        raise Exception(error_message)

    # return the model package arn
    model_package_arn = approved_packages[0]["ModelPackageArn"]
    return model_package_arn


def read_yaml(yaml: ruamel.yaml.YAML, file_path: str) -> dict:
    """
    Read YAML content from a file

    Parameters
    ----------
    yaml : ruamel.yaml.YAML
        The YAML object
    file_path : str
        The path to the YAML file

    Returns
    -------
    dict
        A dictionary containing the YAML content
    """
    with open(file_path) as yaml_file:
        yaml_content = yaml.load(yaml_file)

    return yaml_content


def update_yaml(
    file_path: str,
    yaml_content: dict,
    model_package_arn: str,
) -> None:
    """
    Update the YAML content with the model data

    Parameters
    ----------
    file_path : str
        The path to the YAML file
    yaml_content : dict
        The content of the YAML file
    model_package_arn : str
        The model package ARN, retrieved from the `get_latest_approved_model_arn`
        function
    """
    yaml_content["model_arn"] = model_package_arn
    yaml.dump(yaml_content, open(file_path, "w"))


def main() -> None:
    """The main function of the script"""
    args = parse_args()

    yaml_content = read_yaml(yaml=yaml, file_path=args.input_file)
    model_package_arn = get_latest_approved_model_arn(yaml_content["model_group_name"])

    update_yaml(
        file_path=args.input_file,
        yaml_content=yaml_content,
        model_package_arn=model_package_arn,
    )


if __name__ == "__main__":
    main()
