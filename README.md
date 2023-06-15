# 🎶🌈 MetaAI Musicgen — AWS Endpoint + Ableton integration

This repository implements [Musicgen](https://github.com/facebookresearch/audiocraft), 
a state of the art text-to-music model, as a scalable online endpoint in AWS Sagemaker. 
It includes a lambda function to enable public access to the endpoint, as well as a 
[Max4Live](https://www.ableton.com/en/live/max-for-live/) device that allows to 
perform inference right within Ableton Live, seamlessly integrating the model into 
any music production workflow. 

Check out the demo below! Audio on! 🔊🔽

https://github.com/pietrobolcato/musicgen-endpoint-ableton/assets/3061306/4640ae7c-a8a0-4875-beb5-8f9479ab4e26

## Get started

1.  Login to AWS: `aws sso login`

2.  Change the configuration in `aws/terraform/provision_ec2/src/config-dev.yaml` and
    `aws/terraform/provision_ec2/src/config-prod.yaml`. Also update the `main.tf`
    backend as needed, especially in the terraform state `key`. Finally, change
    `locals.tf` as needed.

3.  Use github actions defined in `.github/workflows/` to execute the CD pipeline and
    provision / destroy the endpoint.

4. Sta
