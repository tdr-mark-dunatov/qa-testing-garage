import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_BASE = '';
const WS_BASE = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}`;

function App() {
  const [pitId, setPitId] = useState('');
  const [pitLaneUrl, setPitLaneUrl] = useState('');
  const [requests, setRequests] = useState([]);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [diagnostics, setDiagnostics] = useState(null);
  const ws = useRef(null);

  const createPitLane = async () => {
    const { data } = await axios.post(`${API_BASE}/api/pit/new`);
    setPitId(data.pit_id);
    setPitLaneUrl(data.pit_lane_url);
    setRequests([]);
    setSelectedRequest(null);
    connectWebSocket(data.pit_id);
  };

  const connectWebSocket = (id) => {
    if (ws.current) ws.current.close();

    ws.current = new WebSocket(`${WS_BASE}/ws/${id}`);

    ws.current.onopen = () => {
      console.log('🏁 Connected to pit lane');
      const pingInterval = setInterval(() => {
        if (ws.current?.readyState === WebSocket.OPEN) {
          ws.current.send('ping');
        }
      }, 30000);
      ws.current.pingInterval = pingInterval;
    };

    ws.current.onmessage = (event) => {
      const newRequest = JSON.parse(event.data);
      setRequests((prev) => [newRequest, ...prev]);
    };

    ws.current.onclose = () => {
      console.log('👋 Disconnected from pit lane');
      if (ws.current?.pingInterval) {
        clearInterval(ws.current.pingInterval);
      }
    };
  };

  useEffect(() => {
    if (!pitId) return;

    axios.get(`${API_BASE}/api/pit/${pitId}/requests`)
      .then(({ data }) => setRequests(data));

    axios.get(`${API_BASE}/api/pit/${pitId}/diagnostics`)
      .then(({ data }) => setDiagnostics(data))
      .catch(() => setDiagnostics(null));
  }, [pitId]);

  const copyUrl = () => {
    navigator.clipboard.writeText(pitLaneUrl);
    alert('🏁 Pit lane URL copied!');
  };

  const clearRequests = async () => {
    if (!confirm('🗑️ Clear all requests from this pit lane?')) return;
    await axios.delete(`${API_BASE}/api/pit/${pitId}/requests`);
    setRequests([]);
    setSelectedRequest(null);
    setDiagnostics(null);
  };

  const getMethodColor = (method) => {
    const colors = {
      'GET': 'text-blue-600 bg-blue-50',
      'POST': 'text-green-600 bg-green-50',
      'PUT': 'text-yellow-600 bg-yellow-50',
      'DELETE': 'text-red-600 bg-red-50',
      'PATCH': 'text-purple-600 bg-purple-50',
    };
    return colors[method] || 'text-gray-600 bg-gray-50';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-racing-black via-gray-900 to-racing-black text-white">
      <div className="max-w-7xl mx-auto p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold mb-2 flex items-center gap-3">
            <span className="text-6xl">🏁</span>
            <span className="bg-gradient-to-r from-racing-red via-pit-orange to-yellow-500 bg-clip-text text-transparent">
              Webhook Pitstop
            </span>
          </h1>
          <p className="text-gray-400 text-lg">Inspect webhooks at race speed</p>
        </div>

        {/* Pit Lane Creation */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-6 mb-8 border border-racing-red">
          {!pitId ? (
            <div className="text-center">
              <button
                onClick={createPitLane}
                className="bg-gradient-to-r from-racing-red to-pit-orange text-white px-8 py-4 rounded-lg text-xl font-bold hover:scale-105 transform transition-all shadow-lg"
              >
                🏁 Open Pit Lane
              </button>
              <p className="text-gray-400 mt-4">Generate a unique webhook URL for testing</p>
            </div>
          ) : (
            <div>
              <div className="flex gap-4 items-center mb-4">
                <input
                  type="text"
                  value={pitLaneUrl}
                  readOnly
                  className="flex-1 p-3 border-2 border-racing-red rounded-lg bg-gray-900 text-white font-mono"
                />
                <button
                  onClick={copyUrl}
                  className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-bold"
                >
                  📋 Copy
                </button>
                <button
                  onClick={clearRequests}
                  className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 font-bold"
                >
                  🗑️ Clear
                </button>
              </div>
              <p className="text-sm text-gray-400">
                ⚡ Pit Lane ID: <code className="text-pit-orange">{pitId.substring(0, 8)}</code>
              </p>

              {/* Diagnostics */}
              {diagnostics && (
                <div className="mt-4 grid grid-cols-4 gap-4 text-center">
                  <div className="bg-gray-900 p-3 rounded">
                    <div className="text-2xl font-bold text-racing-red">{diagnostics.total_requests}</div>
                    <div className="text-xs text-gray-400">Total Laps</div>
                  </div>
                  <div className="bg-gray-900 p-3 rounded">
                    <div className="text-2xl font-bold text-green-500">{diagnostics.fastest_lap_ms || '-'}ms</div>
                    <div className="text-xs text-gray-400">Fastest Lap</div>
                  </div>
                  <div className="bg-gray-900 p-3 rounded">
                    <div className="text-2xl font-bold text-yellow-500">{diagnostics.slowest_lap_ms || '-'}ms</div>
                    <div className="text-xs text-gray-400">Slowest Lap</div>
                  </div>
                  <div className="bg-gray-900 p-3 rounded">
                    <div className="text-2xl font-bold text-blue-500">{diagnostics.average_lap_ms?.toFixed(1) || '-'}ms</div>
                    <div className="text-xs text-gray-400">Avg Lap</div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Requests Grid */}
        {pitId && (
          <div className="grid grid-cols-2 gap-8">
            {/* Request List */}
            <div className="bg-gray-800 rounded-lg shadow-xl p-6 border border-gray-700">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span>📋</span> Pit Lane Activity ({requests.length})
              </h2>
              <div className="space-y-2 max-h-[600px] overflow-y-auto">
                {requests.length === 0 && (
                  <p className="text-gray-500 text-center py-8">⏱️ Waiting for incoming requests...</p>
                )}
                {requests.map((req) => (
                  <div
                    key={req.id}
                    onClick={() => setSelectedRequest(req)}
                    className={`p-4 border rounded-lg cursor-pointer hover:bg-gray-700 transition-all pit-entry ${
                      selectedRequest?.id === req.id ? 'border-racing-red bg-gray-700' : 'border-gray-600'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className={`font-mono font-bold px-2 py-1 rounded ${getMethodColor(req.method)}`}>
                        {req.method}
                      </span>
                      <span className="text-sm text-gray-400">
                        {new Date(req.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="text-sm text-gray-400 mt-2 flex justify-between">
                      <span>⚡ {req.lap_time_ms}ms</span>
                      <span>📍 {req.ip_address}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Request Details */}
            <div className="bg-gray-800 rounded-lg shadow-xl p-6 border border-gray-700">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <span>🔧</span> Diagnostic Report
              </h2>
              {selectedRequest ? (
                <div className="space-y-4">
                  <div className="bg-gray-900 p-4 rounded-lg">
                    <h3 className="font-bold text-racing-red mb-2">Engine Type</h3>
                    <p className={`font-mono text-lg px-3 py-2 rounded inline-block ${getMethodColor(selectedRequest.method)}`}>
                      {selectedRequest.method}
                    </p>
                  </div>

                  <div className="bg-gray-900 p-4 rounded-lg">
                    <h3 className="font-bold text-racing-red mb-2">⚡ Lap Time</h3>
                    <p className="text-2xl font-bold text-green-500">{selectedRequest.lap_time_ms}ms</p>
                  </div>

                  <div className="bg-gray-900 p-4 rounded-lg">
                    <h3 className="font-bold text-racing-red mb-2">📡 Headers</h3>
                    <pre className="bg-black p-3 rounded-lg overflow-x-auto text-xs text-green-400">
                      {JSON.stringify(selectedRequest.headers, null, 2)}
                    </pre>
                  </div>

                  {Object.keys(selectedRequest.query_params).length > 0 && (
                    <div className="bg-gray-900 p-4 rounded-lg">
                      <h3 className="font-bold text-racing-red mb-2">🔍 Query Params</h3>
                      <pre className="bg-black p-3 rounded-lg overflow-x-auto text-xs text-yellow-400">
                        {JSON.stringify(selectedRequest.query_params, null, 2)}
                      </pre>
                    </div>
                  )}

                  {selectedRequest.body && (
                    <div className="bg-gray-900 p-4 rounded-lg">
                      <h3 className="font-bold text-racing-red mb-2">📦 Payload</h3>
                      <pre className="bg-black p-3 rounded-lg overflow-x-auto text-xs text-blue-400 max-h-64">
                        {selectedRequest.body}
                      </pre>
                    </div>
                  )}

                  <div className="bg-gray-900 p-4 rounded-lg">
                    <h3 className="font-bold text-racing-red mb-2">📍 Source</h3>
                    <p className="font-mono text-gray-300">{selectedRequest.ip_address}</p>
                  </div>

                  <div className="bg-gray-900 p-4 rounded-lg">
                    <h3 className="font-bold text-racing-red mb-2">🕐 Timestamp</h3>
                    <p className="text-gray-300">{new Date(selectedRequest.created_at).toLocaleString()}</p>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">👈 Select a request to view diagnostic details</p>
              )}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>🏁 Webhook Pitstop - Built for speed</p>
        </div>
      </div>
    </div>
  );
}

export default App;
