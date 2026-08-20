from agent_graph import agent_app
from retriever import close_qdrant


while True:

    question = input(
        "\nAsk a question (or type 'exit'): "
    )

    if question.lower().strip() == "exit":
        break

    try:

        result = agent_app.invoke({
            "question": question,
            "action": "",
            "tool_result": "",
            "answer": ""
        })

        print("\nFINAL ANSWER:")
        print(result["answer"])

    except Exception as e:

        print("\nError:", e)


close_qdrant()

print("\nAgent system closed.")