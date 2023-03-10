from decimal import Decimal
import psycopg2, psycopg2.extras
import json

fetchSize = 2

def Annuity(row):
    print(f"Сумма кредита: {row['summa']} руб.")
    print(f"Ставка: {row['loan_rate']}%")
    print(f"Срок: {row['loan_term']} месяцев")
    print("Месяц | Ежемесячный платеж | Основной долг | Долг по процентам | Остаток основного долга")

    montlyRate = (1 + (row['loan_rate']/100))**(Decimal(1)/Decimal(12)) # перевод из годовой ставки в месячную
    montlyPayment = (row['summa'] * (montlyRate**(row['loan_term'])) 
                        * (montlyRate - 1)) / (montlyRate**(row['loan_term']) - 1) # рассчет ежемесячного платежа

    currentDebt = row['summa']

    for i in range(row['loan_term']):
        percentageDebt = (montlyRate-1) * currentDebt

        currentDebt = currentDebt - montlyPayment + percentageDebt

        principal = montlyPayment - percentageDebt

        print(f"{i+1} | ", end="")
        print(f"{montlyPayment.quantize(Decimal('0.00'))} | ", end="")
        print(f"{principal.quantize(Decimal('0.00'))} | ", end="")
        print(f"{percentageDebt.quantize(Decimal('0.00'))} | ", end="")
        print(f"{currentDebt.quantize(Decimal('0.00'))}")

with open('postgres_data.json', encoding='utf-8') as json_file:
    postgresData = json.load(json_file)

cnx = psycopg2.connect(**postgresData)

cursor = cnx.cursor(cursor_factory = psycopg2.extras.DictCursor)

query = ("SELECT summa, loan_rate, loan_term FROM applications")
cursor.execute(query)

rows = cursor.fetchmany(size = fetchSize)
for row in rows:
    Annuity(row)

cnx.close()