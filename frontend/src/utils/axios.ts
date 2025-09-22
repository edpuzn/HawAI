import Axios from 'axios'

const axios = Axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
  withCredentials: true
})

export default axios


