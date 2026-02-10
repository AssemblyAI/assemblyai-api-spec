# Authenticate with ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 344839248844.dkr.ecr.us-west-2.amazonaws.com

# Create project directory
mkdir -p ~/assemblyai-streaming
cd ~/assemblyai-streaming

# Create .env file with image references
cat > .env << 'EOF'
STREAMING_API_IMAGE=344839248844.dkr.ecr.us-west-2.amazonaws.com/self-hosted-streaming-api:release-v0.4.0
STREAMING_ASR_ENGLISH_IMAGE=344839248844.dkr.ecr.us-west-2.amazonaws.com/self-hosted-streaming-asr-english:release-v0.4.0
STREAMING_ASR_MULTILANG_IMAGE=344839248844.dkr.ecr.us-west-2.amazonaws.com/self-hosted-streaming-asr-multilang:release-v0.4.0
LICENSE_AND_USAGE_PROXY_IMAGE=344839248844.dkr.ecr.us-west-2.amazonaws.com/self-hosted-streaming-license-and-usage-proxy:release-v0.4.0
USAGE_TRACKING_API_KEY=<your_usage_tracking_api_key_here>
EOF

# Create docker-compose.yml file
# Copy the complete docker-compose.yml content from the Configuration section above and save it
# Or download it from the GitHub repository

# Create nginx configuration file
# Copy the nginx_streaming_asr.conf content from the Configuration section above and save it
# Or download it from the GitHub repository

# Start services
docker compose up -d

# Monitor logs (services may take 2-3 minutes to fully start)
docker compose logs -f
