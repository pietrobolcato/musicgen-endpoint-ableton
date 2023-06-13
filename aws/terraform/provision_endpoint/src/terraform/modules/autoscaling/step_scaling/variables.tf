# scale out settings
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

# scale in settings
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

# autoscaling target settings
variable "resource_id" {
  type        = string
  description = "The identifier of the resource associated with the scaling policy. This string consists of the resource type and unique identifier"
}

variable "scalable_dimension" {
  type        = string
  description = "The scalable dimension. This string consists of the service namespace, resource type, and scaling property"
}

variable "service_namespace" {
  type        = string
  description = "The namespace of the Amazon Web Services service that provides the resource"
}

variable "endpoint_name" {
  type        = string
  description = "The name of the endpoint"
}

variable "variant_name" {
  type        = string
  description = "The name of the endpoint variant"
}

# other
variable "tags" {
  type        = map(string)
  default     = {}
  description = "A mapping of tags which should be assigned to the deployed resource"
}