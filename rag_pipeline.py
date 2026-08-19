from retriever import retrieve_documents, close_qdrant
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Load model
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


while True:

    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    try:
        # Retrieve documents
        documents = retrieve_documents(question, k=1)

        # Combine retrieved context
        context = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        print("\nRETRIEVED CONTEXT:")
        print(context)


        # Improved prompt
        prompt = f"""
You are a helpful assistant answering questions from company reports.

Answer the question using ONLY the context provided.

Context:
{context}

Question:
{question}

Instructions:
- Give a direct and clear answer.
- Do not copy the entire context.
- Do not repeat information.
- If multiple initiatives are mentioned, use bullet points.
- Keep important names and numbers.
- Do not add information that is not present in the context.

Answer:
"""


        # Tokenize
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )


        # Generate answer
        outputs = model.generate(
    **inputs,
    max_new_tokens=150,
    num_beams=4,
    do_sample=False,
    repetition_penalty=1.2
)


        # Decode answer
        answer = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )


        print("\nFINAL RAG ANSWER:")
        print(answer)


    except Exception as e:
        print("\nError:", e)


close_qdrant()

print("\nRAG system closed.")