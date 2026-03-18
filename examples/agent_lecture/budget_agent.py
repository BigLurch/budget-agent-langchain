from langchain.agents import create_agent
from util.models import get_model
from langchain_core.messages import SystemMessage, HumanMessage
from .budget_agent_prompt import BUDGET_AGENT_SYSTEM_PROMPT

def collect_user_data():
    print("\nJag kommer ställa några frågor för att hjälpa dig.\n")

    income = input("Vad är din månadsinkomst efter skatt? ")
    fixed_costs = input("Vad har du för fasta kostnader (hyra, abonnemang etc)? ")
    variable_costs = input("Ungefär hur mycket spenderar du på mat och nöjen? ")
    savings_goal = input("Har du något sparmål? ")

    return f"""
    Inkomst: {income}
    Fasta kostnader: {fixed_costs}
    Rörliga kostnader: {variable_costs}
    Sparmål: {savings_goal}
    """

def main():
    model = get_model()

    print("Välkommen till Budget-Agenten!")
    print("Jag hjälper dig att planera din budget steg för steg.\n")

    user_data = collect_user_data()

    messages = [
        SystemMessage(content=BUDGET_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=user_data)
    ]

    response = model.invoke(messages)

    print("\n" + "="*40)
    print("📊 DIN PERSONLIGA BUDGET")
    print("="*40 + "\n")
    print(response.content)

if __name__ == "__main__":
    main()