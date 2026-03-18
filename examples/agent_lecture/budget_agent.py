from util.models import get_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .budget_agent_prompt import BUDGET_AGENT_SYSTEM_PROMPT

def get_float_input(question):
    while True:
        user_input = input(question).strip().replace(",", ".")
        try:
            value = float(user_input)
            if value < 0:
                print("Skriv ett värde som är 0 eller högre.")
                continue
            return value
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

def show_menu():
    print("\nVad vill du göra nu?")
    print("1. Få tips för att spara mer")
    print("2. Få hjälp att minska kostnader")
    print("3. Göra om budgeten med nya siffror")
    print("4. Ställa en egen fråga")
    print("5. Avsluta")


def handle_menu_choice(choice, model, messages):
    if choice == "1":
        user_input = (
            "Ge mig konkreta och pedagogiska tips på hur jag kan spara mer varje månad "
            "utifrån min nuvarande budget."
        )
    elif choice == "2":
        user_input = (
            "Analysera min budget och förklara vilka kostnader jag borde börja minska först. "
            "Ge konkreta förslag."
        )
    elif choice == "3":
        return "restart"
    elif choice == "4":
        user_input = input("Skriv din fråga: ").strip()
    elif choice == "5":
        return "exit"
    else:
        print("Ogiltigt val. Försök igen.")
        return None

    messages.append(HumanMessage(content=user_input))
    response = model.invoke(messages)

    print("\nBudget-Agenten:\n")
    print(response.content)

    messages.append(AIMessage(content=response.content))
    return "continue"

def menu_loop(model, messages):
    while True:
        show_menu()
        choice = input("Välj ett alternativ (1-5): ").strip()

        result = handle_menu_choice(choice, model, messages)

        if result == "exit":
            print("\nTack för att du använde Budget-Agenten. Lycka till med din budget!")
            return "exit"
        elif result == "restart":
            print("\nDå börjar vi om med nya siffror.\n")
            return "restart"

def main():
    model = get_model()

    print("Välkommen till Budget-Agenten!")
    print("Jag hjälper dig att planera din budget steg för steg.\n")

    while True:
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
        print(f"Inkomst: {user_data['income']:.0f} kr")
        print(f"Fasta kostnader: {budget_result['fixed_costs']:.0f} kr")
        print(f"Rörliga kostnader: {budget_result['variable_costs']:.0f} kr")
        print(f"Totala utgifter: {budget_result['total_expenses']:.0f} kr")
        print(f"Kvar efter utgifter: {budget_result['remaining']:.0f} kr")
        print(f"Kvar efter sparmål: {budget_result['remaining_after_savings']:.0f} kr")

        print("\nBudget-Agentens analys:\n")
        print(response.content)

        messages.append(AIMessage(content=response.content))

        result = menu_loop(model, messages)
        if result != "restart":
            break

if __name__ == "__main__":
    main()