# general settings
namespace = "musicgen-project"
postfix   = "0001"

# elastic ip settings
create_elastic_ip = true

# ec2 settings
ami             = "ami-0810c2d824776b340"
instance_type   = "g4dn.xlarge"
public_key_path = "musicgen-key-ec2.ignore.pub"

root_block_delete_on_termination = true
root_block_volume_size           = 150