import 'dotenv/config';
import { AssemblyAIClient, AssemblyAI } from "@assemblyai-fern/api";
import { CreateTranscriptParameters } from "@assemblyai-fern/api/api";

const aai = new AssemblyAIClient({
  apiKey: process.env.ASSEMBLYAI_API_KEY || '',
});

const audioUrl = 'https://storage.googleapis.com/aai-docs-samples/espn.m4a';
const createTranscriptParams: CreateTranscriptParameters = {
  audioUrl,
  boostParam: AssemblyAI.TranscriptBoostParam.High,
  wordBoost: ['Chicago', 'draft'],
  disfluencies: true,
  dualChannel: true,
  formatText: false,
  languageCode: AssemblyAI.TranscriptLanguageCode.En,
  punctuate: false,
  speechThreshold: 0.5,
};

async function waitForTranscriptToComplete(transcript: AssemblyAI.Transcript) {
  while (true) {
    transcript = await aai.transcript.get(transcript.id);
    if (transcript.status === AssemblyAI.TranscriptStatus.Completed ||
      transcript.status === AssemblyAI.TranscriptStatus.Error) {
      return transcript;
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
}

(async function createStandardTranscript() {
  let transcript = await aai.transcript.create(createTranscriptParams);
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})()
  .then(async (transcript) => {
    // TODO(fern): Support plain text
    //await exportAsSubtitles(transcript);
    await getParagraphs(transcript);
    await getSentences(transcript);
    //await searchTranscript(transcript);
    //await deleteTranscript(transcript);
  });

(async function runLemurModels() {
  let transcript = await aai.transcript.create(createTranscriptParams);
  transcript = await waitForTranscriptToComplete(transcript);
  await lemurSummary(transcript);
  await lemurQuestionAnswer(transcript);
  await lemurActionPoints(transcript);
  await lemurCustomTask(transcript);
  await deleteTranscript(transcript);
})();

(async function createTranscriptWithBadUrl() {
  let transcript = await aai.transcript.create({
    audioUrl: 'https://storage.googleapis.com/aai-docs-samples/oops.m4a'
  });
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(async (transcript) => {
  try {
    await getParagraphs(transcript);
  } catch (error) {
    console.log("Error expected:", error);
    await deleteTranscript(transcript);
  }
});

(async function createTranscriptWithNullUrl() {
  try {
    await aai.transcript.create({
      audioUrl: null as unknown as string
    });
  } catch (error) {
    console.log("Error expected:", error);
  }
})();

(async function createTranscriptWithWordBoost() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    boostParam: AssemblyAI.TranscriptBoostParam.High,
    wordBoost: ['knee', 'hip'],
  });
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithSummarization() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    summarization: true,
    summaryModel: AssemblyAI.SummaryModel.Conversational,
    summaryType: AssemblyAI.SummaryType.BulletsVerbose,
    punctuate: true,
    formatText: true
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithContentSafety() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    contentSafety: true,
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithCustomSpelling() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    customSpelling: [
      { from: ['quarterback', 'QB'], to: 'nickelback' },
      { from: ['bear'], to: 'cub' },
    ]
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithEntityDetection() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    entityDetection: true,
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithFilterProfanity() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    filterProfanity: true,
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithTopicDetection() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    iabCategories: true
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithLanguageDetection() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    languageCode: undefined,
    languageDetection: true
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithPiiRedaction() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    formatText: true,
    redactPii: true,
    redactPiiAudio: true,
    redactPiiAudioQuality: 'wav',
    redactPiiPolicies: [
      AssemblyAI.PiiPolicies.Injury,
      AssemblyAI.PiiPolicies.MedicalCondition,
      AssemblyAI.PiiPolicies.MedicalProcess
    ],
    redactPiiSub: AssemblyAI.SubstitutionPolicy.Hash,
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);

  const redactedAudio = await aai.transcript.getRedactedAudio(transcript.id);
  console.log(redactedAudio);

  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithSentimentAnalysis() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    punctuate: true,
    sentimentAnalysis: true,
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithSpeakerLabels() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    dualChannel: false,
    punctuate: true,
    speakerLabels: true,
    speakersExpected: 2,
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function createTranscriptWithWebhook() {
  let transcript = await aai.transcript.create({
    ...createTranscriptParams,
    webhookAuthHeaderName: 'x-foo',
    webhookAuthHeaderValue: 'bar',
    webhookUrl: 'https://www.assemblyai.com/404'
  })
  transcript = await waitForTranscriptToComplete(transcript);
  console.log(transcript);
  return transcript;
})().then(deleteTranscript);

(async function listTranscripts() {
  let list = await aai.transcript.list();
  console.log(list);
  while (!!list.pageDetails?.nextUrl) {
    const params = new URL(list.pageDetails.nextUrl).searchParams
    list = await aai.transcript.list({
      afterId: params.get('after_id') || undefined,
      limit: parseInt(params.get('limit') || 'NaN') || undefined,
    });
    console.log(list);
  }
})();

async function searchTranscript(transcript: AssemblyAI.Transcript) {
  const result = await aai.transcript.search(transcript.id, {
    words: ['draft', 'football']
  });
  console.log(result);
}

async function exportAsSubtitles(transcript: AssemblyAI.Transcript) {
  const srt = await aai.transcript.exportAsSrt(transcript.id)
  const vtt = await aai.transcript.exportAsVtt(transcript.id)
  console.log('SRT subtitles', srt);
  console.log('VTT subtitles', vtt);
}

async function getParagraphs(transcript: AssemblyAI.Transcript) {
  const paragraphs = await aai.transcript.getParagraphs(transcript.id)
  console.dir(paragraphs, { depth: null });
}

async function getSentences(transcript: AssemblyAI.Transcript) {
  const sentences = await aai.transcript.getSentences(transcript.id)
  console.dir(sentences, { depth: null });
}

async function deleteTranscript(transcript: AssemblyAI.Transcript) {
  await aai.transcript.delete(transcript.id);
};

const lemurContext = 'This is a podcast on the ESPN channel talking about NFL draft picks.';

async function lemurSummary(transcript: AssemblyAI.Transcript) {
  const response = await aai.lemur.summary({
    transcriptIds: [transcript.id],
    context: lemurContext,
    finalModel: AssemblyAI.LemurModels.Basic,
    maxOutputSize: 3000,
    answerFormat: 'bullet points'
  })
  console.log(response.response);
};

async function lemurQuestionAnswer(transcript: AssemblyAI.Transcript) {
  const response = await aai.lemur.questionAnswer({
    transcriptIds: [transcript.id],
    questions: [
      {
        question: 'Which players were mentioned?',
        context: lemurContext,
        answerFormat: '<name> <jersey_number>',
      },
      {
        question: 'Were they excited',
        context: lemurContext,
        answerOptions: ['yes', 'no']
      }
    ],
    context: lemurContext,
    finalModel: AssemblyAI.LemurModels.Basic,
    maxOutputSize: 3000
  })
  console.log(response.response);
};

async function lemurActionPoints(transcript: AssemblyAI.Transcript) {
  const response = await aai.lemur.actionItems({
    transcriptIds: [transcript.id],
    context: lemurContext,
    finalModel: AssemblyAI.LemurModels.Basic,
    maxOutputSize: 3000
  })
  console.log(response.response);
};

async function lemurCustomTask(transcript: AssemblyAI.Transcript) {
  const response = await aai.lemur.task({
    transcriptIds: [transcript.id],
    prompt: 'List all the teams and their players that are mentioned.',
    context: lemurContext,
    finalModel: AssemblyAI.LemurModels.Basic,
    maxOutputSize: 3000
  })
  console.log(response.response);
};