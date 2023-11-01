# AssemblyAI API

Tagging a release on this repository will update the:
  - [Java SDK](https://github.com/AssemblyAI/assemblyai-java-sdk)

## What is in this repository?

This repository contains

- AssemblyAI's [OpenAPI spec](./openapi.yml)
- AssemblyAI's [AsyncAPI spec](./asyncapi.yml) folder
- Generators (see [generators.yml](./fern/generators.yml))

To make sure that the specs are valid, you can use the `lint` script.

```bash
npm run-script lint
```

## What are generators?

Generators read in your API Definition and 
output artifacts (e.g. Java SDK) and are tracked in [generators.yml](./fern/generators.yml).

To trigger the generators run, tag a Github release on this repository.