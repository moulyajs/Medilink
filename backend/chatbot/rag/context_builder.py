def build_context(chunks):

    context_parts = []

    for c in chunks:

        context_parts.append(
            f"""
Date: {c.get('report_date')}
Chunk Type: {c.get('chunk_type')}
Report Type: {c.get('report_type')}

{c.get('text')}
""".strip()
        )

    return "\n\n".join(
        context_parts
    )