(function () {
  const WS_URL = "wss://aaigentsv1.up.railway.app/ws/assemblyai_docs_agentt";

  let websocket = null;
  let audioContext = null;
  let playbackContext = null;
  let mediaStream = null;
  let mediaStreamSource = null;
  let scriptProcessor = null;
  let isConnected = false;
  let isSessionReady = false;
  let isRecording = false;
  let nextPlayTime = 0;
  let conversationItems = [];
  let chatboxElement = null;

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
    const searchButton = document.getElementById("fern-search-button");
    
    const anchorButton = askAIButton || searchButton;
    if (!anchorButton) {
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
      gap: 6px;
      padding: 0 12px;
      height: 36px;
      border-radius: 8px;
      border: 1px solid rgba(0, 0, 0, 0.1);
      background: white;
      cursor: pointer;
      margin-left: 8px;
      transition: all 0.2s ease;
      flex-shrink: 0;
      font-size: 14px;
      font-weight: 500;
      color: #374151;
    `;

    voiceButton.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
      </svg>
      <span>Ask Voice Agent</span>
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

    anchorButton.parentNode.insertBefore(
      voiceButton,
      anchorButton.nextSibling
    );
  }

  async function toggleVoiceAgent() {
    const button = document.getElementById("voice-agent-button");
    if (!button) return;

    if (isRecording) {
      stopVoiceAgent();
      button.style.background = "white";
      button.style.borderColor = "rgba(0, 0, 0, 0.1)";
      button.style.color = "#374151";
      button.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
        <span>Ask Voice Agent</span>
      `;
    } else {
      try {
        button.style.background = "#f59e0b";
        button.style.borderColor = "#f59e0b";
        button.style.color = "white";
        button.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
          <span>Connecting...</span>
        `;
        await startVoiceAgent();
      } catch (error) {
        console.error("Failed to start voice agent:", error);
        button.style.background = "white";
        button.style.borderColor = "rgba(0, 0, 0, 0.1)";
        button.style.color = "#374151";
        button.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
          <span>Ask Voice Agent</span>
        `;
        alert(
          "Failed to start voice agent. Please ensure microphone access is allowed."
        );
      }
    }
  }

  async function startVoiceAgent() {
    conversationItems = [];
    
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

    mediaStreamSource = audioContext.createMediaStreamSource(mediaStream);
    scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);

    scriptProcessor.onaudioprocess = (event) => {
      if (!isSessionReady || !isRecording) return;

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

    websocket = new WebSocket(WS_URL);

    websocket.onopen = () => {
      console.log("Voice agent connected, waiting for session.created...");
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

    isRecording = true;
    showChatbox();
  }

  function startAudioCapture() {
    if (mediaStreamSource && scriptProcessor) {
      mediaStreamSource.connect(scriptProcessor);
      scriptProcessor.connect(audioContext.destination);
      console.log("Audio capture started - now sending audio to server");
    }
  }

  function stopVoiceAgent() {
    isRecording = false;
    isConnected = false;
    isSessionReady = false;

    if (scriptProcessor) {
      scriptProcessor.disconnect();
      scriptProcessor = null;
    }

    if (mediaStreamSource) {
      mediaStreamSource.disconnect();
      mediaStreamSource = null;
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

    if (playbackContext) {
      playbackContext.close();
      playbackContext = null;
    }

    nextPlayTime = 0;
    hideChatbox();
  }

  function updateButtonToDisconnect() {
    const button = document.getElementById("voice-agent-button");
    if (button) {
      button.style.background = "#ef4444";
      button.style.borderColor = "#ef4444";
      button.style.color = "white";
      button.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
        <span>Disconnect</span>
      `;
    }
  }

  function handleServerMessage(message) {
    switch (message.type) {
      case "session.created":
        console.log("Session created:", message.session);
        isSessionReady = true;
        startAudioCapture();
        updateButtonToDisconnect();
        break;
      case "conversation.item.done":
        const item = message.item;
        if (item && item.content && item.content.length > 0) {
          const text = item.content[0].text;
          console.log(`[${item.role}]: ${text}`);
          addConversationItem(item.role, text, false);
        }
        break;
      case "conversation.item.interim":
        const interimItem = message.item;
        if (
          interimItem &&
          interimItem.content &&
          interimItem.content.length > 0
        ) {
          const interimText = interimItem.content[0].text;
          console.log(`[${interimItem.role}] (interim): ${interimText}`);
          updateInterimItem(interimItem.role, interimText);
        }
        break;
      case "tool.call":
        console.log("Tool call received:", message);
        break;
      default:
        console.log("Unknown message type:", message.type);
    }
  }

  function showChatbox() {
    if (chatboxElement) return;

    const voiceButton = document.getElementById("voice-agent-button");
    if (!voiceButton) return;

    chatboxElement = document.createElement("div");
    chatboxElement.id = "voice-agent-chatbox";
    chatboxElement.style.cssText = `
      position: absolute;
      top: 100%;
      right: 0;
      margin-top: 8px;
      width: 320px;
      max-height: 300px;
      background: white;
      border: 1px solid rgba(0, 0, 0, 0.1);
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      overflow: hidden;
      z-index: 1000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    const header = document.createElement("div");
    header.style.cssText = `
      padding: 12px 16px;
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      font-weight: 600;
      font-size: 14px;
      color: #111827;
      display: flex;
      align-items: center;
      gap: 8px;
    `;
    header.innerHTML = `
      <span style="width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite;"></span>
      Voice Agent Active
    `;

    const messagesContainer = document.createElement("div");
    messagesContainer.id = "voice-agent-messages";
    messagesContainer.style.cssText = `
      padding: 12px 16px;
      max-height: 220px;
      overflow-y: auto;
      font-size: 13px;
      line-height: 1.5;
    `;
    messagesContainer.innerHTML = `
      <div style="color: #6b7280; text-align: center; padding: 20px 0;">
        Listening...
      </div>
    `;

    const style = document.createElement("style");
    style.textContent = `
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    `;

    chatboxElement.appendChild(style);
    chatboxElement.appendChild(header);
    chatboxElement.appendChild(messagesContainer);

    const buttonParent = voiceButton.parentNode;
    buttonParent.style.position = "relative";
    buttonParent.appendChild(chatboxElement);
  }

  function hideChatbox() {
    if (chatboxElement) {
      chatboxElement.remove();
      chatboxElement = null;
    }
    conversationItems = [];
  }

  function addConversationItem(role, text, isInterim) {
    const messagesContainer = document.getElementById("voice-agent-messages");
    if (!messagesContainer) return;

    const interimElement = messagesContainer.querySelector(".interim-message");
    if (interimElement) {
      interimElement.remove();
    }

    if (messagesContainer.querySelector('[style*="Listening"]')) {
      messagesContainer.innerHTML = "";
    }

    const messageDiv = document.createElement("div");
    messageDiv.style.cssText = `
      margin-bottom: 12px;
      padding: 8px 12px;
      border-radius: 8px;
      ${role === "user" 
        ? "background: #f3f4f6; margin-left: 20px;" 
        : "background: #eff6ff; margin-right: 20px; border-left: 3px solid #3b82f6;"}
    `;

    const roleLabel = document.createElement("div");
    roleLabel.style.cssText = `
      font-size: 11px;
      font-weight: 600;
      color: ${role === "user" ? "#6b7280" : "#3b82f6"};
      margin-bottom: 4px;
      text-transform: uppercase;
    `;
    roleLabel.textContent = role === "user" ? "You" : "Assistant";

    const textDiv = document.createElement("div");
    textDiv.style.cssText = `color: #374151;`;
    textDiv.textContent = text;

    messageDiv.appendChild(roleLabel);
    messageDiv.appendChild(textDiv);
    messagesContainer.appendChild(messageDiv);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    conversationItems.push({ role, text });
  }

  function updateInterimItem(role, text) {
    const messagesContainer = document.getElementById("voice-agent-messages");
    if (!messagesContainer) return;

    if (messagesContainer.querySelector('[style*="Listening"]')) {
      messagesContainer.innerHTML = "";
    }

    let interimElement = messagesContainer.querySelector(".interim-message");
    
    if (!interimElement) {
      interimElement = document.createElement("div");
      interimElement.className = "interim-message";
      interimElement.style.cssText = `
        margin-bottom: 12px;
        padding: 8px 12px;
        border-radius: 8px;
        opacity: 0.7;
        ${role === "user" 
          ? "background: #f3f4f6; margin-left: 20px;" 
          : "background: #eff6ff; margin-right: 20px; border-left: 3px solid #3b82f6;"}
      `;

      const roleLabel = document.createElement("div");
      roleLabel.className = "interim-role";
      roleLabel.style.cssText = `
        font-size: 11px;
        font-weight: 600;
        color: ${role === "user" ? "#6b7280" : "#3b82f6"};
        margin-bottom: 4px;
        text-transform: uppercase;
      `;
      roleLabel.textContent = role === "user" ? "You" : "Assistant";

      const textDiv = document.createElement("div");
      textDiv.className = "interim-text";
      textDiv.style.cssText = `color: #374151;`;

      interimElement.appendChild(roleLabel);
      interimElement.appendChild(textDiv);
      messagesContainer.appendChild(interimElement);
    }

    const textDiv = interimElement.querySelector(".interim-text");
    if (textDiv) {
      textDiv.textContent = text + "...";
    }

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function playAudio(arrayBuffer) {
    try {
      if (!playbackContext) {
        playbackContext = new (window.AudioContext || window.webkitAudioContext)({
          sampleRate: 16000,
        });
        nextPlayTime = playbackContext.currentTime;
      }

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

      const currentTime = playbackContext.currentTime;
      
      // If we're too far behind (queue backed up), catch up to reduce latency
      // Allow a small buffer (50ms) for smooth playback
      if (nextPlayTime < currentTime) {
        nextPlayTime = currentTime;
      } else if (nextPlayTime > currentTime + 0.3) {
        // If queue is more than 300ms ahead, reset to reduce latency
        console.log("Audio queue backed up, resetting to reduce latency");
        nextPlayTime = currentTime + 0.05;
      }
      
      source.start(nextPlayTime);
      nextPlayTime = nextPlayTime + audioBuffer.duration;
    } catch (error) {
      console.error("Error playing audio:", error);
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
        const voiceButton = document.getElementById("voice-agent-button");
        if (!voiceButton) {
          const askAIButton = findAskAIButton();
          const searchButton = document.getElementById("fern-search-button");
          if (askAIButton || searchButton) {
            createVoiceAgentButton();
          }
        }
      }
    }
  });

  observer.observe(document.body || document.documentElement, {
    childList: true,
    subtree: true,
  });
})();
