"""Helpers functions for endpoint scaling"""

import time
from typing import Tuple, Union

import boto3

region = boto3.Session().region_name

cloudwatch_client = boto3.client("cloudwatch", region_name=region)
aas_client = boto3.client("application-autoscaling", region_name=region)
sm_client = boto3.client("sagemaker", region_name=region)


def register_scaling(
    endpoint_name: str,
    variant_name: str,
    max_capacity: int,
    min_capacity: int = 1,
) -> dict:
    """
    Register the scaling target to SageMaker endpoint variant with min and max
    scaling capacity

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    max_capacity : int
        The max number of instances
    min_capacity : int
        The minimum number of instances. It must be greater than 0

        Defaults to 1.

    Returns
    -------
    dict
        The response from the scalable target registration
    """
    resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"
    response = aas_client.register_scalable_target(
        ServiceNamespace="sagemaker",
        ResourceId=resource_id,
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        MinCapacity=min_capacity,
        MaxCapacity=max_capacity,
    )

    return response


def deregister_scaling(endpoint_name: str, variant_name: str) -> dict:
    """
    Deregister the scaling target from the SageMaker endpoint variant

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant

    Returns
    -------
    dict
        The response from the scalable target deregistration
    """
    resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"
    response = aas_client.deregister_scalable_target(
        ServiceNamespace="sagemaker",
        ResourceId=resource_id,
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
    )

    return response


def set_target_scaling_on_invocation(
    endpoint_name: str,
    variant_name: str,
    target_value: int,
    scale_out_cool_down: int = 10,
    scale_in_cool_down: int = 100,
) -> dict:
    """
    Set scaling target based on invocation per instance with cool-down periods

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    target_value : int
        The target value for scaling based on invocations per instance
    scale_out_cool_down : int, optional
        The cool-down period for scaling out in seconds, by default 10
    scale_in_cool_down : int, optional
        The cool-down period for scaling in in seconds, by default 100

    Returns
    -------
    dict
        The policy name and the response from the scaling policy creation
    """
    policy_name = f"target-tracking-invocations-{round(time.time())}"
    resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"

    response = aas_client.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace="sagemaker",
        ResourceId=resource_id,
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        PolicyType="TargetTrackingScaling",
        TargetTrackingScalingPolicyConfiguration={
            "TargetValue": target_value,
            "PredefinedMetricSpecification": {
                "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance",
            },
            "ScaleOutCooldown": scale_out_cool_down,
            "ScaleInCooldown": scale_in_cool_down,
            "DisableScaleIn": False,
        },
    )

    return policy_name, response


def set_target_scaling_on_hardware_utilization(
    endpoint_name: str,
    variant_name: str,
    hardware: Union["cpu", "gpu"],
    target_value: int,
    scale_out_cool_down: int = 10,
    scale_in_cool_down: int = 100,
) -> Tuple[str, dict]:
    """
    Set scaling target with hardware (cpu or gpu) utilization.

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    hardware : Union["cpu", "gpu"]
        The hardware type (cpu or gpu) for scaling target
    target_value : int
        The target value for scaling based on hardware utilization
    scale_out_cool_down : int, optional
        The cool-down period for scaling out in seconds, by default 10
    scale_in_cool_down : int, optional
        The cool-down period for scaling in in seconds, by default 100

    Returns
    -------
    Tuple[str, dict]
        A tuple with the policy name, and the scaling policy response
    """
    hardware = hardware.upper()

    policy_name = f"target-tracking-{hardware}-util-{round(time.time())}"
    resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"

    response = aas_client.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace="sagemaker",
        ResourceId=resource_id,
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        PolicyType="TargetTrackingScaling",
        TargetTrackingScalingPolicyConfiguration={
            "TargetValue": target_value,
            "CustomizedMetricSpecification": {
                "MetricName": f"{hardware}Utilization",
                "Namespace": "/aws/sagemaker/Endpoints",
                "Dimensions": [
                    {"Name": "EndpointName", "Value": endpoint_name},
                    {"Name": "VariantName", "Value": variant_name},
                ],
                "Statistic": "Average",
                "Unit": "Percent",
            },
            "ScaleOutCooldown": scale_out_cool_down,
            "ScaleInCooldown": scale_in_cool_down,
            "DisableScaleIn": False,
        },
    )

    return policy_name, response


def delete_scaling_policies(
    endpoint_name: str,
    variant_name: str,
    policy_names: list = [],
) -> None:
    """
    Delete scaling policies

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    policy_names : list, optional
        List of policy names to be deleted, by default an empty list
    """
    resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"

    for each_policy in policy_names:
        aas_client.delete_scaling_policy(
            PolicyName=each_policy,
            ServiceNamespace="sagemaker",
            ResourceId=resource_id,
            ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        )


def wait_for_endpoint_to_finish_updating_or_creating(endpoint_name: str) -> None:
    """
    Wait for the endpoint to finish updating or creating.

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    """
    finished = False

    while not finished:
        endpoint_response = sm_client.describe_endpoint(EndpointName=endpoint_name)

        if endpoint_response["EndpointStatus"] in [
            "InService",
            "Deleting",
            "Failed",
            "OutOfService",
        ]:
            print(
                f"Endpoint {endpoint_name} is in {endpoint_response['EndpointStatus']} state",
            )
            finished = True
        else:
            print(f"Endpoint {endpoint_name} is in updating/creating")
            time.sleep(30)


def clear_auto_scaling_and_reset_to_initial_count(
    endpoint_name: str,
    variant_name: str,
    initial_count: int,
) -> None:
    """
    Clear auto-scaling policies and reset to the initial instance count.

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    initial_count : int
        The initial instance count to reset to
    """
    deregister_scaling(endpoint_name=endpoint_name, variant_name=variant_name)

    sm_client.update_endpoint_weights_and_capacities(
        EndpointName=endpoint_name,
        DesiredWeightsAndCapacities=[
            {"VariantName": variant_name, "DesiredInstanceCount": initial_count},
        ],
    )

    wait_for_endpoint_to_finish_updating_or_creating(endpoint_name)


def create_step_scaling_policy(
    endpoint_name: str,
    variant_name: str,
    policy_name: str,
    step_scaling_policy_configuration: dict,
) -> str:
    """
    Creates a step scaling policy

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    policy_name : str
        The name of the step scaling policy
    step_scaling_policy_configuration : dict
        The step scaling policy configuration, as per [AWS documentation]
        (https://boto3.amazonaws.com/v1/documentation/api/1.26.109/reference/services/
        application-autoscaling/client/put_scaling_policy.html).

    Returns
    -------
    str
        The ARN of the step scaling policy
    """
    resource_id = f"endpoint/{endpoint_name}/variant/{variant_name}"

    response = aas_client.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace="sagemaker",
        ResourceId=resource_id,
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        PolicyType="StepScaling",
        StepScalingPolicyConfiguration=step_scaling_policy_configuration,
    )

    return response["PolicyARN"]


def create_alarm_based_on_step_policy(
    step_policy_arn: str,
    endpoint_name: str,
    variant_name: str,
    alarm_name: str,
    threshold: float,
    comparison_operator: str = "GreaterThanOrEqualToThreshold",
    metric_name: str = "InvocationsPerInstance",
    namespace: str = "AWS/SageMaker",
    statistic: str = "Sum",
    period: int = 60,
    evaluation_period: int = 1,
) -> dict:
    """
    Creates a cloudwatch alarm linked to the step policy autoscaling

    Parameters
    ----------
    step_policy_arn : str
        The ARN of the step policy
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    alarm_name : str
        The name of the cloudwatch alarm
    threshold : float
        The metric threshold to trigger the alarm
    comparison_operator : str, optional
        The comparison operator, as per AWS Documentation

        Defaults to `GreaterThanOrEqualToThreshold`
    metric_name : str, optional
        The metric name, as per AWS Documentation

        Defaults to `InvocationsPerInstance`
    namespace : str, optional
        The metric namespace

        Defaults to `AWS/SageMaker`
    statistic : str, optional
        The metric statistic

        Defaults to `Sum`
    period : int, optional
        The metric period

        Defaults to `60`

        Note: `evaluation_period` * `period` = time to trigger the alarm
    evaluation_period: int, optional
        The metric evaluation period

        Defaults to `1`

        Note: `evaluation_period` * `period` = time to trigger the alarm

    Returns
    -------
    dict
        The response dictionary
    """
    response = cloudwatch_client.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic=statistic,
        Period=period,
        EvaluationPeriods=evaluation_period,
        Threshold=threshold,
        ComparisonOperator=comparison_operator,
        Dimensions=[
            {"Name": "EndpointName", "Value": endpoint_name},
            {"Name": "VariantName", "Value": variant_name},
        ],
        AlarmActions=[step_policy_arn],
    )

    return response


def remove_step_scaling_policy(policy_name: str, alarm_name: str) -> Tuple[dict, dict]:
    """
    Removes a step scaling policy and its associated cloudwatch alarm

    Parameters
    ----------
    policy_name : str
        The name of the step scaling policy
    alarm_name : str
        The name of the cloud watch alarm

    Returns
    -------
    Tuple[dict, dict]
        The response dictionary from cloudwatch and autoscaling
    """
    describe_scaling_policy = aas_client.describe_scaling_policies(
        PolicyNames=[policy_name],
        ServiceNamespace="sagemaker",
    )

    cloudwatch_response = cloudwatch_client.delete_alarms(AlarmNames=[alarm_name])
    autoscaling_response = aas_client.delete_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace="sagemaker",
        ResourceId=describe_scaling_policy["ScalingPolicies"][0]["ResourceId"],
        ScalableDimension=describe_scaling_policy["ScalingPolicies"][0][
            "ScalableDimension"
        ],
    )

    return cloudwatch_response, autoscaling_response
