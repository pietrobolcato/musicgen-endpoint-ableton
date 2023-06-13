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