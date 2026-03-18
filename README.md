# Budget Agent (LangChain)

En pedagogisk AI-agent byggd med LangChain som hjälper användare att förstå och planera sin privatekonomi steg för steg.

## Funktionalitet

Budget-agenten guidar användaren genom hela processen:

1. Samlar in ekonomisk information
2. Räknar ut budget med Python-logik
3. Analyserar ekonomin med hjälp av en LLM
4. Ger konkreta och pedagogiska förbättringsförslag
5. Låter användaren fortsätta interagera via en meny

## Målgrupp

Personer som:
- har svårt att planera sin budget
- vill få en tydligare bild av sin ekonomi
- vill ha enkla och konkreta råd

Agenten är designad för att vara:
- pedagogisk
- tydlig
- stöttande (inte dömande)

---

## Teknik

Projektet är byggt med:

- Python
- LangChain
- OpenAI (via projektets modellhantering)
- CLI (terminalbaserad interaktion)

---

## Struktur

Viktiga delar i projektet:

- `budget_agent.py`  
  Innehåller logik för:
  - datainsamling
  - budgetberäkning
  - interaktiv meny
  - LLM-anrop

- `budget_agent_prompt.py`  
  Innehåller agentens systemprompt (beteende, ton, regler)

---

## Hur agenten fungerar

### 1. Datainsamling
Användaren får svara på frågor om:
- inkomst
- hyra
- abonnemang
- transport
- mat
- nöjen
- övrigt
- sparmål

### 2. Budgetberäkning (Python)
Agenten räknar ut:
- fasta kostnader
- rörliga kostnader
- totala utgifter
- kvarvarande pengar
- kvar efter sparmål

### 3. Analys (LLM)
Modellen:
- förklarar ekonomin pedagogiskt
- ger förbättringsförslag
- bedömer sparmålet

### 4. Interaktiv meny
Efter analysen kan användaren:

1. Få tips för att spara mer  
2. Få hjälp att minska kostnader  
3. Göra om budgeten  
4. Ställa egna frågor  
5. Avsluta  

---

## Installation

### 1. Klona repot

```bash
git clone https://github.com/BigLurch/budget-agent-langchain.git
cd budget-agent-langchain
```

### 2. Skapa virtuell miljö

```bash
python -m venv .venv
```

Aktivera:

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

### 3. Installera beroenden

```bash
pip install -r requirements.txt
```

### 4. Sätt API-nyckel

```bash
export OPENAI_API_KEY="din-nyckel"
```

(eller setx på Windows)

## Kör agenten

```bash
python -m examples.agent_lecture.budget_agent
```


## Exempel på användning

Användaren anger t.ex:
- Inkomst: 25000 kr
- Hyra: 8500 kr
- Mat: 3500 kr

Agenten svarar med:
- budgetöversikt
- analys
- förbättringsförslag

Och erbjuder sedan vidare hjälp via meny.

## Projektstruktur
examples/
├── agent_lecture/
|   ├── budget_agent_prompt.py
|   └── budget_agent.py
├── util/
│   ├── embeddings.py
│   ├── models.py
│   ├── streaming_utils.py
│   ├── tools.py
│   └── pretty_print.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── .env

## Syfte med projektet

Detta projekt är en del av en kurs inom AI / MLOps där målet är att:
- bygga praktiska AI-agenter
- använda LangChain
- kombinera programmering och LLM:er
- skapa användarvänliga AI-lösningar

## Författare
Skapad av Jonas Johansson som en del av kursprojekt.