docker run --gpus all -p 8000:8000 \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -v /absolute/local/path/to/license.jwt:/app/license.jwt \
  344839248844.dkr.ecr.us-west-2.amazonaws.com/self-hosted-ml-prod:release-v0.6
