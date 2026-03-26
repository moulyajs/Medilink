def build_context(chunks):
    context_parts = []

    for c in chunks:
        part = f"""
[Date: {c.get('report_date')} | Doc: {c.get('document_id')}]
{c.get('text')}
"""
        context_parts.append(part.strip())

    return "\n\n".join(context_parts)