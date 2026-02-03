---
title: Overview
---

This page describes how to perform common operations with the REST API. Each endpoint is documented individually and grouped by the resource it interacts with.

The AssemblyAI API uses [REST](https://en.wikipedia.org/wiki/REST) with [JSON-encoded](https://www.json.org/json-en.html) request bodies and responses, and is available at the following URL:

```plain title="Base URL"
https://api.assemblyai.com
```

<Note>
  To use our EU servers for **Async STT**, replace `api.assemblyai.com` with
  `api.eu.assemblyai.com`. The EU endpoint for **Streaming STT** is
  `streaming.eu.assemblyai.com`. LLM Gateway is not currently supported in the
  EU.
</Note>

<Info title="Streaming Speech-to-Text">
  This page explains the AssemblyAI REST API. If you want to use Streaming
  Speech-to-Text, see [Streaming API
  reference](/docs/api-reference/streaming-api/streaming-api).
</Info>

## Client SDKs

AssemblyAI provides official SDKs for popular programming languages, that make it simpler to interact with the API.

To get started using the SDKs, see the following resources:

- [Transcribe an audio file](https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file)

## Authorization

To make authorized calls the REST API, your app must provide an authorization header with an API key. You can find your API key in the [AssemblyAI dashboard](https://www.assemblyai.com/app/api-keys).

```bash title="Authenticated request"
curl https://api.assemblyai.com/v2/transcript \
  --header 'Authorization: <YOUR_API_KEY>'
```

<Info title="Your API key">
The examples here contain a placeholder, `<YOUR_API_KEY>`, that you need to replace with your actual API key.
</Info>

## Errors

The AssemblyAI API uses HTTP response codes to indicate whether a request was successful.

The response codes generally fall into the following ranges:

- `2xx` indicates the request was successful.
- `4xx` indicates the request may have omitted a required parameter, or have invalid information.
- `5xx` indicates an error on AssemblyAI's end.

Below is a summary of the HTTP response codes you may encounter:

| Code          | Status            | Description                                                                                  |
| ------------- | ----------------- | -------------------------------------------------------------------------------------------- |
| 200           | OK                | Request was successful.                                                                      |
| 400           | Bad request       | The request failed due to an invalid request.                                                |
| 401           | Unauthorized      | Missing or invalid API key.                                                                  |
| 404           | Not found         | The requested resource doesn't exist.                                                        |
| 429           | Too many requests | Too many request were sent to the API. See [Rate limits](#rate-limits) for more information. |
| 500, 503, 504 | Server error      | Something went wrong on AssemblyAI's end.                                                    |

```json title="Response with error"
{
  "error": "Authentication error, API token missing/invalid"
}
```

<Tip title="API status">
  To stay up-to-date with any known service disruptions, subscribe to updates on
  the [Status](https://status.assemblyai.com) page.
</Tip>

### Failed transcriptions

Transcriptions may fail due to errors while processing the audio data.

When you query a transcription that has failed, the response will have a `200` code, along with `status` set to `error` and an `error` property with more details.

```json title="Failed transcription"
{
    "status": "error",
    "error": "Download error to https://foo.bar, 403 Client Error: Forbidden for url: https://foo.bar",
    ...
}
```

Common reasons why a transcription may fail include:

- Audio data is corrupted or in an unsupported format. See [FAQ](https://www.assemblyai.com/docs/concepts/faq) for supported formats.
- Audio URL is a webpage rather than a file.
- Audio URL isn't accessible from AssemblyAI's servers.
- Audio duration is too short (less than 160ms).

In the rare event of a transcription failure due to a server error, you may resubmit the file for transcription. If the problems persist after resubmitting, [let us know](mailto:support@assemblyai.com).

## Rate limits

To ensure the LLM Gateway API remains available for all users, you can only make a limited number of requests within a 60-second time window. These rate limits are specific to each LLM Gateway model.

If you exceed the limit, the API will respond with a `429` status code.

To see your remaining quota, check the following response headers:

| Header                  | Description                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| `X-RateLimit-Limit`     | Maximum number of allowed requests in a 60 second window.                                  |
| `X-RateLimit-Remaining` | Number of remaining requests in the current time window.                                   |
| `X-RateLimit-Reset`     | Number of seconds until the remaining requests resets to the value of `X-RateLimit-Limit`. |
| `X-RateLimit-Model`     | The model the rate limit applies to. Same as "model" param in the request.                 |
| `X-RateLimit-Service`   | Denotes the service used, LLM Gateway or Speech Understanding                              |

If the response doesn't include `X-RateLimit` headers, the endpoint doesn't have rate limits.

<Info title="Increasing rate limits">
  If you want to increase the rate limit for your account, [contact
  us](mailto:support@assemblyai.com).
</Info>

## Pagination

Endpoints that support listing multiple resources use pagination to limit the number of results returned in a single response.

Paginated responses include a `page_details` JSON object with information about the results and links to navigate between pages.

| Property                       | Description                            |
| ------------------------------ | -------------------------------------- |
| `page_details[i].limit`        | Maximum number of resources in a page. |
| `page_details[i].result_count` | Total number of available resources.   |
| `page_details[i].current_url`  | URL to the current page.               |
| `page_details[i].prev_url`     | URL to the previous page.              |
| `page_details[i].next_url`     | URL to the next page.                  |

```json title="Paginated response"
{
  "page_details": {
    "limit": 1,
    "result_count": 1,
    "current_url": "https://api.assemblyai.com/v2/transcript?limit=1",
    "prev_url": "https://api.assemblyai.com/v2/transcript?limit=1&before_id=bfc3622e-8c69-4497-9a84-fb65b30dcb07",
    "next_url": "https://api.assemblyai.com/v2/transcript?limit=1&after_id=bfc3622e-8c69-4497-9a84-fb65b30dcb07"
  },
  "transcripts": [
    {
      // ...
    }
  ]
}
```

## Versioning

When AssemblyAI makes backwards-incompatible changes to the API, we release a new version. For information on API updates, see [Changelog](https://www.assemblyai.com/changelog).

Endpoints are versioned using a path prefix, such as `/v2`.
