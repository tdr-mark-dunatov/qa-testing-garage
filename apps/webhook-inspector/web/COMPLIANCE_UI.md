# 🎨 Compliance UI - Frontend Implementation

## New Components

### 1. `ComplianceDashboard.jsx`

**Location:** `src/components/ComplianceDashboard.jsx`

**Layout:**
```
┌─────────────────────────────────────────────┐
│  📊 Compliance Overview                      │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Active  │  │ With PII│  │ Alerts  │    │
│  │   12    │  │    3    │  │   5     │    │
│  └─────────┘  └─────────┘  └─────────┘    │
├─────────────────────────────────────────────┤
│  🚨 Recent PII Alerts                        │
│  ┌───────────────────────────────────────┐  │
│  │ hmf-integration | SSN, Credit Score   │  │
│  │ Owner: @mark.dunatov | 2 hours ago    │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │ tdc-test | Email, Phone              │  │
│  │ Owner: @jane.smith | 5 hours ago      │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

**API Calls:**
- `GET /api/compliance/summary` (on mount)
- `GET /api/compliance/alerts?limit=10` (on mount)
- Poll every 30 seconds for updates

---

### 2. Update `CreateBayForm.jsx`

**Add fields:**
```jsx
<input 
  name="owner_user" 
  placeholder="Your username"
  required
/>

<select name="owner_team">
  <option value="QA">QA</option>
  <option value="Dev">Dev</option>
  <option value="DevOps">DevOps</option>
</select>

<input 
  name="owner_repo" 
  placeholder="Repo (optional)"
/>

<input 
  name="owner_pipeline" 
  placeholder="Pipeline ID (optional)"
/>
```

**Update POST request:**
```js
const response = await fetch('/api/bay/named', {
  method: 'POST',
  body: JSON.stringify({
    bay_name: formData.bay_name,
    description: formData.description,
    owner_user: formData.owner_user,
    owner_team: formData.owner_team,
    owner_repo: formData.owner_repo,
    owner_pipeline: formData.owner_pipeline
  })
});
```

---

### 3. Update Bay List View

**Add PII indicator:**
```jsx
{bay.has_pii && (
  <span className="badge badge-warning">
    ⚠️ Contains PII
  </span>
)}
```

**Show owner info:**
```jsx
<div className="owner-info">
  <span>👤 {bay.owner_user}</span>
  <span>👥 {bay.owner_team}</span>
</div>
```

---

## WebSocket Updates

**Listen for PII alerts:**
```js
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.has_pii) {
    // Show notification
    showNotification(`⚠️ PII detected: ${data.pii_types.join(', ')}`);
    
    // Update bay status
    updateBayPIIStatus(data.pit_id);
  }
};
```

---

## Routing

**Add to `App.jsx`:**
```jsx
import ComplianceDashboard from './components/ComplianceDashboard';

<Route path="/compliance" element={<ComplianceDashboard />} />
```

**Add nav link:**
```jsx
<nav>
  <Link to="/">Dashboard</Link>
  <Link to="/compliance">🛡️ Compliance</Link>
</nav>
```

---

## Styling

**Compliance badge colors:**
- Green: No PII detected
- Yellow: PII detected, cleaned up
- Red: PII detected, still active

**Alert cards:**
- Use warning colors (yellow/orange)
- Include timestamp
- Show PII types as badges
- Link to bay details
