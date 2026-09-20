import pandas as pd
from datetime import datetime
from finance import FinancialState, Event
from exchange_rates import ExchangeRateManager
from data_processor import DataProcessor
from llm_client import LLMClient
from evaluator import Evaluator

data_dir = '../dataset'
events_df = pd.read_csv(data_dir + '/financial_events.csv')
messages_df = pd.read_csv(data_dir + '/messages.csv')
profiles_df = pd.read_csv(data_dir + '/financial_profiles.csv')
sample = pd.read_csv(data_dir + '/sample_requests.csv')
exchange_rates_df = pd.read_csv(data_dir + '/exchange_rates.csv')
exchange_mgr = ExchangeRateManager(exchange_rates_df)
llm = LLMClient()
processor = DataProcessor(llm, data_dir)

req_row = sample[sample['request_id'] == 'request_05'].iloc[0]
user_id = req_row['user_id']
prof_row = profiles_df[profiles_df['user_id'] == user_id].iloc[0]

user_events = events_df[events_df['user_id'] == user_id]
events = [Event(row, exchange_mgr, prof_row['home_currency']) for _, row in user_events.iterrows()]

messages = []
req_date = datetime.strptime(req_row['request_date'], '%Y-%m-%d').date()
state = FinancialState(user_id, prof_row, events, messages, exchange_mgr)
tl, rules = state.build_forecast_with_rules(req_date, days=90)
print('Net 90d sum:', sum(t['net'] for t in tl))

for r in rules:
    print(r['type'], r['amount'], r['direction'], r['category'])

