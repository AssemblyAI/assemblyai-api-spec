transcriber.on("open", ({ id }) => {
  console.log(`Session opened with ID: ${id}`);
});

transcriber.on("error", (error) => {
  console.error("Error:", error);
});

transcriber.on("close", (code, reason) =>
  console.log("Session closed:", code, reason)
);

transcriber.on("turn", (turn) => {
  if (!turn.transcript) {
    return;
  }

  console.log("Turn:", turn.transcript);
});
