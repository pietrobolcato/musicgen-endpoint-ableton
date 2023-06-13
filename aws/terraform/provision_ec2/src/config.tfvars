# general settings
namespace = "ai-module"
postfix   = "0001"

# elastic ip settings
create_elastic_ip = true

# ec2 settings
ami             = "ami-05b22acc58f4e6494"
instance_type   = "g4dn.xlarge"
public_key_path = "ai-module-ec2-key.pub.ignore"

root_block_delete_on_termination = true
root_block_volume_size           = 150