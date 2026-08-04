def build_response(responses):

    sections = []
    all_chunks = []

    for response in responses:

        if response.get("content"):
            sections.append(response["content"])

        if response.get("chunks"):
            all_chunks.extend(response["chunks"])

    return {
        "answer": "\n\n".join(sections),
        "chunks": all_chunks
    }