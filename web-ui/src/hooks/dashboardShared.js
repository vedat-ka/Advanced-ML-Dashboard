export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export const initialPrediction = {
  area: '52',
}

export function cloneValue(value) {
  return JSON.parse(JSON.stringify(value))
}