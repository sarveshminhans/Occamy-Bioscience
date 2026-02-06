# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
All API endpoints except `/login` require authentication. The system uses session-based authentication with Flask-Login.

### Login
**Endpoint:** `POST /login`

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "role": "admin",
  "redirect": "/admin/dashboard"
}
```

**Response (Error):**
```json
{
  "error": "Invalid credentials"
}
```

### Logout
**Endpoint:** `GET /logout`

**Response:** Redirects to `/login`

---

## Admin API Endpoints

### Get System Statistics
**Endpoint:** `GET /api/admin/stats`

**Auth Required:** Admin

**Response:**
```json
{
  "active_officers": 5,
  "total_meetings": 120,
  "total_sales": 45,
  "total_distance": 567.8,
  "b2c_sales": 30,
  "b2b_sales": 15,
  "state_activity": [
    {
      "state": "Uttar Pradesh",
      "meetings": 50,
      "sales": 20
    }
  ]
}
```

### Get All Field Officers
**Endpoint:** `GET /api/admin/users`

**Auth Required:** Admin

**Response:**
```json
[
  {
    "id": 2,
    "name": "Rajesh Kumar",
    "username": "rajesh_kumar",
    "email": "rajesh@occamy.com",
    "phone": "9876543210",
    "state": "Uttar Pradesh",
    "district": "Lucknow",
    "is_active": true,
    "created_at": "2024-02-06T10:30:00"
  }
]
```

### Create Field Officer
**Endpoint:** `POST /api/admin/users`

**Auth Required:** Admin

**Request:**
```json
{
  "username": "new_officer",
  "email": "officer@occamy.com",
  "password": "password123",
  "name": "New Officer",
  "state": "Punjab",
  "district": "Ludhiana",
  "phone": "9876543211"
}
```

**Response (Success):**
```json
{
  "success": true,
  "user_id": 3
}
```

**Response (Error):**
```json
{
  "error": "Username already exists"
}
```

### Get Activities
**Endpoint:** `GET /api/admin/activities`

**Auth Required:** Admin

**Query Parameters:**
- `days` (optional): Number of days to retrieve (default: 7)
- `user_id` (optional): Filter by specific user

**Example:** `/api/admin/activities?days=30&user_id=2`

**Response:**
```json
[
  {
    "name": "Rajesh Kumar",
    "state": "Uttar Pradesh",
    "date": "2024-02-06",
    "distance": 45.5,
    "meetings": 3,
    "sales": 2
  }
]
```

### Get All Meetings
**Endpoint:** `GET /api/admin/meetings`

**Auth Required:** Admin

**Response:**
```json
[
  {
    "id": 1,
    "officer_name": "Rajesh Kumar",
    "type": "one_on_one",
    "date": "2024-02-06T14:30:00",
    "person_name": "Ram Singh",
    "category": "Farmer",
    "village": null,
    "attendees": null,
    "location": "Rampur Village",
    "business_potential": "10-20 kg"
  },
  {
    "id": 2,
    "officer_name": "Priya Sharma",
    "type": "group",
    "date": "2024-02-06T11:00:00",
    "person_name": null,
    "category": null,
    "village": "Kishanganj",
    "attendees": 25,
    "location": "Kishanganj Village",
    "business_potential": null
  }
]
```

### Get All Sales
**Endpoint:** `GET /api/admin/sales`

**Auth Required:** Admin

**Response:**
```json
[
  {
    "id": 1,
    "officer_name": "Rajesh Kumar",
    "date": "2024-02-06T15:30:00",
    "type": "B2C",
    "customer": "Ram Singh",
    "product": "Calcium Supplement",
    "quantity": 5,
    "amount": 2500.0,
    "location": "Rampur Village",
    "repeat_order": false
  }
]
```

---

## Field Officer API Endpoints

### Start Work Day
**Endpoint:** `POST /api/field/worklog/start`

**Auth Required:** Field Officer

**Request:**
```json
{
  "latitude": 26.8467,
  "longitude": 80.9462,
  "odometer": 1000,
  "notes": "Starting work day"
}
```

**Response (Success):**
```json
{
  "success": true,
  "worklog_id": 1
}
```

**Response (Error):**
```json
{
  "error": "Work already started today"
}
```

### End Work Day
**Endpoint:** `POST /api/field/worklog/end`

**Auth Required:** Field Officer

**Request:**
```json
{
  "latitude": 26.9467,
  "longitude": 80.8462,
  "odometer": 1050
}
```

**Response:**
```json
{
  "success": true
}
```

### Check Work Status
**Endpoint:** `GET /api/field/worklog/status`

**Auth Required:** Field Officer

**Response:**
```json
{
  "status": "started",
  "start_time": "2024-02-06T09:00:00",
  "end_time": null
}
```

Possible status values:
- `not_started` - No work log for today
- `started` - Work in progress
- `ended` - Work completed for today

### Log Meeting
**Endpoint:** `POST /api/field/meeting`

**Auth Required:** Field Officer

**One-on-One Meeting Request:**
```json
{
  "meeting_type": "one_on_one",
  "person_name": "Ram Singh",
  "person_category": "Farmer",
  "contact_number": "9876543210",
  "business_potential": "10-20 kg",
  "latitude": 26.8467,
  "longitude": 80.9462,
  "location_name": "Rampur Village",
  "notes": "Interested in calcium supplement"
}
```

**Group Meeting Request:**
```json
{
  "meeting_type": "group",
  "village": "Kishanganj",
  "attendees_count": 25,
  "group_meeting_type": "Training Session",
  "latitude": 26.8467,
  "longitude": 80.9462,
  "location_name": "Kishanganj Village Hall",
  "notes": "Conducted product training"
}
```

**Response:**
```json
{
  "success": true,
  "meeting_id": 1
}
```

### Log Sample Distribution
**Endpoint:** `POST /api/field/sample`

**Auth Required:** Field Officer

**Request:**
```json
{
  "recipient_name": "Ram Singh",
  "recipient_type": "Farmer",
  "product_name": "Calcium Supplement",
  "quantity": 1.0,
  "unit": "kg",
  "purpose": "trial",
  "latitude": 26.8467,
  "longitude": 80.9462,
  "location_name": "Rampur Village",
  "notes": "First time trial"
}
```

**Response:**
```json
{
  "success": true,
  "sample_id": 1
}
```

### Record Sale
**Endpoint:** `POST /api/field/sale`

**Auth Required:** Field Officer

**Request:**
```json
{
  "sale_type": "B2C",
  "customer_name": "Ram Singh",
  "customer_type": "Farmer",
  "contact_number": "9876543210",
  "product_sku": "NUT-001",
  "product_name": "Calcium Supplement",
  "pack_size": "1 kg",
  "quantity": 5,
  "unit_price": 500,
  "total_amount": 2500,
  "mode": "direct",
  "is_repeat_order": false,
  "latitude": 26.8467,
  "longitude": 80.9462,
  "location_name": "Rampur Village",
  "notes": "Cash payment"
}
```

**Response:**
```json
{
  "success": true,
  "sale_id": 1
}
```

### Log GPS Location
**Endpoint:** `POST /api/field/location`

**Auth Required:** Field Officer

**Request:**
```json
{
  "latitude": 26.8467,
  "longitude": 80.9462,
  "accuracy": 10.5,
  "activity_type": "tracking"
}
```

**Response:**
```json
{
  "success": true
}
```

### Get My Activities
**Endpoint:** `GET /api/field/my-activities`

**Auth Required:** Field Officer

**Query Parameters:**
- `days` (optional): Number of days (default: 7)

**Example:** `/api/field/my-activities?days=30`

**Response:**
```json
{
  "meetings": 15,
  "sales": 8,
  "samples": 5,
  "distance": 234.5
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Admin access required"
}
```

### 400 Bad Request
```json
{
  "error": "Invalid request data"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Data Models

### User
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "role": "admin|field_officer",
  "name": "string",
  "state": "string",
  "district": "string",
  "phone": "string",
  "is_active": true,
  "created_at": "ISO 8601 datetime"
}
```

### WorkLog
```json
{
  "id": 1,
  "user_id": 1,
  "date": "YYYY-MM-DD",
  "start_time": "ISO 8601 datetime",
  "end_time": "ISO 8601 datetime",
  "start_location_lat": 26.8467,
  "start_location_lng": 80.9462,
  "end_location_lat": 26.9467,
  "end_location_lng": 80.8462,
  "odometer_start": 1000,
  "odometer_end": 1050,
  "distance_traveled": 50,
  "notes": "string",
  "status": "started|ended"
}
```

### Meeting
```json
{
  "id": 1,
  "user_id": 1,
  "meeting_type": "one_on_one|group",
  "date": "ISO 8601 datetime",
  "person_name": "string (one_on_one only)",
  "person_category": "Farmer|Seller|Influencer (one_on_one only)",
  "contact_number": "string (optional)",
  "business_potential": "string (one_on_one only)",
  "village": "string (group only)",
  "attendees_count": 25,
  "group_meeting_type": "string (group only)",
  "location_lat": 26.8467,
  "location_lng": 80.9462,
  "location_name": "string",
  "notes": "string",
  "photos": "JSON array of URLs"
}
```

### SampleDistribution
```json
{
  "id": 1,
  "user_id": 1,
  "date": "ISO 8601 datetime",
  "recipient_name": "string",
  "recipient_type": "Farmer|Distributor|Seller",
  "product_name": "string",
  "quantity": 1.0,
  "unit": "kg|g|pieces",
  "purpose": "trial|demo|follow-up",
  "location_lat": 26.8467,
  "location_lng": 80.9462,
  "location_name": "string",
  "notes": "string"
}
```

### Sale
```json
{
  "id": 1,
  "user_id": 1,
  "date": "ISO 8601 datetime",
  "sale_type": "B2C|B2B",
  "customer_name": "string",
  "customer_type": "Farmer|Distributor|Reseller",
  "contact_number": "string",
  "product_sku": "string",
  "product_name": "string",
  "pack_size": "string",
  "quantity": 5,
  "unit_price": 500.0,
  "total_amount": 2500.0,
  "mode": "direct|via_distributor",
  "is_repeat_order": false,
  "location_lat": 26.8467,
  "location_lng": 80.9462,
  "location_name": "string",
  "notes": "string"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Recommended: 100 requests per minute per user
- Consider implementing Flask-Limiter

## Pagination

Currently returns all results. For production with large datasets:
- Add `page` and `per_page` query parameters
- Default: 50 items per page

## WebSocket Support

Not currently implemented. For real-time updates:
- Consider Flask-SocketIO
- Useful for live location tracking on admin dashboard

## File Uploads

Photo upload endpoint not yet implemented. When added:
- Max file size: 16MB
- Allowed formats: JPG, PNG, GIF, PDF
- Storage: local filesystem or S3

---

## Testing the API

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  -c cookies.txt
```

**Get Stats (with session):**
```bash
curl http://localhost:5000/api/admin/stats \
  -b cookies.txt
```

### Using Python

```python
import requests

# Login
session = requests.Session()
login_data = {"username": "admin", "password": "admin123"}
response = session.post("http://localhost:5000/login", json=login_data)
print(response.json())

# Get stats
stats = session.get("http://localhost:5000/api/admin/stats")
print(stats.json())
```

### Using JavaScript

```javascript
// Login
const login = async () => {
  const response = await fetch('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username: 'admin', password: 'admin123'})
  });
  return response.json();
};

// Get stats
const getStats = async () => {
  const response = await fetch('/api/admin/stats');
  return response.json();
};
```

---

## Best Practices

1. **Always check HTTP status codes**
2. **Handle errors gracefully**
3. **Use HTTPS in production**
4. **Implement CSRF protection for state-changing operations**
5. **Add request validation**
6. **Log API usage for monitoring**
7. **Implement rate limiting in production**
8. **Use API versioning for future updates**
