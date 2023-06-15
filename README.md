# Musicgen Endpoint for Ableton 

This repo implements [Meta's Musicgen](https://github.com/facebookresearch/audiocraft) — 
a state of the art text to music model — as scalable online endpoint in AWS Sagemaker.

It provides:
- The code to provision the endpoint, as well as a CD pipeline to provision it 
automatically
- A lambda function to publicly access the endpoint
- A [Max4Live](https://www.ableton.com/en/live/max-for-live/) device to perform the 
inference inside Ableton Live, enabling to use the model as part of a music production
workflow.

## Get started

1.  Login to AWS:

    ```
    aws sso login
    ```
2.  Change the configuration in `aws/terraform/provision_ec2/src/config-dev.yaml` and
    `aws/terraform/provision_ec2/src/config-prod.yaml`. Also update the `main.tf`
    backend as needed, especially in the terraform state `key`. Finally, change
    `locals.tf` as needed.

3.  Use github actions defined in `.github/workflows/` to execute the CD pipeline and
    provision / destroy the endpoint.

4. TODO