# scale out
resource "aws_appautoscaling_policy" "step_scaling_policy_scale_out" {
  name               = "SageMakerEndpointInvocationScalingPolicy-ScaleOut"
  policy_type        = "StepScaling"
  resource_id        = var.resource_id
  scalable_dimension = var.scalable_dimension
  service_namespace  = var.service_namespace

  step_scaling_policy_configuration {
    adjustment_type = "ChangeInCapacity"

    # change / add steps here
    step_adjustment {
      scaling_adjustment          = 1
      metric_interval_lower_bound = 0.0
    }

    metric_aggregation_type = "Average"
  }
}

resource "aws_cloudwatch_metric_alarm" "step_scaling_policy_scale_out_alarm" {
  alarm_name          = "StepScaling-${var.resource_id}-ScaleOut"
  metric_name         = "InvocationsPerInstance"
  namespace           = "AWS/SageMaker"
  statistic           = "Sum"
  period              = var.step_scaling_scale_out_period
  evaluation_periods  = var.step_scaling_scale_out_evaluation_periods
  threshold           = var.step_scaling_scale_out_threshold
  comparison_operator = "GreaterThanOrEqualToThreshold"

  dimensions = {
    EndpointName = var.endpoint_name
    VariantName  = var.variant_name
  }

  alarm_actions = [aws_appautoscaling_policy.step_scaling_policy_scale_out.arn]

  tags = var.tags
}

# scale in
resource "aws_appautoscaling_policy" "step_scaling_policy_scale_in" {
  name               = "SageMakerEndpointInvocationScalingPolicy-ScaleIn"
  policy_type        = "StepScaling"
  resource_id        = var.resource_id
  scalable_dimension = var.scalable_dimension
  service_namespace  = var.service_namespace

  step_scaling_policy_configuration {
    adjustment_type = "ChangeInCapacity"

    # change / add steps here
    step_adjustment {
      scaling_adjustment          = -1
      metric_interval_upper_bound = 0.0
    }

    metric_aggregation_type = "Average"
  }
}

resource "aws_cloudwatch_metric_alarm" "step_scaling_policy_scale_in_alarm" {
  alarm_name          = "StepScaling-${var.resource_id}-ScaleIn"
  metric_name         = "InvocationsPerInstance"
  namespace           = "AWS/SageMaker"
  statistic           = "Sum"
  period              = var.step_scaling_scale_in_period
  evaluation_periods  = var.step_scaling_scale_in_evaluation_periods
  threshold           = var.step_scaling_scale_in_threshold
  comparison_operator = "LessThanThreshold"

  dimensions = {
    EndpointName = var.endpoint_name
    VariantName  = var.variant_name
  }

  alarm_actions = [aws_appautoscaling_policy.step_scaling_policy_scale_in.arn]

  tags = var.tags
}