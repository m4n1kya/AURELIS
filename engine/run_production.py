import pandas as pd
from datetime import datetime
import json
import os
import time

from dotenv import load_dotenv
load_dotenv('../.env')

from finance import Event, FinancialState
from exchange_rates import ExchangeRateManager
from evaluator import Evaluator
from data_processor import DataProcessor
from llm_client import LLMClient

def run_full():
    data_dir = '../dataset'
    
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
        req_amt = float(req_row['requested_amount'])
        
        prof_row = profiles_df[profiles_df['user_id'] == user_id].iloc[0]
        user_events = events_df[events_df['user_id'] == user_id]
        
        events = []
        for _, r in user_events.iterrows():
            ev = Event(r, exchange_mgr, prof_row['home_currency'])
            if ev.amount is None:
                # Need OCR
                img_df = pd.read_csv(data_dir + '/images.csv')
                img_row = img_df[img_df['related_event_id'] == ev.id]
                if not img_row.empty:
                    img_id = img_row.iloc[0]['image_id']
                    try:
                        amt = processor.extract_image_amount(img_id, diagnostic_mode=False)
                        if amt is not None:
                     
<truncated 2778 bytes>