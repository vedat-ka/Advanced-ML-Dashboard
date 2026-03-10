import { useState } from 'react'
import { API_BASE_URL } from './dashboardShared'

function useApiClient() {
  const [pageMessage, setPageMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [loadingMap, setLoadingMap] = useState({})

  async function apiRequest(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers ?? {}),
      },
      ...options,
    })

    const contentType = response.headers.get('content-type') ?? ''
    const payload = contentType.includes('application/json') ? await response.json() : await response.text()

    if (!response.ok) {
      const detail = typeof payload === 'object' && payload !== null ? payload.detail : payload
      throw new Error(detail || `Anfrage fehlgeschlagen mit Status ${response.status}`)
    }

    return payload
  }

  function setLoading(key, isLoading) {
    setLoadingMap((current) => ({
      ...current,
      [key]: isLoading,
    }))
  }

  async function withRequestState(key, action, successMessage) {
    setLoading(key, true)
    setErrorMessage('')

    try {
      await action()
      if (successMessage) {
        setPageMessage(successMessage)
      }
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setLoading(key, false)
    }
  }

  return {
    apiBaseUrl: API_BASE_URL,
    pageMessage,
    errorMessage,
    loadingMap,
    setPageMessage,
    setErrorMessage,
    apiRequest,
    withRequestState,
  }
}

export default useApiClient