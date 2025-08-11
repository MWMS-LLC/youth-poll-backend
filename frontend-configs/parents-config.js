// Parents Site API Configuration
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://youth-poll-backend.onrender.com/api'  // Production API endpoint
  : 'http://localhost:8000';

export default API_BASE_URL;

