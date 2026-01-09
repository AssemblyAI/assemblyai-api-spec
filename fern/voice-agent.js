(function () {
  const WS_URL = "wss://aaigentsv1.up.railway.app/ws/assemblyai_docs_agent";

  let websocket = null;
  let audioContext = null;
  let mediaStream = null;
  let scriptProcessor = null;
  let isConnected = false;
  let isRecording = false;
  let audioQueue = [];
  let isPlaying = false;

  function findAskAIButton() {
    const buttons = document.querySelectorAll("button");
    for (const button of buttons) {
      if (button.textContent && button.textContent.includes("Ask AI")) {
        return button;
      }
    }
    return null;
  }

  function createVoiceAgentButton() {
    const existingButton = document.getElementById("voice-agent-button");
    if (existingButton) {
      return;
    }

    const askAIButton = findAskAIButton();
    if (!askAIButton) {
      return;
    }

    const voiceButton = document.createElement("button");
    voiceButton.id = "voice-agent-button";
    voiceButton.type = "button";
    voiceButton.title = "Talk to AI Assistant";
    voiceButton.setAttribute("aria-label", "Talk to AI Assistant");

    voiceButton.style.cssText = `
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: 8px;
      border: 1px solid rgba(0, 0, 0, 0.1);
      background: white;
      cursor: pointer;
      margin-left: 8px;
      transition: all 0.2s ease;
      flex-shrink: 0;
    `;

    voiceButton.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
      </svg>
    `;

    voiceButton.addEventListener("mouseenter", () => {
      if (!isRecording) {
        voiceButton.style.background = "#f5f5f5";
      }
    });

    voiceButton.addEventListener("mouseleave", () => {
      if (!isRecording) {
        voiceButton.style.background = "white";
      }
    });

    voiceButton.addEventListener("click", toggleVoiceAgent);

    askAIButton.parentNode.insertBefore(
      voiceButton,
      askAIButton.nextSibling
    );
  }

  async function toggleVoiceAgent() {
    const button = document.getElementById("voice-agent-button");
    if (!button) return;

    if (isRecording) {
      stopVoiceAgent();
      button.style.background = "white";
      button.style.borderColor = "rgba(0, 0, 0, 0.1)";
      button.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      `;
    } else {
      try {
        await startVoiceAgent();
        button.style.background = "#ef4444";
        button.style.borderColor = "#ef4444";
        button.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        `;
      } catch (error) {
        console.error("Failed to start voice agent:", error);
        alert(
          "Failed to start voice agent. Please ensure microphone access is allowed."
        );
      }
    }
  }

  async function startVoiceAgent() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: 16000,
    });

    mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: 16000,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      },
    });

    websocket = new WebSocket(WS_URL);

    websocket.onopen = () => {
      console.log("Voice agent connected");
      isConnected = true;
    };

    websocket.onmessage = async (event) => {
      if (event.data instanceof Blob) {
        const arrayBuffer = await event.data.arrayBuffer();
        playAudio(arrayBuffer);
      } else {
        try {
          const message = JSON.parse(event.data);
          handleServerMessage(message);
        } catch (e) {
          console.log("Received non-JSON message:", event.data);
        }
      }
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    websocket.onclose = () => {
      console.log("Voice agent disconnected");
      isConnected = false;
      stopVoiceAgent();
    };

    const source = audioContext.createMediaStreamSource(mediaStream);
    scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);

    scriptProcessor.onaudioprocess = (event) => {
      if (!isConnected || !isRecording) return;

      const inputData = event.inputBuffer.getChannelData(0);
      const pcm16 = new Int16Array(inputData.length);

      for (let i = 0; i < inputData.length; i++) {
        const s = Math.max(-1, Math.min(1, inputData[i]));
        pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
      }

      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(pcm16.buffer);
      }
    };

    source.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);

    isRecording = true;
  }

  function stopVoiceAgent() {
    isRecording = false;
    isConnected = false;

    if (scriptProcessor) {
      scriptProcessor.disconnect();
      scriptProcessor = null;
    }

    if (mediaStream) {
      mediaStream.getTracks().forEach((track) => track.stop());
      mediaStream = null;
    }

    if (websocket) {
      websocket.close();
      websocket = null;
    }

    if (audioContext) {
      audioContext.close();
      audioContext = null;
    }

    audioQueue = [];
    isPlaying = false;
  }

  function handleServerMessage(message) {
    switch (message.type) {
      case "session.created":
        console.log("Session created:", message.session);
        break;
      case "conversation.item.done":
        const item = message.item;
        if (item && item.content && item.content.length > 0) {
          console.log(`[${item.role}]: ${item.content[0].text}`);
        }
        break;
      case "conversation.item.interim":
        const interimItem = message.item;
        if (
          interimItem &&
          interimItem.content &&
          interimItem.content.length > 0
        ) {
          console.log(`[${interimItem.role}] (interim): ${interimItem.content[0].text}`);
        }
        break;
      case "tool.call":
        console.log("Tool call received:", message);
        break;
      default:
        console.log("Unknown message type:", message.type);
    }
  }

  async function playAudio(arrayBuffer) {
    audioQueue.push(arrayBuffer);
    if (!isPlaying) {
      processAudioQueue();
    }
  }

  async function processAudioQueue() {
    if (audioQueue.length === 0) {
      isPlaying = false;
      return;
    }

    isPlaying = true;
    const arrayBuffer = audioQueue.shift();

    try {
      const playbackContext = new (window.AudioContext ||
        window.webkitAudioContext)({
        sampleRate: 16000,
      });

      const int16Array = new Int16Array(arrayBuffer);
      const float32Array = new Float32Array(int16Array.length);

      for (let i = 0; i < int16Array.length; i++) {
        float32Array[i] = int16Array[i] / 32768.0;
      }

      const audioBuffer = playbackContext.createBuffer(
        1,
        float32Array.length,
        16000
      );
      audioBuffer.getChannelData(0).set(float32Array);

      const source = playbackContext.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(playbackContext.destination);

      source.onended = () => {
        playbackContext.close();
        processAudioQueue();
      };

      source.start(0);
    } catch (error) {
      console.error("Error playing audio:", error);
      processAudioQueue();
    }
  }

  function init() {
    createVoiceAgentButton();
  }

  document.addEventListener("DOMContentLoaded", init);

  if (
    document.readyState === "complete" ||
    document.readyState === "interactive"
  ) {
    init();
  }

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === "childList") {
        const askAIButton = findAskAIButton();
        const voiceButton = document.getElementById("voice-agent-button");
        if (askAIButton && !voiceButton) {
          createVoiceAgentButton();
        }
      }
    }
  });

  observer.observe(document.body || document.documentElement, {
    childList: true,
    subtree: true,
  });
})();
