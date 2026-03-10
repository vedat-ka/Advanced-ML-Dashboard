import { useDeferredValue, useState } from 'react'
import { initialPrediction } from './dashboardShared'

function useLinearRegressionWorkflow({ apiRequest, withRequestState }) {
  const [summary, setSummary] = useState(null)
  const [history, setHistory] = useState([])
  const [actualPriceInputs, setActualPriceInputs] = useState({})
  const [predictForm, setPredictForm] = useState(initialPrediction)
  const [finetunedForm, setFinetunedForm] = useState(initialPrediction)
  const [compareForm, setCompareForm] = useState(initialPrediction)
  const [historyLimit, setHistoryLimit] = useState('20')
  const [summaryLimit, setSummaryLimit] = useState('100')
  const [finetuneLimit, setFinetuneLimit] = useState('')
  const [historyFilter, setHistoryFilter] = useState('')
  const [predictResult, setPredictResult] = useState(null)
  const [finetunedResult, setFinetunedResult] = useState(null)
  const [compareResult, setCompareResult] = useState(null)
  const [finetuneResult, setFinetuneResult] = useState(null)

  const deferredHistoryFilter = useDeferredValue(historyFilter)
  const latestMarketPriceRows = history.slice(0, 5)
  const filteredHistory = history.filter((item) => {
    const query = deferredHistoryFilter.trim().toLowerCase()
    if (!query) {
      return true
    }

    return [
      String(item.id),
      String(item.area),
      String(item.predicted_price),
      String(item.actual_price ?? ''),
      item.model_source,
      item.created_at,
    ].some((value) => value.toLowerCase().includes(query))
  })

  async function loadHistory(limit = Number(historyLimit) || 20) {
    await withRequestState('history', async () => {
      const result = await apiRequest(`/predictions?limit=${limit}`)
      setHistory(result.items)
      setActualPriceInputs((current) => {
        const nextInputs = {}
        result.items.forEach((item) => {
          nextInputs[item.id] = current[item.id] ?? (item.actual_price ?? '')
        })
        return nextInputs
      })
    })
  }

  async function loadSummary(limit = Number(summaryLimit) || 100) {
    await withRequestState('summary', async () => {
      const result = await apiRequest(`/reporting/summary?limit=${limit}`)
      setSummary(result)
    })
  }

  async function handlePredict(event) {
    event.preventDefault()
    await withRequestState('predict', async () => {
      const result = await apiRequest('/predict', {
        method: 'POST',
        body: JSON.stringify({ area: Number(predictForm.area) }),
      })
      setPredictResult(result)
      await Promise.all([loadHistory(), loadSummary()])
    }, 'Vorhersage mit dem Originalmodell wurde erstellt.')
  }

  async function handleFinetunedPredict(event) {
    event.preventDefault()
    await withRequestState('predict-finetuned', async () => {
      const result = await apiRequest('/predict-finetuned', {
        method: 'POST',
        body: JSON.stringify({ area: Number(finetunedForm.area) }),
      })
      setFinetunedResult(result)
      await Promise.all([loadHistory(), loadSummary()])
    }, 'Vorhersage mit dem finetunten Modell wurde erstellt.')
  }

  async function handleCompare(event) {
    event.preventDefault()
    await withRequestState('compare', async () => {
      const result = await apiRequest('/compare-models', {
        method: 'POST',
        body: JSON.stringify({ area: Number(compareForm.area) }),
      })
      setCompareResult(result)
    }, 'Modellvergleich wurde aktualisiert.')
  }

  async function handleFinetune(event) {
    event.preventDefault()
    const normalizedLimit = finetuneLimit.trim()
    const query = normalizedLimit ? `?limit=${Number(normalizedLimit)}` : ''

    await withRequestState('finetune', async () => {
      const result = await apiRequest(`/finetune-model${query}`, {
        method: 'POST',
      })
      setFinetuneResult(result)
    }, 'Finetuntes Modell wurde erfolgreich mit echten Vergleichspreisen trainiert.')
  }

  function updateActualPriceInput(predictionId, value) {
    setActualPriceInputs((current) => ({
      ...current,
      [predictionId]: value,
    }))
  }

  async function handleSaveActualPrice(predictionId) {
    const rawValue = String(actualPriceInputs[predictionId] ?? '').trim()

    await withRequestState(`actual-price-${predictionId}`, async () => {
      await apiRequest(`/predictions/${predictionId}/actual-price`, {
        method: 'PATCH',
        body: JSON.stringify({
          actual_price: rawValue ? Number(rawValue) : null,
        }),
      })
      await Promise.all([loadHistory(), loadSummary()])
    }, rawValue ? 'Vergleichspreis wurde gespeichert.' : 'Vergleichspreis wurde entfernt.')
  }

  return {
    summary,
    history,
    actualPriceInputs,
    predictForm,
    finetunedForm,
    compareForm,
    historyLimit,
    summaryLimit,
    finetuneLimit,
    historyFilter,
    predictResult,
    finetunedResult,
    compareResult,
    finetuneResult,
    latestMarketPriceRows,
    filteredHistory,
    setPredictForm,
    setFinetunedForm,
    setCompareForm,
    setHistoryLimit,
    setSummaryLimit,
    setFinetuneLimit,
    setHistoryFilter,
    loadHistory,
    loadSummary,
    handlePredict,
    handleFinetunedPredict,
    handleCompare,
    handleFinetune,
    updateActualPriceInput,
    handleSaveActualPrice,
  }
}

export default useLinearRegressionWorkflow