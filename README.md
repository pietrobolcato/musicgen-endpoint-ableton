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

1. Login to AWS: `aws sso login`

2. Create the `dev` environment and activate it:

  ```bash
  conda env create -n dev -f envs/dev.yaml
  conda activate dev
  ```

3. Download the model artifacts: 
  
  ```bash
  cd aws/endpoint/src/artifacts/
  python download_artifacts.py
  ```

4. Create the model tar gz: 
  ```
  cd aws/endpoint/model/
  bash create_tar.sh
  ```

5. Build and publish the custom docker image for the endpoint:

  ```
  cd aws/endpoint/container/
  bash build_and_publish.sh
  ```

6. Update the deployment notebook `aws/endpoint/notebooks/deployment.ipynb`, to reflect
the url of the image published in `step 5`, and use it to register the model.

7. Change the configuration in `aws/terraform/provision_ec2/src/config-dev.yaml` and
`aws/terraform/provision_ec2/src/config-prod.yaml`. Also update the `main.tf`
backend as needed, especially in the terraform state `key`. Finally, change
`locals.tf` as needed.

8. Use github actions defined in `.github/workflows/` to execute the CD pipeline and
provision / destroy the endpoint.