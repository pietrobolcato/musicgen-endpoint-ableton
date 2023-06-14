FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.0-gpu-py310

# uninstall current torch, torchaudio and torchvision
RUN pip uninstall --yes torch torchaudio torchvision

# re-install it using audiocraft, alongside the right version of xformers
RUN pip install audiocraft~=0.0.1