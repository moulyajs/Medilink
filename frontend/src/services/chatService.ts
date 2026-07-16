export async function sendMessage(message: string) {
  await new Promise((resolve) =>
    setTimeout(resolve, 1000)
  );

  return {
    response:
      "This is a dummy response from Medilink AI. Later this will come from your FastAPI backend.",
  };
}