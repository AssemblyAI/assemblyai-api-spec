import { AssemblyAI } from 'assemblyai';
import fs from 'fs';
import { spawn } from 'child_process';
import { Readable } from 'stream';

// Configuration
const YOUR_API_KEY = '<YOUR_API_KEY>';
const AUDIO_FILE_PATH = '<DUAL_CHANNEL_AUDIO_FILE_PATH>';

// Simple WAV file parser
class SimpleWavParser {
    constructor(filePath) {
        this.buffer = fs.readFileSync(filePath);
        this.parseHeader();
    }

    parseHeader() {
        // Read WAV header
        this.channels = this.buffer.readUInt16LE(22);
        this.sampleRate = this.buffer.readUInt32LE(24);
        this.bitsPerSample = this.buffer.readUInt16LE(34);
        
        // Find data chunk
        let dataOffset = 12;
        while (dataOffset < this.buffer.length - 8) {
            const chunkId = this.buffer.toString('ascii', dataOffset, dataOffset + 4);
            const chunkSize = this.buffer.readUInt32LE(dataOffset + 4);
            
            if (chunkId === 'data') {
                this.dataStart = dataOffset + 8;
                this.dataSize = chunkSize;
                break;
            }
            
            dataOffset += 8 + chunkSize;
        }
    }

    getChannelData(channelIndex) {
        if (this.channels !== 2) {
            throw new Error('Audio file is not stereo');
        }

        const bytesPerSample = this.bitsPerSample / 8;
        const samplesPerChannel = this.dataSize / (bytesPerSample * this.channels);
        const channelData = [];

        // Extract samples for the specified channel
        for (let i = 0; i < samplesPerChannel; i++) {
            const sampleOffset = this.dataStart + (i * this.channels + channelIndex) * bytesPerSample;
            
            if (this.bitsPerSample === 16) {
                const sample = this.buffer.readInt16LE(sampleOffset);
                channelData.push(sample);
            } else if (this.bitsPerSample === 8) {
                const sample = this.buffer.readUInt8(sampleOffset) - 128;
                channelData.push(sample * 256); // Convert to 16-bit range
            }
        }

        return channelData;
    }
}

class ChannelTranscriber {
    constructor(client, channelId, channelName, sampleRate) {
        this.client = client;
        this.channelId = channelId;
        this.channelName = channelName;
        this.sampleRate = sampleRate;
        this.transcriber = null;
        this.audioData = [];
        this.currentTurnLine = null;
        this.lineCount = 0;
    }

    loadAudioChannel() {
        try {
            const wavParser = new SimpleWavParser(AUDIO_FILE_PATH);
            const channelSamples = wavParser.getChannelData(this.channelId);
            
            // Split into chunks for streaming (50ms chunks)
            const FRAMES_PER_BUFFER = Math.floor(this.sampleRate * 0.05); // 50ms
            
            for (let i = 0; i < channelSamples.length; i += FRAMES_PER_BUFFER) {
                const chunkArray = new Int16Array(FRAMES_PER_BUFFER);
                
                // Copy samples and pad if necessary
                for (let j = 0; j < FRAMES_PER_BUFFER; j++) {
                    if (i + j < channelSamples.length) {
                        chunkArray[j] = channelSamples[i + j];
                    } else {
                        chunkArray[j] = 0; // Pad with silence
                    }
                }
                
                // Convert to Buffer (Little Endian)
                const buffer = Buffer.from(chunkArray.buffer);
                this.audioData.push(buffer);
            }
        } catch (error) {
            throw error;
        }
    }

    clearCurrentLine() {
        if (this.currentTurnLine !== null) {
            process.stdout.write('\r' + ' '.repeat(100) + '\r');
        }
    }

    printPartialTranscript(words) {
        this.clearCurrentLine();
        // Build transcript from individual words
        const wordTexts = words.map(word => word.text || '');
        const transcript = wordTexts.join(' ');
        const partialText = `${this.channelName}: ${transcript}`;
        process.stdout.write(partialText);
        this.currentTurnLine = partialText.length;
    }

    printFinalTranscript(transcript) {
        this.clearCurrentLine();
        const finalText = `${this.channelName}: ${transcript}`;
        console.log(finalText);
        this.currentTurnLine = null;
        this.lineCount++;
    }

    async startTranscription() {
        try {
            this.loadAudioChannel();
        } catch (error) {
            throw error;
        }

        const turnDetectionConfig = {
          endOfTurnConfidenceThreshold: 0.4,
          minEndOfTurnSilenceWhenConfident: 160,
          maxTurnSilence: 400
        };

        // Create transcriber with SDK
        this.transcriber = this.client.streaming.transcriber({
            sampleRate: this.sampleRate,
            formatTurns: true,
            ...turnDetectionConfig
        });

        // Set up event handlers
        this.transcriber.on('open', ({ id }) => {
            // Session opened
        });

        this.transcriber.on('error', (error) => {
            console.error(`\n${this.channelName}: Error:`, error);
        });

        this.transcriber.on('close', (code, reason) => {
            this.clearCurrentLine();
            if (code !== 1000 && code !== 1001) {
                console.log(`\n${this.channelName}: Connection closed unexpectedly`);
            }
        });

        this.transcriber.on('turn', (turn) => {
            const transcript = (turn.transcript || '').trim();
            const formatted = turn.turn_is_formatted || false;
            const words = turn.words || [];
            
            if (transcript || words.length > 0) {
                if (formatted) {
                    this.printFinalTranscript(transcript);
                } else {
                    this.printPartialTranscript(words);
                }
            }
        });

        // Connect to the streaming service
        await this.transcriber.connect();

        // Create a readable stream from audio chunks
        const audioStream = new Readable({
            async read() {
                // This will be controlled by our manual push below
            }
        });

        // Pipe audio stream to transcriber
        Readable.toWeb(audioStream).pipeTo(this.transcriber.stream());

        // Stream audio data
        for (const chunk of this.audioData) {
            audioStream.push(chunk);
            await new Promise(resolve => setTimeout(resolve, 50)); // 50ms intervals
        }

        // Signal end of stream
        audioStream.push(null);

        // Wait a bit for final transcripts
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Close the transcriber
        await this.transcriber.close();
    }

    async close() {
        if (this.transcriber) {
            await this.transcriber.close();
        }
    }
}

function playAudioFile() {
    return new Promise((resolve) => {
        console.log(`Playing audio: ${AUDIO_FILE_PATH}`);
        
        // Use platform-specific audio player
        let command;
        let args;
        
        if (process.platform === 'darwin') {
            // macOS
            command = 'afplay';
            args = [AUDIO_FILE_PATH];
        } else if (process.platform === 'win32') {
            // Windows - using PowerShell
            command = 'powershell';
            args = ['-c', `(New-Object Media.SoundPlayer '${AUDIO_FILE_PATH}').PlaySync()`];
        } else {
            // Linux - try aplay
            command = 'aplay';
            args = [AUDIO_FILE_PATH];
        }
        
        try {
            const player = spawn(command, args, {
                stdio: ['ignore', 'ignore', 'ignore'] // Suppress all output from player
            });
            
            player.on('close', (code) => {
                if (code === 0) {
                    console.log('Audio playback finished');
                }
                resolve();
            });
            
            player.on('error', (error) => {
                // Silently continue without audio
                resolve();
            });
        } catch (error) {
            resolve();
        }
    });
}

async function transcribeMultichannel() {
    // Verify API key is set
    if (YOUR_API_KEY === '<YOUR_API_KEY>') {
        console.error('ERROR: Please set YOUR_API_KEY before running');
        process.exit(1);
    }
    
    // Verify file exists
    if (!fs.existsSync(AUDIO_FILE_PATH)) {
        console.error(`ERROR: Audio file not found: ${AUDIO_FILE_PATH}`);
        process.exit(1);
    }

    // Get sample rate from file
    const wavParser = new SimpleWavParser(AUDIO_FILE_PATH);
    const sampleRate = wavParser.sampleRate;

    // Create SDK client
    const client = new AssemblyAI({
        apiKey: YOUR_API_KEY
    });

    const transcriber1 = new ChannelTranscriber(client, 0, 'Speaker 1', sampleRate);
    const transcriber2 = new ChannelTranscriber(client, 1, 'Speaker 2', sampleRate);
    
    try {
        // Start audio playback (non-blocking)
        const audioPromise = playAudioFile();
        
        // Start both transcriptions
        const transcriptionPromises = [
            transcriber1.startTranscription(),
            transcriber2.startTranscription()
        ];
        
        // Wait for all to complete
        await Promise.all([...transcriptionPromises, audioPromise]);
        
    } catch (error) {
        console.error('\nError during transcription:', error.message);
        
        // Clean up
        await transcriber1.close();
        await transcriber2.close();
        
        process.exit(1);
    }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n'); // Clean line break before exit
    process.exit(0);
});

// Main execution
transcribeMultichannel();