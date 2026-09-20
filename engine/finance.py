import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from collections import defaultdict

class Event:
    def __init__(self, row, exchange_mgr, home_currency):
        self.id = row.get('event_id')
        self.type = row.get('event_type')
        self.description = row.get('description', '')
        self.category = row.get('category', '')
        self.direction = row.get('direction')
        
        amt = row.get('amount')
        self.amount = float(amt) if pd.notnull(amt) and amt != '' else None
        
        self.currency = row.get('currency')
        
        e_date = row.get('event_date')
        self.event_date = datetime.strptime(e_date, "%Y-%m-%d").date() if isinstance(e_date, str) else e_date
        
        s_date = row.get('settlement_date')
        if isinstance(s_date, str) and pd.notnull(s_date) and s_date != '':
            self.settlement_date = datetime.strptime(s_date, "%Y-%m-%d").date()
        else:
            self.settlement_date = self.event_date
            
        self.status = row.get('status', 'settled')
        self.linked_id = row.get('linked_event_id')
        self.flexibility = row.get('flexibility', 'fixed')
        
        min_amt = row.get('minimum_allowed_amount')
        self.minimum_allowed_amount = float(min_amt) if pd.notnull(min_amt) and min_amt != '' else None
        
        self.exchange_mgr = exchange_mgr
        self.home_currency = home_currency

    def get_home_amount(self) -> float:
        if self.amount is None:
            return 0.0
        if self.currency == self.home_currency:
            return self.amount
        date_str = self.settlement_date.strftime("%Y-%m-%d") if self.settlement_date else "2024-01-01"
        return self.exchange_mgr.convert(self.amount, date_str, self.currency, self.home_currency)

class FinancialState:
    def __init__(self, user_id, profile_row, events: List[Event], messages: List[Dict], exchange_mgr):
        self.user_id = user_id
        self.profile = profile_row
        self.home_currency = profile_row['home_currency']
        self.current_balance = float(profile_row['current_available_balance'])
        self.events = events
        self.messages = messages
        self.exchange_mgr = exchange_mgr

    def build_forecast_with_rules(self, req_date, days=90):
        timeline = []
        rules = []
        
        for i in range(days + 1):
            timeline.append({
                'date': req_date + timedelta(days=i),
                'net': 0.0,
                'events': []
            })
            
        explicit_amounts = {}
        for ev in self.events:
            if ev.status in ['pending', 'scheduled'] and ev.settlement_date and ev.settlement_date >= req_date:
                amt = ev.get_home_amount()
                if ev.direction == 'debit':
                    amt = -amt
                idx = (ev.settlement_date - req_date).days
                if 0 <= idx <= days:
                    timeline[idx]['net'] += amt
                    timeline[idx]['events'].append(ev)
                if ev.category:
                    explicit_amounts[ev.category] = amt
                    
        cat_evs = defaultdict(list)
        for ev in self.events:
            if ev.status == 'settled' and ev.settlement_date and ev.settlement_date <= req_date:
                cat_evs[ev.category].append(ev)
                
        for cat, evs in cat_evs.items():
            if len(evs) >= 2:
                evs.sort(key=lambda x: x.settlement_date)
                d1 = (evs[-1].settlement_date - evs[-2].settlement_date).days
                if len(evs) >= 3:
                    d2 = (evs[-2].settlement_date - evs[-3].settlement_date).days
                else:
                    d2 = d1
                amt = evs[-1].get_home_amount()
                if evs[-1].direction == 'debit': amt = -amt
                
                rule_type = None
                interval = 0
                if 6 <= d1 <= 8 and 6 <= d2 <= 8:
                    rule_type = 'weekly'
                    interval = 7
                elif 28 <= d1 <= 31 and 28 <= d2 <= 31:
                    rule_type = 'monthly'
                    interval = 30
                    
                if rule_type:
                    rules.append({
                        'type': rule_type,
                        'category': cat,
                        'amount': amt,
                        'last_date': evs[-1].settlement_date
                    })
                    
        for rule in rules:
            next_date = rule['last_date']
            interval = 7 if rule['type'] == 'weekly' else 30
            while next_date <= req_date + timedelta(days=days):
                next_date += timedelta(days=interval)
                if next_date >= req_date:
                    idx = (next_date - req_date).days
                    if 0 <= idx <= days:
                        if not any(e.category == rule['category'] for e in timeline[idx]['events']):
                            amt = explicit_amounts.get(rule['category'], rule['amount'])
                            timeline[idx]['net'] += amt
                            
        return timeline, rules