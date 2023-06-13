"""Helpers functions to show results and analysis"""

import datetime
import json
import math
from operator import itemgetter
from typing import Tuple

import boto3
from IPython.display import Image, display

region = boto3.Session().region_name
sm_client = boto3.client("sagemaker", region_name=region)
cloudwatch = boto3.client("cloudwatch", region_name=region)
aas_client = boto3.client("application-autoscaling")


def analysis_and_visualize_time_now(
    endpoint_name: str,
    variant_name: str,
    upper_threshold: float = 55.0,
    lower_threshold: float = 45.0,
    hardware: str = "cpu",
    timedelta_minutes=30,
    hours_timezone=0,
):
    """
    Wrapper for the function `analysis_and_visualize` which sets the datetime to
    now +- `timedelta_minutes`

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    upper_threshold : float, optional
        The upper threshold for scaling, by default 55.0
    lower_threshold : float, optional
        The lower threshold for scaling, by default 45.0
    hardware : str, optional
        The hardware type for scaling, by default "cpu"
    timedelta_minutes : int
        The minutes of difference with respect to datetime now
    hours_timezone : int
        Offset of timezone hours

    Returns
    -------
    Tuple[int, int, int]
        A tuple containing the maximum number of invocations, upper limit, and
        lower limit
    """
    datetime_now = datetime.datetime.now()
    start_time = (
        datetime_now
        - datetime.timedelta(minutes=timedelta_minutes)
        + datetime.timedelta(hours=hours_timezone)
    )
    end_time = (
        datetime_now
        + datetime.timedelta(minutes=timedelta_minutes)
        + datetime.timedelta(hours=hours_timezone)
    )

    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    max_value, upper_limit, lower_limit = analysis_and_visualize(
        endpoint_name=endpoint_name,
        variant_name=variant_name,
        start_time=start_time,
        end_time=end_time,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold,
        hardware=hardware,
    )

    return max_value, upper_limit, lower_limit


def analysis_and_visualize(
    endpoint_name: str,
    variant_name: str,
    start_time: str,
    end_time: str,
    upper_threshold: float = 55.0,
    lower_threshold: float = 45.0,
    visualize: bool = True,
    hardware: str = "cpu",
) -> Tuple[int, int, int]:
    """
    Visualizes the benchmarking and derives the target for scaling based on input
    thresholds.

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant
    start_time : str
        The start time for the analysis in the format "%Y-%m-%dT%H:%M:%S.000Z"
    end_time : str
        The end time for the analysis in the format "%Y-%m-%dT%H:%M:%S.000Z"
    upper_threshold : float, optional
        The upper threshold for scaling, by default 55.0
    lower_threshold : float, optional
        The lower threshold for scaling, by default 45.0
    visualize : bool, optional
        Flag indicating whether to visualize the results, by default True
    hardware : str, optional
        The hardware type for scaling, by default "cpu"

    Returns
    -------
    Tuple[int, int, int]
        A tuple containing the maximum number of invocations, upper limit, and lower limit
    """
    stats_response = cloudwatch.get_metric_statistics(
        Period=30,
        StartTime=start_time,
        EndTime=end_time,
        MetricName="Invocations",
        Namespace="AWS/SageMaker",
        Statistics=["Sum"],
        Dimensions=[
            {"Name": "EndpointName", "Value": endpoint_name},
            {"Name": "VariantName", "Value": variant_name},
        ],
    )

    max_value = 0
    invocations_list = []
    for each in stats_response["Datapoints"]:
        invocations_list.append(each)
        if max_value < each["Sum"]:
            max_value = each["Sum"]

    invocations_list = sorted(invocations_list, key=itemgetter("Timestamp"))

    if visualize:
        print(f"Maximum Invocation seen in benchmarking = {max_value}")

    upper_limit = math.floor(max_value * upper_threshold / 100)
    lower_limit = math.ceil(max_value * lower_threshold / 100)

    if visualize:
        print(
            f"Invocation upper limit={upper_limit} for {upper_threshold}%, \
            lower limit={lower_limit} for {lower_threshold}%",
        )

    max_diff = math.inf
    min_diff = math.inf
    timestamp_upper = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.000Z")
    timestamp_lower = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.000Z")
    for each in invocations_list:
        if abs(each["Sum"] - lower_limit) < min_diff:
            min_diff = abs(each["Sum"] - lower_limit)
            timestamp_lower = each["Timestamp"]
        elif abs(each["Sum"] - upper_limit) < max_diff:
            max_diff = abs(each["Sum"] - upper_limit)
            timestamp_upper = each["Timestamp"]
        else:
            break

    invocations_metrics_widget = {
        "metrics": [
            [
                "AWS/SageMaker",
                "InvocationModelErrors",
                "EndpointName",
                endpoint_name,
                "VariantName",
                variant_name,
            ],
            [".", "Invocation5XXErrors", ".", ".", ".", "."],
            [".", "Invocation4XXErrors", ".", ".", ".", "."],
            [".", "ModelLatency", ".", ".", ".", ".", {"yAxis": "right"}],
            [".", "OverheadLatency", ".", ".", ".", ".", {"yAxis": "right"}],
            [".", "InvocationsPerInstance", ".", ".", ".", "."],
            [".", "Invocations", ".", ".", ".", "."],
        ],
        "view": "timeSeries",
        "stat": "ts99",
        "period": 60,
        "title": "InvocationsVsLatencies",
        "width": 1200,
        "height": 400,
        "start": start_time,
        "end": end_time,
        "annotations": {
            "horizontal": [
                [
                    {"value": upper_limit},
                    {
                        "value": lower_limit,
                    },
                ],
            ],
            "vertical": [
                [
                    {"value": timestamp_upper.strftime("%Y-%m-%dT%H:%M:%S.000Z")},
                    {
                        "value": timestamp_lower.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    },
                ],
            ],
        },
    }

    invocations_response = cloudwatch.get_metric_widget_image(
        MetricWidget=json.dumps(invocations_metrics_widget),
        OutputFormat="png",
    )

    utilization_metrics_widget = {
        "metrics": [
            [
                "/aws/sagemaker/Endpoints",
                f"{hardware.upper()}Utilization",
                "EndpointName",
                endpoint_name,
                "VariantName",
                variant_name,
            ],
            [".", "MemoryUtilization", ".", ".", ".", ".", {"yAxis": "right"}],
            [".", "DiskUtilization", ".", ".", ".", ".", {"yAxis": "left"}],
        ],
        "view": "timeSeries",
        "stat": "ts99",
        "period": 60,
        "title": "UtilizationMetrics",
        "width": 1200,
        "height": 400,
        "start": start_time,
        "end": end_time,
        "annotations": {
            "vertical": [
                [
                    {"value": timestamp_upper.strftime("%Y-%m-%dT%H:%M:%S.000Z")},
                    {
                        "value": timestamp_lower.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    },
                ],
            ],
        },
    }

    utilization_response = cloudwatch.get_metric_widget_image(
        MetricWidget=json.dumps(utilization_metrics_widget),
        OutputFormat="png",
    )

    x = Image(invocations_response["MetricWidgetImage"])
    y = Image(data=utilization_response["MetricWidgetImage"])

    if visualize:
        display(x, y)

    return max_value, upper_limit, lower_limit


def get_current_invocation_per_instance(endpoint_name: str, variant_name: str) -> int:
    """
    Get the current invocation per instance metric of an endpoint

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant

    Returns
    -------
    int
        The current invocation per instance metric
    """
    datetime_now = datetime.datetime.now()

    start_time = (
        datetime_now - datetime.timedelta(minutes=1) + datetime.timedelta(hours=6)
    )
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    end_time = (
        datetime_now + datetime.timedelta(minutes=1) + datetime.timedelta(hours=6)
    )
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    stats_response = cloudwatch.get_metric_statistics(
        Period=30,
        StartTime=start_time,
        EndTime=end_time,
        MetricName="InvocationsPerInstance",
        Namespace="AWS/SageMaker",
        Statistics=["Sum"],
        Dimensions=[
            {"Name": "EndpointName", "Value": endpoint_name},
            {"Name": "VariantName", "Value": variant_name},
        ],
    )

    try:
        return stats_response["Datapoints"][0]["Sum"]
    except Exception:
        return 0.0


def get_autoscaling_last_activity(
    endpoint_name: str,
    variant_name: str,
) -> Tuple[str, str, str, str]:
    """
    Get the last activity of the autoscaling log

    Parameters
    ----------
    endpoint_name : str
        The name of the endpoint
    variant_name : str
        The name of the endpoint variant

    Returns
    -------
    Tuple[str, str, str, str]
        A tuple containing: `start date, end date, description, cause` of the latest
        autoscaling event
    """
    response = aas_client.describe_scaling_activities(
        ServiceNamespace="sagemaker",
        ResourceId=f"endpoint/{endpoint_name}/variant/{variant_name}",
    )

    last_activity = response["ScalingActivities"][0]

    start_time = last_activity["StartTime"].strftime("%Y-%m-%dT%H:%M:%S.000Z")
    description = last_activity["Description"]
    cause = last_activity["Cause"].split("policy")[-1].strip()

    if "EndTime" in last_activity:
        end_time = last_activity["EndTime"].strftime("%Y-%m-%dT%H:%M:%S.000Z")
    else:
        end_time = -1

    return start_time, end_time, description, cause
