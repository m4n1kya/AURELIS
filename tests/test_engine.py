import unittest
import pandas as pd
from datetime import datetime, timedelta
from finance import Event, FinancialState
from evaluator import Evaluator, Plan
from exchange_rates import ExchangeRateManager
from data_processor import DataProcessor

class DummyExchange:
    def convert(self, amt, date_str, from_cur, to_cur):
        return amt

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.ex = DummyExchange()
        self.profile = {
            'home_currency': 'USD',
            'current_available_balance': 1000.0,
            'minimum_balance_to_keep': 100.0,
            'payment_methods_user_will_consider': 'full_payment|installments|wait|partial_payment',
            'expense_categories_to_protect': 'rent|utilities',
            'expense_categories_user_is_willing_to_reduce': 'dining',
            'expense_categories_user_is_willing_to_stop': 'entertainment'
        }

    def make_event(self, eid, date_str, amount, direction, category, status='settled', desc='test', flex='fixed'):
        return Event({
            'event_id': eid,
            'user_id': 'u1',
            'event_type': 'expense' if direction == 'debit' else 'income',
            'category': category,
            'description': desc,
            'direction': direction,
            'status': status,
            'flexibility': flex,
            'amount': amount,
            'currency': 'USD',
            'event_date': date_str
        }, self.ex, 'USD')

    def test_request_date_events(self):
        # Settled event on request_date should be history (not subtracted again)
        # Pending debit on request_date should be forecasted
        # Scheduled credit on request_date should be forecasted
        ev1 = self.make_event('e1', '2024-01-01', 50, 'debit', 'food', status='settled')
        ev2 = self.make_event('e2', '2024-01-01', 30, 'debit', 'food', status='pending')
        ev3 = self.make_event('e3', '2024-01-01', 100, 'credit', 'salary', status='scheduled')
        
        state = FinancialState('u1', self.profile, [ev1, ev2, ev3], [], self.ex)
        req_date = datetime(2024, 1, 1).date()
        
        timeline, rules = state.build_forecast_with_rules(req_date, days=1)
        # day 1 net should be -30 + 100 = 70. 50 is ignored because it's settled.
        self.assertEqual(timeline[0]['net'], 70.0)

    def test_recurrence_weekly(self):
        # 3 events 7 days apart
        ev1 = self.make_event('e1', '2024-01-01', 50, 'debit', 'groceries')
        ev2 = self.make_event('e2', '2024-01-08', 60, 'debit', 'groceries')
        ev3 = self.make_event('e3', '2024-01-15', 55, 'debit', 'groceries')
        
        state = FinancialState('u1', self.profile, [ev1, ev2, ev3], [], self.ex)
        req_date = datetime(2024, 1, 20).date()
        
        timeline, rules = state.build_forecast_with_rules(req_date, days=10)
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['type'], 'weekly')
        # should project on 2024-01-22 and 2024-01-29
        nets = {t['date'].strftime('%Y-%m-%d'): t['net'] for t in timeline}
        self.assertEqual(nets['2024-01-22'], -55.0) # Uses most recent explicit amount
        self.assertEqual(nets['2024-01-29'], -55.0)

    def test_double_counting(self):
        # Monthly rule with a scheduled event in the future
        ev1 = self.make_event('e1', '2024-01-01', 500, 'credit', 'salary', status='settled')
        ev2 = self.make_event('e2', '2024-02-01', 500, 'credit', 'salary', status='settled')
        ev3 = self.make_event('e3', '2024-03-01', 500, 'credit', 'salary', status='scheduled')
        
        state = FinancialState('u1', self.profile, [ev1, ev2, ev3], [], self.ex)
        req_date = datetime(2024, 2, 15).date()
        timeline, rules = state.build_forecast_with_rules(req_date, days=60)
        
        nets = {t['date'].strftime('%Y-%m-%d'): t['net'] for t in timeline}
        # On 2024-03-01, it should only add 500 once
        self.assertEqual(nets['2024-03-01'], 500.0)
        
    def test_spending_changes_and_evaluator(self):
        ev1 = self.make_event('e1', '2024-01-01', 200, 'debit', 'dining', flex='flexible')
        ev2 = self.make_event('e2', '2024-02-01', 200, 'debit', 'dining', flex='flexible')
        ev2.minimum_allowed_amount = 50.0 # can reduce to 50
        
        ev3 = self.make_event('e3', '2024-01-10', 300, 'debit', 'entertainment', flex='flexible')
        ev4 = self.make_event('e4', '2024-02-10', 300, 'debit', 'entertainment', flex='flexible')
        
        state = FinancialState('u1', self.profile, [ev1, ev2, ev3, ev4], [], self.ex)
        req_date = datetime(2024, 2, 15).date()
        
        req_row = {
            'request_id': 'r1',
            'request_date': '2024-02-15',
            'request_type': 'purchase',
            'requested_amount': 900.0,
            'desired_completion_date': '2024-05-01',
            'allows_partial_payment': 'false'
        }
        
        evaluator = Evaluator(req_row, [], state)
        res = evaluator.evaluate()
        # Initial balance 1000. Min 100. Available 900.
        # But recurring expenses: dining (200), entertainment (300).
        # Without changes: 900 - 500 = 400. Not affordable for 900.
        # With changes: stop entertainment (+300), reduce dining to 50 (+150). Total saved = 450.
        # Available = 400 + 450 = 850. Still not affordable? 
        # Wait, over 90 days, we have 3 months of expenses! 3 * 500 = 1500.
        # Balance goes negative. 
        self.assertEqual(res['affordability_status'], 'not_affordable')

if __name__ == '__main__':
    unittest.main()
