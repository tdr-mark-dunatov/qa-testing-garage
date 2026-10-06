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
    <div className="min-h-screen bg-gradient-to-br from-white via-checkered to-track-gray">
      <div className="max-w-7xl mx-auto p-8">
        {/* Header with Racing Stripe */}
        <div className="mb-8 relative">
          <div className="absolute inset-x-0 top-0 h-2 bg-gradient-to-r from-racing-red via-pit-orange to-racing-red"></div>
          <h1 className="text-5xl font-bold mb-2 flex items-center gap-3 mt-4">
            <span className="text-6xl">🏁</span>
            <span className="bg-gradient-to-r from-racing-red to-racing-red-dark bg-clip-text text-transparent">
              Webhook Pitstop
            </span>
          </h1>
          <p className="text-gray-600 text-lg font-medium">⚡ Inspect webhooks at race speed</p>
        </div>

        {/* Pit Lane Creation */}
        <div className="bg-white rounded-lg shadow-2xl p-6 mb-8 border-4 border-racing-red">
          {!pitId ? (
            <div className="text-center py-8">
              <button
                onClick={createPitLane}
                className="bg-gradient-to-r from-racing-red to-racing-red-dark text-white px-12 py-6 rounded-xl text-2xl font-bold hover:scale-105 transform transition-all shadow-2xl hover:shadow-racing-red/50 border-4 border-racing-red-dark"
              >
                🏁 Open Pit Lane
              </button>
              <p className="text-gray-600 mt-6 text-lg font-medium">Generate a unique webhook URL for testing</p>
            </div>
          ) : (
            <div>
              <div className="flex gap-4 items-center mb-4">
                <input
                  type="text"
                  value={pitLaneUrl}
                  readOnly
                  className="flex-1 p-4 border-3 border-racing-red rounded-lg bg-checkered text-racing-black font-mono text-lg font-bold shadow-inner"
                />
                <button
                  onClick={copyUrl}
                  className="bg-gradient-to-r from-green-600 to-green-700 text-white px-8 py-4 rounded-lg hover:scale-105 font-bold shadow-lg transform transition-all"
                >
                  📋 Copy
                </button>
                <button
                  onClick={clearRequests}
                  className="bg-gradient-to-r from-racing-red to-racing-red-dark text-white px-8 py-4 rounded-lg hover:scale-105 font-bold shadow-lg transform transition-all"
                >
                  🗑️ Clear
                </button>
              </div>
              <p className="text-sm text-gray-700 font-semibold">
                ⚡ Pit Lane ID: <code className="text-racing-red bg-racing-red/10 px-2 py-1 rounded font-mono">{pitId.substring(0, 8)}</code>
              </p>

              {/* Diagnostics - Racing Dashboard */}
              {diagnostics && (
                <div className="mt-6 grid grid-cols-4 gap-4 text-center">
                  <div className="bg-gradient-to-br from-racing-red to-racing-red-dark p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all">
                    <div className="text-3xl font-bold text-white">{diagnostics.total_requests}</div>
                    <div className="text-xs text-white/80 font-semibold mt-1">🏁 Total Laps</div>
                  </div>
                  <div className="bg-gradient-to-br from-green-500 to-green-600 p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all">
                    <div className="text-3xl font-bold text-white">{diagnostics.fastest_lap_ms || '-'}ms</div>
                    <div className="text-xs text-white/80 font-semibold mt-1">⚡ Fastest Lap</div>
                  </div>
                  <div className="bg-gradient-to-br from-pit-orange to-yellow-500 p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all">
                    <div className="text-3xl font-bold text-white">{diagnostics.slowest_lap_ms || '-'}ms</div>
                    <div className="text-xs text-white/80 font-semibold mt-1">🐌 Slowest Lap</div>
                  </div>
                  <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-4 rounded-lg shadow-lg transform hover:scale-105 transition-all">
                    <div className="text-3xl font-bold text-white">{diagnostics.average_lap_ms?.toFixed(1) || '-'}ms</div>
                    <div className="text-xs text-white/80 font-semibold mt-1">📊 Avg Lap</div>
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
            <div className="bg-white rounded-lg shadow-2xl p-6 border-4 border-racing-red">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 text-racing-red">
                <span>📋</span> Pit Lane Activity ({requests.length})
              </h2>
              <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {requests.length === 0 && (
                  <p className="text-gray-500 text-center py-8 font-medium">⏱️ Waiting for incoming requests...</p>
                )}
                {requests.map((req) => (
                  <div
                    key={req.id}
                    onClick={() => setSelectedRequest(req)}
                    className={`p-4 border-2 rounded-lg cursor-pointer hover:shadow-lg transition-all pit-entry transform hover:scale-102 ${
                      selectedRequest?.id === req.id ? 'border-racing-red bg-racing-red/5 shadow-lg' : 'border-gray-300 bg-white hover:border-racing-red'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className={`font-mono font-bold px-3 py-1 rounded-lg ${getMethodColor(req.method)}`}>
                        {req.method}
                      </span>
                      <span className="text-sm text-gray-600 font-semibold">
                        {new Date(req.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="text-sm text-gray-700 mt-2 flex justify-between font-semibold">
                      <span>⚡ {req.lap_time_ms}ms</span>
                      <span>📍 {req.ip_address}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Request Details - Diagnostic Report */}
            <div className="bg-white rounded-lg shadow-2xl p-6 border-4 border-racing-red">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 text-racing-red">
                <span>🔧</span> Diagnostic Report
              </h2>
              {selectedRequest ? (
                <div className="space-y-4">
                  <div className="bg-gradient-to-br from-racing-red/10 to-racing-red/5 p-4 rounded-lg border-2 border-racing-red/20">
                    <h3 className="font-bold text-racing-red mb-2">🏎️ Engine Type</h3>
                    <p className={`font-mono text-lg px-3 py-2 rounded-lg inline-block font-bold ${getMethodColor(selectedRequest.method)}`}>
                      {selectedRequest.method}
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border-2 border-green-200">
                    <h3 className="font-bold text-green-700 mb-2">⚡ Lap Time</h3>
                    <p className="text-3xl font-bold text-green-600">{selectedRequest.lap_time_ms}ms</p>
                  </div>

                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-lg border-2 border-gray-200">
                    <h3 className="font-bold text-gray-700 mb-2">📡 Headers</h3>
                    <pre className="bg-carbon-fiber text-green-400 p-3 rounded-lg overflow-x-auto text-xs font-mono border border-gray-600">
                      {JSON.stringify(selectedRequest.headers, null, 2)}
                    </pre>
                  </div>

                  {Object.keys(selectedRequest.query_params).length > 0 && (
                    <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-lg border-2 border-yellow-200">
                      <h3 className="font-bold text-yellow-700 mb-2">🔍 Query Params</h3>
                      <pre className="bg-carbon-fiber text-yellow-400 p-3 rounded-lg overflow-x-auto text-xs font-mono border border-gray-600">
                        {JSON.stringify(selectedRequest.query_params, null, 2)}
                      </pre>
                    </div>
                  )}

                  {selectedRequest.body && (
                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border-2 border-blue-200">
                      <h3 className="font-bold text-blue-700 mb-2">📦 Payload</h3>
                      <pre className="bg-carbon-fiber text-blue-400 p-3 rounded-lg overflow-x-auto text-xs font-mono max-h-64 border border-gray-600">
                        {selectedRequest.body}
                      </pre>
                    </div>
                  )}

                  <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border-2 border-purple-200">
                    <h3 className="font-bold text-purple-700 mb-2">📍 Source IP</h3>
                    <p className="font-mono text-purple-900 font-semibold text-lg">{selectedRequest.ip_address}</p>
                  </div>

                  <div className="bg-gradient-to-br from-racing-red/10 to-pit-orange/10 p-4 rounded-lg border-2 border-racing-red/30">
                    <h3 className="font-bold text-racing-red mb-2">🕐 Timestamp</h3>
                    <p className="text-gray-800 font-semibold">{new Date(selectedRequest.created_at).toLocaleString()}</p>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500 text-center py-12 font-medium text-lg">👈 Select a request to view diagnostic details</p>
              )}
            </div>
          </div>
        )}

        {/* Footer with Racing Stripe */}
        <div className="mt-12 text-center pb-8">
          <div className="h-1 bg-gradient-to-r from-racing-red via-pit-orange to-racing-red mb-4"></div>
          <p className="text-gray-600 text-sm font-semibold">🏁 Webhook Pitstop - Built for Race Speed</p>
          <p className="text-gray-500 text-xs mt-1">Inspect webhooks at lightning speed ⚡</p>
        </div>
      </div>
    </div>
  );
}

export default App;
