# AssemblyAI API Spec

## What is in this repository?

This repository contains

- AssemblyAI's [OpenAPI spec](./openapi.yml)
- AssemblyAI's [AsyncAPI spec](./asyncapi.yml)
- Additional files to work with Fern

To make sure that the specs are valid, you can use the `lint` script.

```bash
npm run-script lint
```

## Fern

### SDKs

We use Fern to generate some of the AssemblyAI SDKs.

- [Java SDK](https://github.com/AssemblyAI/assemblyai-java-sdk)
- [Ruby SDK](https://github.com/AssemblyAI/assemblyai-ruby-sdk)
- [C# .NET SDK](https://github.com/AssemblyAI/assemblyai-csharp-sdk)

### Docs

Our documentation is hosted at https://www.assemblyai.com/docs and all of the content lives inside the `fern/` folder.

## Running the docs

The [Fern CLI](https://www.npmjs.com/package/fern-api) is what builds the documentation.

Install Fern

```
npm install -g fern-api
```

Run the following command at the root of the folder to spin up a local dev server

```
fern docs dev
```

