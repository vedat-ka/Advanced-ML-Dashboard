import { useEffect, useState } from 'react'
import { cloneValue } from './dashboardShared'

function useAlgorithmWorkflow({ apiRequest, withRequestState, selectedAlgorithm, setErrorMessage, setPageMessage }) {
  const [algorithmHyperparameters, setAlgorithmHyperparameters] = useState({})
  const [trainingSamples, setTrainingSamples] = useState([])
  const [finetuningSamples, setFinetuningSamples] = useState([])
  const [finetuningSampleDraft, setFinetuningSampleDraft] = useState({})
  const [finetuningSampleNote, setFinetuningSampleNote] = useState('')
  const [algorithmPredictionInput, setAlgorithmPredictionInput] = useState({})
  const [selectedAlgorithmModel, setSelectedAlgorithmModel] = useState(null)
  const [selectedAlgorithmFinetunedModel, setSelectedAlgorithmFinetunedModel] = useState(null)
  const [customFinetuneLimit, setCustomFinetuneLimit] = useState('')
  const [customTrainingResult, setCustomTrainingResult] = useState(null)
  const [customPredictResult, setCustomPredictResult] = useState(null)
  const [customFinetuneResult, setCustomFinetuneResult] = useState(null)
  const [customFinetunedPredictResult, setCustomFinetunedPredictResult] = useState(null)
  const [customCompareResult, setCustomCompareResult] = useState(null)

  useEffect(() => {
    if (!selectedAlgorithm) {
      return
    }

    const nextParameters = {}
    selectedAlgorithm.hyperparameters.forEach((parameter) => {
      nextParameters[parameter.name] = parameter.default ?? ''
    })

    setAlgorithmHyperparameters(nextParameters)
    setTrainingSamples(cloneValue(selectedAlgorithm.default_training_samples))
    setFinetuningSampleDraft(cloneValue(selectedAlgorithm.default_training_samples[0] ?? {}))
    setFinetuningSampleNote('')
    setFinetuningSamples([])
    setAlgorithmPredictionInput(cloneValue(selectedAlgorithm.default_prediction_input))
    setCustomTrainingResult(null)
    setCustomPredictResult(null)
    setCustomFinetuneResult(null)
    setCustomFinetunedPredictResult(null)
    setCustomCompareResult(null)
    loadSelectedAlgorithmModel(selectedAlgorithm.algorithm_key)
    loadSelectedAlgorithmFinetunedModel(selectedAlgorithm.algorithm_key)
    loadAlgorithmFinetuningSamples(selectedAlgorithm.algorithm_key)
  }, [selectedAlgorithm])

  async function loadSelectedAlgorithmModel(algorithmKey) {
    await withRequestState('selected-model', async () => {
      const result = await apiRequest(`/ml/algorithms/${algorithmKey}/model`)
      setSelectedAlgorithmModel(result)
    })
  }

  async function loadSelectedAlgorithmFinetunedModel(algorithmKey) {
    await withRequestState('selected-finetuned-model', async () => {
      const result = await apiRequest(`/ml/algorithms/${algorithmKey}/finetuned-model`)
      setSelectedAlgorithmFinetunedModel(result)
    })
  }

  async function loadAlgorithmFinetuningSamples(algorithmKey) {
    await withRequestState('finetuning-samples', async () => {
      const result = await apiRequest(`/ml/algorithms/${algorithmKey}/finetuning-samples?limit=50`)
      setFinetuningSamples(result.items)
    })
  }

  async function handleCustomTraining(event) {
    event.preventDefault()

    if (!selectedAlgorithm) {
      setErrorMessage('Bitte zuerst einen Algorithmus auswaehlen.')
      return
    }

    await withRequestState('custom-train', async () => {
      const result = await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/train`, {
        method: 'POST',
        body: JSON.stringify({
          training_samples: trainingSamples,
          hyperparameters: algorithmHyperparameters,
        }),
      })
      setCustomTrainingResult(result)
      await loadSelectedAlgorithmModel(selectedAlgorithm.algorithm_key)
    }, 'Algorithmus-Modell wurde erfolgreich trainiert.')
  }

  async function handleCustomFinetune(event) {
    event.preventDefault()

    if (!selectedAlgorithm) {
      setErrorMessage('Bitte zuerst einen Algorithmus auswaehlen.')
      return
    }

    const normalizedLimit = customFinetuneLimit.trim()
    const query = normalizedLimit ? `?limit=${Number(normalizedLimit)}` : ''

    await withRequestState('custom-finetune', async () => {
      const result = await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/finetune${query}`, {
        method: 'POST',
      })
      setCustomFinetuneResult(result)
      await loadSelectedAlgorithmFinetunedModel(selectedAlgorithm.algorithm_key)
    }, 'Finetuntes Algorithmus-Modell wurde erfolgreich aus echten SQLite-Finetuning-Daten trainiert.')
  }

  async function handleSaveFinetuningSample(event) {
    event.preventDefault()

    if (!selectedAlgorithm) {
      setErrorMessage('Bitte zuerst einen Algorithmus auswaehlen.')
      return
    }

    await withRequestState('save-finetuning-sample', async () => {
      await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/finetuning-samples`, {
        method: 'POST',
        body: JSON.stringify({
          sample: finetuningSampleDraft,
          note: finetuningSampleNote,
        }),
      })
      setFinetuningSampleDraft(cloneValue(selectedAlgorithm.default_training_samples[0] ?? {}))
      setFinetuningSampleNote('')
      await loadAlgorithmFinetuningSamples(selectedAlgorithm.algorithm_key)
    }, 'Reales Finetuning-Sample wurde in SQLite gespeichert.')
  }

  async function handleDeleteFinetuningSample(sampleId) {
    if (!selectedAlgorithm) {
      return
    }

    await withRequestState(`delete-finetuning-sample-${sampleId}`, async () => {
      await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/finetuning-samples/${sampleId}`, {
        method: 'DELETE',
      })
      await loadAlgorithmFinetuningSamples(selectedAlgorithm.algorithm_key)
    }, 'Finetuning-Sample wurde entfernt.')
  }

  async function handleCustomPredict(event) {
    event.preventDefault()

    if (!selectedAlgorithm) {
      setErrorMessage('Bitte zuerst einen Algorithmus auswaehlen.')
      return
    }

    if (!selectedAlgorithmModel?.trained) {
      setErrorMessage(`Fuer ${selectedAlgorithm.label} existiert noch kein trainiertes Modell. Bitte zuerst trainieren.`)
      return
    }

    await withRequestState('custom-predict', async () => {
      const result = await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/predict`, {
        method: 'POST',
        body: JSON.stringify({
          prediction_input: algorithmPredictionInput,
        }),
      })
      setCustomPredictResult(result)
      await loadSelectedAlgorithmModel(selectedAlgorithm.algorithm_key)
    }, 'Vorhersage mit dem ausgewaehlten Algorithmus wurde erstellt.')
  }

  async function handleCustomFinetunedPredict(event) {
    event.preventDefault()

    if (!selectedAlgorithm) {
      setErrorMessage('Bitte zuerst einen Algorithmus auswaehlen.')
      return
    }

    if (!selectedAlgorithmFinetunedModel?.trained) {
      setErrorMessage(`Fuer ${selectedAlgorithm.label} existiert noch kein finetuntes Modell. Bitte zuerst Finetuning starten.`)
      return
    }

    await withRequestState('custom-predict-finetuned', async () => {
      const result = await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/predict-finetuned`, {
        method: 'POST',
        body: JSON.stringify({
          prediction_input: algorithmPredictionInput,
        }),
      })
      setCustomFinetunedPredictResult(result)
      await loadSelectedAlgorithmFinetunedModel(selectedAlgorithm.algorithm_key)
    }, 'Vorhersage mit dem finetunten Algorithmus-Modell wurde erstellt.')
  }

  async function handleCustomCompare(event) {
    event.preventDefault()

    if (!selectedAlgorithm) {
      setErrorMessage('Bitte zuerst einen Algorithmus auswaehlen.')
      return
    }

    if (!selectedAlgorithmFinetunedModel?.trained) {
      setErrorMessage(`Fuer ${selectedAlgorithm.label} existiert noch kein finetuntes Modell. Bitte zuerst Finetuning starten.`)
      return
    }

    await withRequestState('custom-compare', async () => {
      const result = await apiRequest(`/ml/algorithms/${selectedAlgorithm.algorithm_key}/compare-models`, {
        method: 'POST',
        body: JSON.stringify({
          prediction_input: algorithmPredictionInput,
        }),
      })
      setCustomCompareResult(result)
    }, 'Modellvergleich fuer den ausgewaehlten Algorithmus wurde aktualisiert.')
  }

  function addTrainingSample() {
    if (!selectedAlgorithm) {
      return
    }

    const emptySample = {}
    selectedAlgorithm.training_fields.forEach((field) => {
      emptySample[field.name] = ''
    })
    setTrainingSamples((current) => [...current, emptySample])
  }

  function removeTrainingSample(index) {
    setTrainingSamples((current) => current.filter((_, sampleIndex) => sampleIndex !== index))
  }

  function updateTrainingSample(index, fieldName, value) {
    setTrainingSamples((current) =>
      current.map((sample, sampleIndex) => {
        if (sampleIndex !== index) {
          return sample
        }

        return {
          ...sample,
          [fieldName]: value,
        }
      }),
    )
  }

  function updateHyperparameter(parameterName, value) {
    setAlgorithmHyperparameters((current) => ({
      ...current,
      [parameterName]: value,
    }))
  }

  function updatePredictionInput(fieldName, value) {
    setAlgorithmPredictionInput((current) => ({
      ...current,
      [fieldName]: value,
    }))
  }

  function updateFinetuningSampleDraft(fieldName, value) {
    setFinetuningSampleDraft((current) => ({
      ...current,
      [fieldName]: value,
    }))
  }

  function applyPredictionExample(example) {
    setAlgorithmPredictionInput(cloneValue(example.input))
    setPageMessage(`Beispiel geladen: ${example.label}`)
    setErrorMessage('')
  }

  return {
    algorithmHyperparameters,
    trainingSamples,
    finetuningSamples,
    finetuningSampleDraft,
    finetuningSampleNote,
    algorithmPredictionInput,
    selectedAlgorithmModel,
    selectedAlgorithmFinetunedModel,
    customFinetuneLimit,
    customTrainingResult,
    customPredictResult,
    customFinetuneResult,
    customFinetunedPredictResult,
    customCompareResult,
    setCustomFinetuneLimit,
    setFinetuningSampleNote,
    handleCustomTraining,
    handleCustomFinetune,
    handleSaveFinetuningSample,
    handleDeleteFinetuningSample,
    handleCustomPredict,
    handleCustomFinetunedPredict,
    handleCustomCompare,
    addTrainingSample,
    removeTrainingSample,
    updateTrainingSample,
    updateHyperparameter,
    updatePredictionInput,
    updateFinetuningSampleDraft,
    applyPredictionExample,
  }
}

export default useAlgorithmWorkflow