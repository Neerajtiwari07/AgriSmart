from services.agent.router import route_question

while True:
    question = input("Question: ")

    if question.lower() == "exit":
        break

    tool = route_question(question)

    print("Selected Tool:", tool)