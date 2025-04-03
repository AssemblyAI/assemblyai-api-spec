if (
  window.location.pathname === "/docs/speech-to-text/pre-recorded-audio" &&
  window.location.hash
) {
  const hash = window.location.hash.substring(1); // Remove the # symbol
  const skipRedirects = ["example-output", "api-reference", "quickstart"];
  if (!skipRedirects.includes(hash)) {
    window.location.href = `/docs/speech-to-text/pre-recorded-audio/${hash}`;
  }
}
