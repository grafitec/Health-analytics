from fetch_data import get_data
from process_data import process_data
from create_charts import create_steps_chart
from generate_report import generate_report
from pathlib import Path

class HealthAnalytic():
    def __init__(self):
        print('HealthAnalytic')
        raw_data = get_data()
        clean_data = process_data(raw_data)

        #fig = create_steps_chart(clean_data)
        generate_report(clean_data)





if __name__ == '__main__':
    HealthAnalytic()
