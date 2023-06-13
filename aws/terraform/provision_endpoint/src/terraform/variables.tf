# general settings
variable "namespace" {
  type        = string
  description = "The namespace, used as prefix for resources names"
}

variable "postfix" {
  type        = string
  description = "Postfix for modules names"
}

variable "environment" {
  type        = string
  description = "Environment, generally either `dev`, `stage`, `prod`"
}

# model settings
variable "execution_role_arn" {
  type        = string
  description = "Execution IAM role used for deploying the model"
}

variable "model_arn" {
  type        = string
  description = "The ARN of the registered model"
}

# endpoint configuration settings
variable "instance_type" {
  type        = string
  default     = "ml.t2.medium"
  description = "The ML compute instance type for the endpoint"
}

variable "instance_count" {
  type        = number
  default     = 1
  description = "Number of instances to launch for the endpoint"
}

# data capture settings
variable "enable_data_capture" {
  type        = bool
  default     = true
  description = "Boolean that activate or deactivate data capture"
}

variable "create_s3_bucket" {
  type        = bool
  default     = false
  description = "If set to true, creates the s3 bucket for data capture, with the name set in the `s3_bucket_name` variable"
}

variable "s3_bucket_name" {
  type        = string
  default     = ""
  description = "The name of the `s3_bucket_name` to create, if `create_s3_bucket` is set to `true`"
}

variable "s3_bucket_force_destroy" {
  type        = bool
  default     = false
  description = "If true, empties the s3 bucket used for data capture before destroying the endpoint. If set to `false`, it will not empty the bucket automatically, and `terraform destroy` will fail if run while the bucket has objects inside it"
}

variable "sampling_percentage" {
  type        = number
  default     = 100
  description = "Portion of data to capture. Should be between 0 and 100"

  validation {
    condition     = var.sampling_percentage >= 0 && var.sampling_percentage <= 100
    error_message = "The sampling percentage should be between 0 and 100"
  }
}

variable "data_capture_s3_upload_path" {
  type        = string
  default     = ""
  description = "The s3 bucket location where to upload the captured data"
}

# autoscaling settings
variable "enable_autoscaling" {
  type        = bool
  default     = false
  description = "Boolean that activate or deactivate endpoint autoscaling"
}

variable "autoscaling_type" {
  type    = string
  default = ""

  validation {
    condition     = contains(["target_tracking", "step_scaling", ""], var.autoscaling_type)
    error_message = "Allowed values for input_parameter are: `target_tracking`, `step_scaling`, ``"
  }
}

variable "min_capacity" {
  type        = number
  default     = 1
  description = "Min number of instances running"
}

variable "max_capacity" {
  type        = number
  default     = 2
  description = "Max number of instances running"
}

# target tracking policy settings
variable "policy_target_value" {
  type        = number
  default     = 1
  description = "The autoscaling policy target value for `SageMakerVariantInvocationsPerInstance`"
}

variable "scale_out_cooldown" {
  type        = number
  default     = 300
  description = "The time in seconds for the scale-out cooldown"
}

variable "scale_in_cooldown" {
  type        = number
  default     = 300
  description = "The time in seconds for the scale-in cooldown"
}

# step scaling policy settings
# scale out
variable "step_scaling_scale_out_threshold" {
  type        = number
  default     = 1
  description = "The threshold for `SageMakerVariantInvocationsPerInstance` of scale out step scaling policy"
}

variable "step_scaling_scale_out_period" {
  type        = number
  default     = 60
  description = "The metric period for the scale out policy"
}

variable "step_scaling_scale_out_evaluation_periods" {
  type        = number
  default     = 1
  description = "The metric evaluation periods for the scale out policy"
}

# scale in
variable "step_scaling_scale_in_threshold" {
  type        = number
  default     = 1
  description = "The threshold for `SageMakerVariantInvocationsPerInstance` of scale in step scaling policy"
}

variable "step_scaling_scale_in_period" {
  type        = number
  default     = 60
  description = "The metric period for the scale in policy"
}

variable "step_scaling_scale_in_evaluation_periods" {
  type        = number
  default     = 1
  description = "The metric evaluation periods for the scale in policy"
}