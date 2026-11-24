from fetch_data import get_data
from process_data import process_data
from create_charts import create_steps_chart
from generate_report import generate_report
from pathlib import Path

# Todo
# sätta upp procent, baserat på hur mycket man har nått målen för den aktiviteten
# procent skrivs ner per dag per aktivitet, per månad får vi genom att plussa ihop alla dagar
# poängsystem, bygger på procent, med en total på 10 poäng per aktivitet, 100% betyder 10 och 150% betyder 15 poäng
# vissa aktiviteter kan inte ha mer än 100% och andra kan ha mer
# Visa månadens påäng på och antal procent av uppnådda mål överst på rapporten



class HealthAnalytic():
    def __init__(self):
        print('HealthAnalytic')

        settings = {
            'useMonth': 'latest' # latest or current or name of the month
        }

        raw_data, points_data = get_data()
        clean_data = process_data(raw_data, settings)
        fig = create_steps_chart(clean_data, points_data)
        generate_report(clean_data, points_data)





if __name__ == '__main__':
    HealthAnalytic()
