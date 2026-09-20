import pandas as pd
from datetime import datetime
import json
import os
import time

from dotenv import load_dotenv
load_dotenv('../.env')

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))

from finance import Event, FinancialState
from exchange_rates import ExchangeRateManager
from evaluator import Evaluator
from data_processor import DataProcessor
from llm_client import LLMClient

def run_full():
    data_dir = 'dataset'
    
    events_df = pd.read_csv(data_dir + '/financial_events.csv')
    profiles_df = pd.read_csv(data_dir + '/financial_profiles.csv')
    requests_df = pd.read_csv(data_dir + '/requests.csv')
    messages_df = pd.read_csv(data_dir + '/messages.csv')
    payment_options_df = pd.read_csv(data_dir + '/request_payment_options.csv')
    exchange_rates_df = pd.read_csv(data_dir + '/exchange_rates.csv')
    
    exchange_mgr = ExchangeRateManager(exchange_rates_df)
    llm = LLMClient()
    processor = DataProcessor(llm, data_dir)
    
    output_rows = []
    
    start_time = time.time()
    
    for i, req_row in requests_df.iterrows():
        req_id = req_row['request_id']
        user_id = req_row['user_id']
        req_date = datetime.strptime(req_row['request_date'], '%Y-%m-%d').date()
        
        prof_row = profiles_df[profiles_df['user_id'] == user_id].iloc[0]
        user_events = events_df[events_df['user_id'] == user_id]
        
        events = []
        for _, r in user_events.iterrows():
            ev = Event(r, exchange_mgr, prof_row['home_currency'])
            events.append(ev)
            
        state = FinancialState(user_id, prof_row, events, [], exchange_mgr)
        
        evaluator = Evaluator(req_row, [], state)
        res = evaluator.evaluate()
        
        res['request_id'] = req_id
        output_rows.append(res)
        
    out_df = pd.DataFrame(output_rows)
    out_df = out_df[['request_id', 'amount_safe_to_pay', 'affordability_status', 'recommended_payment_method', 'payment_plan', 'earliest_date_for_full_payment', 'spending_changes_needed', 'decision_explanation']]
    out_df.to_csv(data_dir + '/output.csv', index=False)
    
    print(f"Processed {len(requests_df)} requests in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    run_full()