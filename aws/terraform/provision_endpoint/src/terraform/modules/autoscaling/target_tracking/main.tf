# target tracking policy settings
resource "aws_appautoscaling_policy" "target_tracking_scaling_policy" {
  name               = "SageMakerEndpointInvocationScalingPolicy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = var.resource_id
  scalable_dimension = var.scalable_dimension
  service_namespace  = var.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = var.policy_target_value
    scale_in_cooldown  = var.scale_in_cooldown
    scale_out_cooldown = var.scale_out_cooldown

    predefined_metric_specification {
      predefined_metric_type = "SageMakerVariantInvocationsPerInstance"
    }
  }
}
