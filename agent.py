from agent_graph import agent_app
from retriever import close_qdrant


# ==========================================
# MAIN AGENT LOOP
# ==========================================

while True:

    question = input(
        "\nAsk a question (or type 'exit'): "
    )

    # Exit
    if question.lower().strip() == "exit":
        break

    try:

        # Run Agent Graph
        result = agent_app.invoke({
            "question": question,
            "action": "",
            "tool_result": "",
            "answer": ""
        })

        # Print final answer
        print("\nFINAL ANSWER:")

        if result.get("answer"):
            print(result["answer"])
        else:
            print(
                "No answer was generated."
            )

    except Exception as e:

        print("\nError:", e)


# ==========================================
# CLOSE QDRANT
# ==========================================

close_qdrant()

print("\nAgent system closed.")