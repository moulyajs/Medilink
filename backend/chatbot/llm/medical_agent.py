from openai import OpenAI

client = OpenAI()


class MedicalAgent:

    def generate(self, query, context):

        prompt = f"""
You are a medical assistant.

Answer ONLY using the patient records below.

If the answer is not present say:
"I cannot find this information in the records."

Records:
{context}

Question:
{query}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content