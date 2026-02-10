# 1. Clone and install
git clone https://github.com/AssemblyAI/assemblyai-recallai-zoom-bot.git
cd assemblyai-recallai-zoom-bot
npm install

# 2. Run ngrok and copy the ngrok URL
# ngrok http 8000

# 3. Configure your .env file and edit it with your API keys and ngrok URL
cp .env.example .env

# 4a. Open a new terminal and run
# node webhook.js

# 4b. Open another terminal and run
# node zoomBot.js
