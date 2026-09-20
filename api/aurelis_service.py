import pandas as pd
from datetime import datetime
import os
import json

# These are imported from the parent directory's 'engine/' package safely via sys.path
from finance import Event, FinancialState
from exchange_rates import ExchangeRateManager
from evaluator import Evaluator
from data_processor import DataProcessor
from llm_client import LLMClient

class AurelisService:
    """Core service orchestrating data retrieval and engine evaluation."""
    def __init__(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
        self.events_df = pd.read_csv(f'{self.data_dir}/financial_events.csv')
        self.profiles_df = pd.read_csv(f'{self.data_dir}/financial_profiles.csv')
        self.requests_df = pd.read_csv(f'{self.data_dir}/requests.csv')
        self.messages_df = pd.read_csv(f'{self.data_dir}/messages.csv')
        self.options_df = pd.read_csv(f'{self.data_dir}/request_payment_options.csv')
        self.rates_df = pd.read_csv(f'{self.data_dir}/exchange_rates.csv')
        self.images_df = pd.read_csv(f'{self.data_dir}/images.csv')
        
        self.exchange_mgr = ExchangeRateManager(self.rates_df)
        self.llm = LLMClient()
        self.processor = DataProcessor(self.llm, self.data_dir)

    def get_all_requests(self):
        """Fetch all requests available in the dataset."""
        # Return a list of basic info for the sidebar
        res = []
        for _, row in self.requests_df.iterrows():
            res.append({
                "request_id": row["request_id"],
                "user_id": row["user_id"],
                "amount": float(row["requested_amount"])
            })
        return res

    def analyze(self, req_id: str):
        req_rows = self.requests_df[self.requests_df['request_id'] == req_id]
        if req_rows.empty:
            raise ValueError(f"Request {req_id} not found.")
            
        req_row = req_rows.iloc[0]
        user_id = req_row['user_id']
        req_date = datetime.strptime(req_row['request_date'], '%Y-%m-%d').date()
        
        prof_row = self.profiles_df[self.profiles_df['user_id'] == user_id].iloc[0]
        user_events = self.events_df[self.events_df['user_id'] == user_id]
        
        evidence_log = []
        events = []
        
        for _, r in user_events.iterrows():
            ev = Event(r, self.exchange_mgr, prof_row['home_currency'])
            if ev.amount is None:
                img_row = self.images_df[self.images_df['related_event_id'] == ev.id]
                if not img_row.empty:
                    img_id = img_row.iloc[0]['image_id']
                    try:
                        amt = self.processor.extract_image_amount(img_id, diagnostic_mode=False)
                        if amt is not None:
                            ev.amount = amt
                            evidence_log.append({"class": "image", "id": img_id, "result": amt, "status": "verified"})
                        else:
                            evidence_log.append({"class": "image", "id": img_id, "result": "API Limited/Failed", "status": "unresolved"})
                    except Exception as e:
                        evidence_log.append({"class": "image", "id": img_id, "result": str(e), "status": "unresolved"})
            events.append(ev)
            
        user_msgs = self.messages_df[self.messages_df['user_id'] == user_id]
        messages = []
        for _, msg_row in user_msgs.iterrows():
            if self.processor.is_message_potentially_relevant(msg_row['message_text'], req_date, msg_row['sent_at']):
                try:
                    parsed = self.processor.parse_message(msg_row['message_text'], req_date, msg_row['sent_at'], diagnostic_mode=False, msg_id=msg_row['message_id'])
                    if parsed and parsed.get('is_relevant'):
                        parsed['event_id'] = msg_row['related_event_id'] if pd.notnull(msg_row['related_event_id']) else parsed.get('event_id')
                        messages.append(parsed)
                        evidence_log.append({"class": "message", "id": msg_row['message_id'], "result": parsed, "status": "verified", "raw": msg_row['message_text']})
                    else:
                        if parsed is None:
                            evidence_log.append({"class": "message", "id": msg_row['message_id'], "result": "API Limited", "status": "unresolved", "raw": msg_row['message_text']})
                except Exception as e:
                    evidence_log.append({"class": "message", "id": msg_row['message_id'], "result": str(e), "status": "unresolved", "raw": msg_row['message_text']})
                    
        state = FinancialState(user_id, prof_row, events, messages, self.exchange_mgr)
        req_opts = self.options_df[self.options_df['request_id'] == req_id]
        opts = [row.to_dict() for _, row in req_opts.iterrows()]
        
        evaluator = Evaluator(req_row, opts, state)
        decision = evaluator.evaluate()
        
        # We also want to map the 90-day forecast to send to the frontend chart
        timeline = state.build_forecast(evaluator.request_date)
        forecast_data = []
        curr_bal = state.current_balance
        proj_low = float('inf')
        dates_list = []
        for day in timeline:
            curr_bal += day['net']
            if curr_bal < proj_low:
                proj_low = curr_bal
            
            dates_list.append(day['date'])
            forecast_data.append({
                "date": day['date'].strftime("%Y-%m-%d"),
                "balance": curr_bal,
                "net": day['net']
            })
            
        # Serialize specific event markers (income/expenses) within timeline
        income_pts = []
        expense_pts = []
        for evt in state.events:
            if evt.settlement_date >= evaluator.request_date and evt.settlement_date <= dates_list[-1]:
                if evt.status != 'cancelled' and evt.amount is not None:
                    amt = evt.get_home_amount()
                    idx = (evt.settlement_date - dates_list[0]).days
                    if 0 <= idx < len(forecast_data):
                        y_val = forecast_data[idx]["balance"]
                        if evt.direction == 'credit':
                            income_pts.append({"x": evt.settlement_date.strftime("%Y-%m-%d"), "y": y_val, "text": f"+{amt:,.0f} ({evt.category})"})
                        else:
                            expense_pts.append({"x": evt.settlement_date.strftime("%Y-%m-%d"), "y": y_val, "text": f"-{amt:,.0f} ({evt.category})"})

        # Format spending changes clearly for the frontend
        spending_changes = []
        sc_raw = decision['spending_changes_needed']
        if sc_raw and sc_raw != 'none':
            for chunk in sc_raw.split('|'):
                parts = chunk.split(':')
                action = parts[0]
                ev = next((e for e in state.events if e.id == parts[1]), None)
                cat = ev.category if ev else "Unknown"
                new_amt = float(parts[2]) if action == 'reduce_to' else 0.0
                curr_amt = float(ev.get_home_amount()) if ev else 0.0
                rel_cash = curr_amt - new_amt
                spending_changes.append({
                    "category": cat,
                    "action": action,
                    "current": curr_amt,
                    "new": new_amt,
                    "released_cash": rel_cash
                })
                
        # Format payment plan for timeline
        plan_timeline = []
        plan_str = decision['payment_plan']
        if plan_str and plan_str != 'none':
            for chunk in plan_str.split('|'):
                d_str, a_str = chunk.split(':')
                plan_timeline.append({
                    "date": d_str,
                    "amount": float(a_str),
                    "status": "Scheduled"
                })

        return {
            "meta": {
                "request_id": req_id,
                "user_id": user_id,
                "currency": prof_row['home_currency'],
                "requested_amount": float(req_row['requested_amount']),
                "current_balance": state.current_balance,
                "minimum_reserve": state.min_balance,
                "projected_low": proj_low,
                "has_unresolved_evidence": any(e['status'] == 'unresolved' for e in evidence_log)
            },
            "decision": {
                "affordability_status": decision['affordability_status'],
                "amount_safe_to_pay": float(decision['amount_safe_to_pay']),
                "recommended_payment_method": decision['recommended_payment_method'],
                "earliest_date_for_full_payment": decision['earliest_date_for_full_payment']
            },
            "forecast": forecast_data,
            "chart_markers": {
                "income": income_pts,
                "expenses": expense_pts
            },
            "spending_changes": spending_changes,
            "payment_timeline": plan_timeline,
            "evidence": evidence_log
        }
