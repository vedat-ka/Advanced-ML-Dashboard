import { startTransition, useEffect, useState } from 'react'
import { API_BASE_URL } from './dashboardShared'
import useAlgorithmWorkflow from './useAlgorithmWorkflow'
import useApiClient from './useApiClient'
import useLinearRegressionWorkflow from './useLinearRegressionWorkflow'

function useDashboardData() {
  const [status, setStatus] = useState(null)
  const [schema, setSchema] = useState([])
  const [algorithms, setAlgorithms] = useState([])
  const [selectedAlgorithmKey, setSelectedAlgorithmKey] = useState('')
  const {
    apiBaseUrl,
    pageMessage,
    errorMessage,
    loadingMap,
    setPageMessage,
    setErrorMessage,
    apiRequest,
    withRequestState,
  } = useApiClient()

  const selectedAlgorithm = algorithms.find((item) => item.algorithm_key === selectedAlgorithmKey) ?? null

  const linearRegression = useLinearRegressionWorkflow({
    apiRequest,
    withRequestState,
  })

  const algorithmWorkflow = useAlgorithmWorkflow({
    apiRequest,
    withRequestState,
    selectedAlgorithm,
    setErrorMessage,
    setPageMessage,
  })

  useEffect(() => {
    loadRootStatus()
    linearRegression.loadHistory(20)
    linearRegression.loadSummary(100)
    loadSchema()
    loadAlgorithms()
  }, [])

  useEffect(() => {
    if (!selectedAlgorithmKey && algorithms.length > 0) {
      const preferredAlgorithm = algorithms.find((item) => item.algorithm_key === 'decision_tree_classifier')
      setSelectedAlgorithmKey(preferredAlgorithm?.algorithm_key ?? algorithms[0].algorithm_key)
    }
  }, [algorithms, selectedAlgorithmKey])

  async function loadRootStatus() {
    await withRequestState('status', async () => {
      const result = await apiRequest('/')
      startTransition(() => {
        setStatus(result)
      })
    })
  }

  async function loadSchema() {
    await withRequestState('schema', async () => {
      const result = await apiRequest('/database/schema')
      startTransition(() => {
        setSchema(result.items)
      })
    })
  }

  async function loadAlgorithms() {
    await withRequestState('algorithms', async () => {
      const result = await apiRequest('/ml/algorithms')
      startTransition(() => {
        setAlgorithms(result.items)
      })
    })
  }

  return {
    apiBaseUrl,
    status,
    schema,
    algorithms,
    selectedAlgorithmKey,
    selectedAlgorithm,
    pageMessage,
    errorMessage,
    loadingMap,
    setSelectedAlgorithmKey,
    loadRootStatus,
    loadSchema,
    ...linearRegression,
    ...algorithmWorkflow,
  }
}

export default useDashboardData