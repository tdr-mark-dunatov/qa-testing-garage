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
  const [allBays, setAllBays] = useState([]);
  const [showDashboard, setShowDashboard] = useState(false);
  const [bayName, setBayName] = useState('');
  const [bayDescription, setBayDescription] = useState('');
  const [showNamedForm, setShowNamedForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterMethod, setFilterMethod] = useState('ALL');
  const ws = useRef(null);

  const createQuickBay = async () => {
    const { data } = await axios.post(`${API_BASE}/api/bay/quick`);
    setPitId(data.pit_id);
    setPitLaneUrl(data.pit_lane_url);
    setRequests([]);
    setSelectedRequest(null);
    setShowDashboard(false);
    connectWebSocket(data.pit_id);
  };

  const createNamedBay = async () => {
    if (!bayName.trim()) return;
    try {
      const { data } = await axios.post(`${API_BASE}/api/bay/named`, {
        bay_name: bayName,
        description: bayDescription
      });
      setPitId(data.pit_id);
      setPitLaneUrl(data.pit_lane_url);
      setRequests([]);
      setSelectedRequest(null);
      setShowDashboard(false);
      setShowNamedForm(false);
      setBayName('');
      setBayDescription('');
      connectWebSocket(data.pit_id);
    } catch (error) {
      alert(error.response?.data?.detail || 'Error creating bay');
    }
  };

  const loadAllBays = async () => {
    const { data } = await axios.get(`${API_BASE}/api/bays`);
    setAllBays(data);
    setShowDashboard(true);
  };

  const openBay = (bay) => {
    setPitId(bay.bay_id);
    setPitLaneUrl(`${window.location.origin}/bay/${bay.bay_id}`);
    setShowDashboard(false);
    connectWebSocket(bay.bay_id);
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
    alert('🏁 Webhook Receiving Bay URL copied!');
  };

  const clearRequests = async () => {
    if (!confirm('🗑️ Clear all requests from this receiving bay?')) return;
    await axios.delete(`${API_BASE}/api/pit/${pitId}/requests`);
    setRequests([]);
    setSelectedRequest(null);
    setDiagnostics(null);
  };

  const deleteBay = async (bayId, bayName, event) => {
    // Prevent opening the bay when clicking delete (if called from list)
    if (event) event.stopPropagation();

    if (!confirm(`🗑️ Delete bay "${bayName || bayId}" completely?\n\nThis will delete:\n- The bay\n- All captured webhooks\n\nThis action cannot be undone.`)) return;

    try {
      await axios.delete(`${API_BASE}/api/bay/${bayId}`);

      // If we're viewing this bay, go back home
      if (pitId === bayId) {
        setPitId('');
        setRequests([]);
        setShowDashboard(false);
      } else {
        // Otherwise refresh the bay list
        await loadAllBays();
      }
    } catch (error) {
      alert(error.response?.data?.detail || 'Error deleting bay');
    }
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

  const filteredRequests = requests.filter(req => {
    // Filter by search term (searches in body, headers, query params)
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const matchesBody = req.body?.toLowerCase().includes(searchLower);
      const matchesHeaders = JSON.stringify(req.headers).toLowerCase().includes(searchLower);
      const matchesQuery = JSON.stringify(req.query_params).toLowerCase().includes(searchLower);
      const matchesIp = req.ip_address?.toLowerCase().includes(searchLower);
      if (!matchesBody && !matchesHeaders && !matchesQuery && !matchesIp) return false;
    }
    // Filter by HTTP method
    if (filterMethod !== 'ALL' && req.method !== filterMethod) return false;
    return true;
  });

  const copyAsCurl = (req) => {
    let curl = `curl -X ${req.method} "${pitLaneUrl}"`;
    if (req.headers && Object.keys(req.headers).length > 0) {
      Object.entries(req.headers).forEach(([key, value]) => {
        if (!key.toLowerCase().startsWith('host')) {
          curl += ` \\\n  -H "${key}: ${value}"`;
        }
      });
    }
    if (req.body) {
      curl += ` \\\n  -d '${req.body}'`;
    }
    navigator.clipboard.writeText(curl);
    alert('📋 cURL command copied! Paste in terminal to replay webhook.');
  };

  const exportWebhooks = () => {
    const data = JSON.stringify(filteredRequests, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `webhooks-${pitId}-${new Date().toISOString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
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

        {/* Bay Creation / Dashboard */}
        <div className="bg-white rounded-lg shadow-2xl p-6 mb-8 border-4 border-racing-red">
          {!pitId && !showDashboard ? (
            <div className="text-center py-8">
              <div className="flex gap-4 justify-center mb-6">
                <button
                  onClick={() => setShowNamedForm(!showNamedForm)}
                  className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 py-4 rounded-xl text-xl font-bold hover:scale-105 transform transition-all shadow-lg"
                >
                  🏗️ Create Named Bay
                </button>
                <button
                  onClick={createQuickBay}
                  className="bg-gradient-to-r from-racing-red to-racing-red-dark text-white px-8 py-4 rounded-xl text-xl font-bold hover:scale-105 transform transition-all shadow-lg"
                >
                  ⚡ Quick Bay
                </button>
                <button
                  onClick={loadAllBays}
                  className="bg-gradient-to-r from-green-600 to-green-700 text-white px-8 py-4 rounded-xl text-xl font-bold hover:scale-105 transform transition-all shadow-lg"
                >
                  📋 View All Bays
                </button>
              </div>

              {showNamedForm && (
                <div className="mt-6 max-w-md mx-auto bg-blue-50 p-6 rounded-lg border-2 border-blue-200">
                  <h3 className="text-xl font-bold text-blue-900 mb-4">Create Named Receiving Bay</h3>
                  <input
                    type="text"
                    placeholder="Bay name (e.g., hmf-integration)"
                    value={bayName}
                    onChange={(e) => setBayName(e.target.value)}
                    className="w-full p-3 border-2 border-blue-300 rounded-lg mb-3 font-semibold"
                  />
                  <textarea
                    placeholder="Description (optional)"
                    value={bayDescription}
                    onChange={(e) => setBayDescription(e.target.value)}
                    className="w-full p-3 border-2 border-blue-300 rounded-lg mb-4 font-medium"
                    rows="2"
                  />
                  <button
                    onClick={createNamedBay}
                    className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700"
                  >
                    Create Bay
                  </button>
                </div>
              )}

              <p className="text-gray-600 mt-6 text-lg font-medium">
                Named bays are reusable • Quick bays are temporary
              </p>
            </div>
          ) : !pitId && showDashboard ? (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-racing-red">📋 All Receiving Bays</h2>
                <button
                  onClick={() => setShowDashboard(false)}
                  className="bg-gray-500 text-white px-4 py-2 rounded-lg font-bold hover:bg-gray-600"
                >
                  ← Back
                </button>
              </div>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {allBays.map((bay) => (
                  <div
                    key={bay.bay_id}
                    onClick={() => openBay(bay)}
                    className="p-4 border-2 border-gray-300 rounded-lg hover:border-racing-red hover:bg-racing-red/5 cursor-pointer transition-all"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="font-bold text-lg text-racing-red">
                          {bay.is_named ? '🏗️' : '⚡'} {bay.bay_name || bay.bay_id}
                        </h3>
                        {bay.description && (
                          <p className="text-sm text-gray-600">{bay.description}</p>
                        )}
                        <p className="text-xs text-gray-500 mt-1">
                          ID: {bay.bay_id}
                        </p>
                      </div>
                      <div className="text-right flex flex-col items-end gap-2">
                        <div>
                          <p className="text-2xl font-bold text-racing-red">{bay.total_requests}</p>
                          <p className="text-xs text-gray-500">webhooks</p>
                          {bay.last_request_at && (
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(bay.last_request_at).toLocaleString()}
                            </p>
                          )}
                        </div>
                        <button
                          onClick={(e) => deleteBay(bay.bay_id, bay.bay_name, e)}
                          className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm font-bold transition-colors"
                          title="Delete this bay completely"
                        >
                          🗑️ Delete
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div>
              <div className="flex gap-4 items-center mb-4">
                <button
                  onClick={() => { setPitId(''); setRequests([]); setShowDashboard(false); }}
                  className="bg-gray-500 text-white px-6 py-4 rounded-lg hover:bg-gray-600 font-bold"
                >
                  ← Home
                </button>
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
                <button
                  onClick={() => deleteBay(pitId, pitId)}
                  className="bg-gradient-to-r from-red-700 to-red-900 text-white px-8 py-4 rounded-lg hover:scale-105 font-bold shadow-lg transform transition-all"
                  title="Delete this bay completely"
                >
                  🗑️ Delete Bay
                </button>
              </div>
              <p className="text-sm text-gray-700 font-semibold">
                ⚡ Receiving Bay ID: <code className="text-racing-red bg-racing-red/10 px-2 py-1 rounded font-mono">{pitId.substring(0, 8)}</code>
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
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold flex items-center gap-2 text-racing-red">
                  <span>📋</span> Activity ({filteredRequests.length}/{requests.length})
                </h2>
                <button
                  onClick={exportWebhooks}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold hover:bg-blue-700 text-sm"
                  disabled={filteredRequests.length === 0}
                >
                  📤 Export JSON
                </button>
              </div>

              {/* Search & Filter */}
              <div className="mb-4 space-y-2">
                <input
                  type="text"
                  placeholder="🔍 Search webhooks (dealId, body, headers...)"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg font-medium focus:border-racing-red focus:outline-none"
                />
                <div className="flex gap-2">
                  {['ALL', 'GET', 'POST', 'PUT', 'DELETE', 'PATCH'].map(method => (
                    <button
                      key={method}
                      onClick={() => setFilterMethod(method)}
                      className={`px-3 py-1 rounded-lg font-bold text-sm transition-all ${
                        filterMethod === method
                          ? 'bg-racing-red text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {method}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {filteredRequests.length === 0 && requests.length === 0 && (
                  <p className="text-gray-500 text-center py-8 font-medium">⏱️ Waiting for incoming requests...</p>
                )}
                {filteredRequests.length === 0 && requests.length > 0 && (
                  <p className="text-gray-500 text-center py-8 font-medium">🔍 No webhooks match your search</p>
                )}
                {filteredRequests.map((req) => (
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
                    <div className="mt-2 flex justify-between items-center">
                      <div className="text-sm text-gray-700 font-semibold">
                        <span>⚡ {req.lap_time_ms}ms</span>
                        <span className="ml-4">📍 {req.ip_address}</span>
                      </div>
                      <button
                        onClick={(e) => { e.stopPropagation(); copyAsCurl(req); }}
                        className="text-xs bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700 font-bold"
                        title="Copy as cURL command"
                      >
                        📋 cURL
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Request Details - Diagnostic Report */}
            <div className="bg-white rounded-lg shadow-2xl p-6 border-4 border-racing-red">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold flex items-center gap-2 text-racing-red">
                  <span>🔧</span> Diagnostic Report
                </h2>
                {selectedRequest && (
                  <button
                    onClick={() => copyAsCurl(selectedRequest)}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg font-bold hover:bg-gray-700 text-sm"
                  >
                    📋 Copy as cURL
                  </button>
                )}
              </div>
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
