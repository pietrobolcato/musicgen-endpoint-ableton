locals {
  endpoint_name = aws_sagemaker_endpoint.sagemaker_endpoint.name
  variant_name  = aws_sagemaker_endpoint_configuration.sagemaker_endpoint_configuration.production_variants[0].variant_name
  resource_id   = "endpoint/${local.endpoint_name}/variant/${local.variant_name}"
}

# s3 bucket for data capture - if enabled
resource "aws_s3_bucket" "data_capture_bucket" {
  count = var.create_s3_bucket ? 1 : 0

  bucket        = var.s3_bucket_name
  force_destroy = var.s3_bucket_force_destroy

  tags = local.tags
}

# sagemaker model
resource "aws_sagemaker_model" "sagemaker_model" {
  name               = "model-${var.namespace}-${var.postfix}-${var.environment}"
  execution_role_arn = var.execution_role_arn

  primary_container {
    mode               = "SingleModel"
    model_package_name = var.model_arn
  }

  tags = local.tags
}

# sagemaker endpoint configuration
resource "aws_sagemaker_endpoint_configuration" "sagemaker_endpoint_configuration" {
  name = "epc-${var.namespace}-${var.postfix}-${var.environment}"

  production_variants {
    initial_instance_count = var.instance_count
    instance_type          = var.instance_type
    model_name             = aws_sagemaker_model.sagemaker_model.name
    variant_name           = "AllTraffic"
  }

  data_capture_config {
    enable_capture              = var.enable_data_capture
    initial_sampling_percentage = var.sampling_percentage
    destination_s3_uri          = var.enable_data_capture ? var.data_capture_s3_upload_path : "s3://."

    capture_options {
      capture_mode = "Input"
    }

    capture_options {
      capture_mode = "Output"
    }
  }

  tags = local.tags
}

# sagemaker realtime endpoint
resource "aws_sagemaker_endpoint" "sagemaker_endpoint" {
  name                 = "endpoint-${var.namespace}-${var.postfix}-${var.environment}"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.sagemaker_endpoint_configuration.name

  tags = local.tags
}

# autoscaling settings
resource "aws_appautoscaling_target" "endpoint_autoscaling_target" {
  count = var.enable_autoscaling ? 1 : 0

  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = local.resource_id
  scalable_dimension = "sagemaker:variant:DesiredInstanceCount"
  service_namespace  = "sagemaker"

  tags = local.tags
}

# target tracking policy
module "target_tracking_scaling_policy" {
  source = "./modules/autoscaling/target_tracking"

  count = var.enable_autoscaling && var.autoscaling_type == "target_tracking" ? 1 : 0

  resource_id        = aws_appautoscaling_target.endpoint_autoscaling_target[count.index].resource_id
  scalable_dimension = aws_appautoscaling_target.endpoint_autoscaling_target[count.index].scalable_dimension
  service_namespace  = aws_appautoscaling_target.endpoint_autoscaling_target[count.index].service_namespace

  policy_target_value = var.policy_target_value
  scale_out_cooldown  = var.scale_out_cooldown
  scale_in_cooldown   = var.scale_in_cooldown
}

# step scaling policy
module "step_scaling_policy" {
  source = "./modules/autoscaling/step_scaling"

  count = var.enable_autoscaling && var.autoscaling_type == "step_scaling" ? 1 : 0

  resource_id        = aws_appautoscaling_target.endpoint_autoscaling_target[count.index].resource_id
  scalable_dimension = aws_appautoscaling_target.endpoint_autoscaling_target[count.index].scalable_dimension
  service_namespace  = aws_appautoscaling_target.endpoint_autoscaling_target[count.index].service_namespace

  endpoint_name = local.endpoint_name
  variant_name  = local.variant_name

  step_scaling_scale_out_threshold          = var.step_scaling_scale_out_threshold
  step_scaling_scale_out_period             = var.step_scaling_scale_out_period
  step_scaling_scale_out_evaluation_periods = var.step_scaling_scale_out_evaluation_periods

  step_scaling_scale_in_threshold          = var.step_scaling_scale_in_threshold
  step_scaling_scale_in_period             = var.step_scaling_scale_in_period
  step_scaling_scale_in_evaluation_periods = var.step_scaling_scale_in_evaluation_periods

  tags = local.tags
}