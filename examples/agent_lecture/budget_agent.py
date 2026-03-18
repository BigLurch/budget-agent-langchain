from langchain.agents import create_agent
from util.models import get_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .budget_agent_prompt import BUDGET_AGENT_SYSTEM_PROMPT

def get_float_input(question):
    while True:
        user_input = input(question).strip().replace(",", ".")
        try:
            return float(user_input)
        except ValueError:
            print("Ogiltig inmatning. Skriv ett nummer, till exempel 8500 eller 8500,50.")


def collect_user_data():
    print("\nJag kommer ställa några frågor för att hjälpa dig göra en enkel budget.\n")

    income = get_float_input("Vad är din månadsinkomst efter skatt? ")
    rent = get_float_input("Hur mycket betalar du i hyra per månad? ")
    subscriptions = get_float_input("Hur mycket betalar du för abonnemang per månad? ")
    transport = get_float_input("Hur mycket spenderar du på transport per månad? ")
    food = get_float_input("Hur mycket spenderar du på mat per månad? ")
    fun = get_float_input("Hur mycket spenderar du på nöjen per månad? ")
    other = get_float_input("Hur mycket spenderar du på övrigt per månad? ")
    savings_goal = get_float_input("Hur mycket vill du spara per månad? ")

    return {
        "income": income,
        "rent": rent,
        "subscriptions": subscriptions,
        "transport": transport,
        "food": food,
        "fun": fun,
        "other": other,
        "savings_goal": savings_goal,
    }


def calculate_budget(data):
    fixed_costs = data["rent"] + data["subscriptions"]
    variable_costs = data["transport"] + data["food"] + data["fun"] + data["other"]
    total_expenses = fixed_costs + variable_costs
    remaining = data["income"] - total_expenses
    remaining_after_savings = remaining - data["savings_goal"]

    return {
        "fixed_costs": fixed_costs,
        "variable_costs": variable_costs,
        "total_expenses": total_expenses,
        "remaining": remaining,
        "remaining_after_savings": remaining_after_savings,
    }


def build_budget_summary(data, result):
    return f"""
Användarens ekonomi:

Månadsinkomst efter skatt: {data["income"]} kr
Hyra: {data["rent"]} kr
Abonnemang: {data["subscriptions"]} kr
Transport: {data["transport"]} kr
Mat: {data["food"]} kr
Nöjen: {data["fun"]} kr
Övrigt: {data["other"]} kr
Sparmål: {data["savings_goal"]} kr

Beräknad budget:
Fasta kostnader: {result["fixed_costs"]} kr
Rörliga kostnader: {result["variable_costs"]} kr
Totala utgifter: {result["total_expenses"]} kr
Kvar efter utgifter: {result["remaining"]} kr
Kvar efter sparmål: {result["remaining_after_savings"]} kr

Ge en pedagogisk analys av budgeten.
Förklara enkelt hur situationen ser ut.
Ge konkreta förbättringsförslag.
Bedöm om sparmålet verkar realistiskt.
Var stöttande och tydlig.
"""

def chat_loop(model, messages):
    print("\nDu kan nu ställa följdfrågor om din budget.")
    print("Skriv 'avsluta' om du vill avsluta.\n")

    while True:
        user_input = input("Du: ").strip()

        if user_input.lower() in ["avsluta", "exit", "quit", "q"]:
            print("\nTack för att du använde Budget-Agenten. Lycka till med din budget!")
            break

        messages.append(HumanMessage(content=user_input))
        response = model.invoke(messages)

        print("\nBudget-Agenten:\n")
        print(response.content)
        print()

        messages.append(AIMessage(content=response.content))

def main():
    model = get_model()

    print("Välkommen till Budget-Agenten!")
    print("Jag hjälper dig att planera din budget steg för steg.\n")

    user_data = collect_user_data()
    budget_result = calculate_budget(user_data)
    budget_summary = build_budget_summary(user_data, budget_result)

    messages = [
        SystemMessage(content=BUDGET_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=budget_summary)
    ]

    response = model.invoke(messages)

    print("\n" + "=" * 40)
    print("📊 DIN PERSONLIGA BUDGET")
    print("=" * 40)
    print(f"Inkomst: {user_data['income']} kr")
    print(f"Fasta kostnader: {budget_result['fixed_costs']} kr")
    print(f"Rörliga kostnader: {budget_result['variable_costs']} kr")
    print(f"Totala utgifter: {budget_result['total_expenses']} kr")
    print(f"Kvar efter utgifter: {budget_result['remaining']} kr")
    print(f"Kvar efter sparmål: {budget_result['remaining_after_savings']} kr")

    print("\nBudget-Agentens analys:\n")
    print(response.content)

    chat_loop(model, messages)

if __name__ == "__main__":
    main()