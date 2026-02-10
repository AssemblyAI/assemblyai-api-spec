print("Waiting for operation to complete...")
response = operation.result(timeout=90)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print("-" * 20)
    print(f"First alternative of result {i}")
    print(f"Transcript: {alternative.transcript}")
