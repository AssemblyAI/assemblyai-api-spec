// Import required AWS SDK modules
import { S3 } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { GetObjectCommand } from "@aws-sdk/client-s3";

// Configure logging
const logger = {
  info: (data) => console.log(JSON.stringify(data)),
  error: (data) => console.error(JSON.stringify(data)),
};

// Configuration settings for AssemblyAI
// See config parameters here: https://www.assemblyai.com/docs/api-reference/transcripts/submit
const ASSEMBLYAI_CONFIG = {
  multichannel: true, // Using multichannel here as we told Genesys to send us multichannel audio.
};

// Initialize AWS S3 client
const s3Client = new S3();

/**
 * Generate a presigned URL for the S3 object
 * @param {string} bucket - S3 bucket name
 * @param {string} key - S3 object key
 * @param {number} expiration - URL expiration time in seconds
 * @returns {Promise<string>} Presigned URL
 */
const getPresignedUrl = async (bucket, key, expiration = 3600) => {
  logger.info({
    message: "Generating presigned URL",
    bucket: bucket,
    key: key,
    expiration: expiration,
  });

  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  return getSignedUrl(s3Client, command, { expiresIn: expiration });
};

/**
 * Delete transcript data from AssemblyAI's database
 * @param {string} transcriptId - The AssemblyAI transcript ID to delete
 * @param {string} apiKey - The AssemblyAI API key
 * @returns {Promise<boolean>} True if deletion was successful, False otherwise
 */
const deleteTranscriptFromAssemblyAI = async (transcriptId, apiKey) => {
  try {
    const response = await fetch(
      `https://api.assemblyai.com/v2/transcript/${transcriptId}`,
      {
        method: "DELETE",
        headers: {
          authorization: apiKey,
          "content-type": "application/json",
        },
      }
    );

    if (response.ok) {
      logger.info(
        `Successfully deleted transcript ${transcriptId} from AssemblyAI`
      );
      return true;
    } else {
      const errorData = await response.text();
      logger.error(
        `Failed to delete transcript ${transcriptId}: HTTP ${response.status} - ${errorData}`
      );
      return false;
    }
  } catch (error) {
    logger.error(`Error deleting transcript ${transcriptId}: ${error.message}`);
    return false;
  }
};

/**
 * Submit audio for transcription
 * @param {object} requestData - Request data including audio URL and config
 * @param {string} apiKey - AssemblyAI API key
 * @returns {Promise<string>} Transcript ID
 */
const submitTranscriptionRequest = async (requestData, apiKey) => {
  const response = await fetch("https://api.assemblyai.com/v2/transcript", {
    method: "POST",
    headers: {
      authorization: apiKey,
      "content-type": "application/json",
    },
    body: JSON.stringify(requestData),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to submit audio for transcription: ${errorText}`);
  }

  const responseData = await response.json();
  const transcriptId = responseData.id;

  logger.info({
    message: "Audio submitted for transcription",
    transcript_id: transcriptId,
  });

  return transcriptId;
};

/**
 * Poll for transcription completion
 * @param {string} transcriptId - Transcript ID
 * @param {string} apiKey - AssemblyAI API key
 * @returns {Promise<object>} Transcription data
 */
const pollTranscriptionStatus = async (transcriptId, apiKey) => {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // Keep polling until we get a completion or error
  while (true) {
    const response = await fetch(
      `https://api.assemblyai.com/v2/transcript/${transcriptId}`,
      {
        method: "GET",
        headers: {
          authorization: apiKey,
          "content-type": "application/json",
        },
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to poll transcription status: ${errorText}`);
    }

    const pollingData = await response.json();

    if (pollingData.status === "completed") {
      logger.info({ message: "Transcription completed successfully" });
      return pollingData;
    } else if (pollingData.status === "error") {
      throw new Error(`Transcription failed: ${pollingData.error}`);
    }

    // Wait before polling again
    await sleep(3000);
  }
};

/**
 * Transcribe audio using AssemblyAI API
 * @param {string} audioUrl - URL of the audio file
 * @param {string} apiKey - AssemblyAI API key
 * @returns {Promise<object>} Transcription data
 */
const transcribeAudio = async (audioUrl, apiKey) => {
  logger.info({ message: "Starting audio transcription" });

  // Prepare request data with config parameters
  const requestData = { audio_url: audioUrl, ...ASSEMBLYAI_CONFIG };

  // Submit the audio file for transcription
  const transcriptId = await submitTranscriptionRequest(requestData, apiKey);

  // Poll for transcription completion
  return await pollTranscriptionStatus(transcriptId, apiKey);
};

/**
 * Lambda function handler
 * @param {object} event - S3 event
 * @param {object} context - Lambda context
 * @returns {Promise<object>} Response
 */
export const handler = async (event, context) => {
  try {
    // Get the AssemblyAI API key from environment variables
    const apiKey = process.env.ASSEMBLYAI_API_KEY;
    if (!apiKey) {
      throw new Error("ASSEMBLYAI_API_KEY environment variable is not set");
    }

    // Process each record in the S3 event
    const records = event.Records || [];

    for (const record of records) {
      // Get the S3 bucket and key
      const bucket = record.s3.bucket.name;
      const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, " "));

      // Generate a presigned URL for the audio file
      const audioUrl = await getPresignedUrl(bucket, key);

      // Get the full transcript JSON from AssemblyAI
      const transcriptData = await transcribeAudio(audioUrl, apiKey);

      // Prepare the transcript key - maintaining path structure but changing directory and extension
      const transcriptKey = key
        .replace("audio", "transcripts", 1)
        .replace(".wav", ".json");

      // Convert the JSON data to a string
      const transcriptJsonStr = JSON.stringify(transcriptData, null, 2);

      // Upload the transcript JSON to the same bucket but in transcripts directory
      await s3Client.putObject({
        Bucket: bucket, // Use the same bucket
        Key: transcriptKey, // Store under the /transcripts directory
        Body: transcriptJsonStr,
        ContentType: "application/json",
      });

      logger.info({
        message: "Transcript uploaded to transcript bucket successfully.",
        key: transcriptKey,
      });

      // Uncomment the following line to delete transcript data from AssemblyAI after saving to S3
      // https://www.assemblyai.com/docs/api-reference/transcripts/delete
      // await deleteTranscriptFromAssemblyAI(transcriptData.id, apiKey);
    }

    return {
      statusCode: 200,
      body: JSON.stringify({
        message: "Audio file(s) processed successfully",
        detail:
          "Transcripts have been stored in the AssemblyAITranscripts directory",
      }),
    };
  } catch (error) {
    console.error(`Error: ${error.message}`);
    return {
      statusCode: 500,
      body: JSON.stringify({
        message: "Error processing audio file(s)",
        error: error.message,
      }),
    };
  }
};
