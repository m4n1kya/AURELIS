"use client";

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, CartesianGrid } from 'recharts';
import { ArrowRight, ChevronRight, Activity, Cpu, Search, Calendar, ChevronDown, CheckCircle, AlertCircle, FileText } from 'lucide-react';

const API_BASE = "http://localhost:8000/api";

export default function Dashboard() {
  const [requests, setRequests] = useState<any[]>([]);
  const [selectedReq, setSelectedReq] = useState('request_01');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('events');

  useEffect(() => {
    fetch(`${API_BASE}/requests`)
      .then(r => r.json())
      .then(d => {
        if(d.length > 0) {
          setRequests(d);
          setSelectedReq(d[0].request_id);
        }
      }).catch(console.error);
  }, []);

  useEffect(() => {
    if (!selectedReq) return;
    setLoading(true);
    fetch(`${API_BASE}/analyze/${selectedReq}`)
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, [selectedReq]);

  if (!data && loading) {
    return <div className="h-screen w-full flex items-center justify-center text-[var(--text-muted)] tracking-widest text-xs">INITIALIZING ENGINE...</div>;
  }

  const statusMap: Record<string, string> = {
    'affordable_now': 'var(--status-safe)',
    'affordable_with_plan': 'var(--status-warning)',
    'affordable_later': 'var(--status-warning)',
    'not_affordable': 'var(--status-danger)',
  };

  const statusColor = data ? statusMap[data.decision.affordability_status] || 'var(--status-safe)' : 'var(--status-safe)';
  const formattedStatus = data?.decision.affordability_status.replace(/_/g, ' ').toUpperCase() || '';
  
  return (
    <div className="flex h-screen bg-black text-white font-mono overflow-hidden">
      <div className="w-64 border-r border-gray-800 flex flex-col">
        <div className="p-4 border-b border-gray-800 flex items-center gap-2">
          <Activity size={16} className="text-[var(--accent-primary)]" />
          <span className="font-bold tracking-widest">AURELIS</span>
        </div>
        <div className="p-2 flex-1 overflow-y-auto">
          <div className="text-xs text-gray-500 mb-2 px-2 uppercase">Requests</div>
          {requests.map(r => (
            <div 
              key={r.request_id}
              onClick={() => setSelectedReq(r.request_id)}
              className={`p-2 text-sm cursor-pointer hover:bg-gray-900 rounded flex justify-between items-center ${selectedReq === r.request_id ? 'bg-gray-900 text-[var(--accent-primary)]' : ''}`}
            >
              <span>{r.request_id}</span>
              <ChevronRight size={14} />
            </div>
          ))}
        </div>
      </div>
      
      <div className="flex-1 flex flex-col h-screen overflow-y-auto relative">
        <div className="absolute top-0 left-0 w-full h-1" style={{ backgroundColor: statusColor }} />
        <div className="p-8">
          <h1 className="text-3xl font-bold mb-8">Analysis: {selectedReq}</h1>
          
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="p-4 border border-gray-800 rounded bg-gray-900/50">
              <div className="text-xs text-gray-500 uppercase">Status</div>
              <div className="text-xl font-bold mt-1" style={{ color: statusColor }}>{formattedStatus}</div>
            </div>
            <div className="p-4 border border-gray-800 rounded bg-gray-900/50">
              <div className="text-xs text-gray-500 uppercase">Safe to Pay</div>
              <div className="text-xl font-bold mt-1 text-white">${data?.decision.amount_safe_to_pay}</div>
            </div>
            <div className="p-4 border border-gray-800 rounded bg-gray-900/50">
              <div className="text-xs text-gray-500 uppercase">Recommendation</div>
              <div className="text-xl font-bold mt-1 text-white">{data?.decision.recommended_payment_method.replace(/_/g, ' ').toUpperCase()}</div>
            </div>
          </div>
          
          <div className="mb-8 border border-gray-800 rounded overflow-hidden">
            <div className="bg-gray-900 p-2 flex gap-4 text-sm border-b border-gray-800">
              <button className={`px-4 py-1 rounded ${activeTab === 'events' ? 'bg-gray-800 text-white' : 'text-gray-400'}`} onClick={() => setActiveTab('events')}>Events</button>
              <button className={`px-4 py-1 rounded ${activeTab === 'timeline' ? 'bg-gray-800 text-white' : 'text-gray-400'}`} onClick={() => setActiveTab('timeline')}>Timeline</button>
            </div>
            
            <div className="p-4 h-96">
              {activeTab === 'events' && (
                <div className="overflow-y-auto h-full">
                  <table className="w-full text-sm text-left">
                    <thead className="text-xs text-gray-500 uppercase bg-gray-900/50">
                      <tr>
                        <th className="px-4 py-2">Date</th>
                        <th className="px-4 py-2">Category</th>
                        <th className="px-4 py-2">Description</th>
                        <th className="px-4 py-2 text-right">Amount</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data?.state.events.map((ev: any, i: number) => (
                        <tr key={i} className="border-b border-gray-800">
                          <td className="px-4 py-2 text-gray-400">{ev.event_date}</td>
                          <td className="px-4 py-2">{ev.category}</td>
                          <td className="px-4 py-2">{ev.description}</td>
                          <td className={`px-4 py-2 text-right font-bold ${ev.direction === 'debit' ? 'text-red-400' : 'text-green-400'}`}>
                            {ev.direction === 'debit' ? '-' : '+'}{ev.amount}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
              
              {activeTab === 'timeline' && (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data?.timeline || []} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="date" stroke="#666" tick={{fontSize: 10}} />
                    <YAxis stroke="#666" tick={{fontSize: 10}} />
                    <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
                    <ReferenceLine y={0} stroke="#666" />
                    <Line type="stepAfter" dataKey="net" stroke="var(--accent-primary)" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}