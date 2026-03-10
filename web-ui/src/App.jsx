import {
  AlgorithmFinetunedUsageSection,
  AlgorithmFinetuningSection,
  AlgorithmInsightsSection,
  AlgorithmWorkspace,
} from './components/algorithms'
import { AlgorithmNav, HeroHeader, StatsSection } from './components/common'
import {
  LinearRegressionDataSections,
  LinearRegressionFinetuneSection,
  LinearRegressionTools,
  MarketPriceSection,
} from './components/linear-regression'
import { useDashboardData } from './hooks'

function App() {
  const {
    apiBaseUrl,
    status,
    summary,
    actualPriceInputs,
    schema,
    algorithms,
    selectedAlgorithmKey,
    selectedAlgorithm,
    algorithmHyperparameters,
    trainingSamples,
    finetuningSamples,
    finetuningSampleDraft,
    finetuningSampleNote,
    algorithmPredictionInput,
    selectedAlgorithmModel,
    selectedAlgorithmFinetunedModel,
    predictForm,
    finetunedForm,
    compareForm,
    historyLimit,
    summaryLimit,
    finetuneLimit,
    customFinetuneLimit,
    historyFilter,
    predictResult,
    finetunedResult,
    compareResult,
    finetuneResult,
    customTrainingResult,
    customPredictResult,
    customFinetuneResult,
    customFinetunedPredictResult,
    customCompareResult,
    pageMessage,
    errorMessage,
    loadingMap,
    latestMarketPriceRows,
    filteredHistory,
    setSelectedAlgorithmKey,
    setPredictForm,
    setFinetunedForm,
    setCompareForm,
    setHistoryLimit,
    setSummaryLimit,
    setFinetuneLimit,
    setCustomFinetuneLimit,
    setHistoryFilter,
    setFinetuningSampleNote,
    loadRootStatus,
    loadHistory,
    loadSummary,
    loadSchema,
    handlePredict,
    handleFinetunedPredict,
    handleCompare,
    handleFinetune,
    updateActualPriceInput,
    handleSaveActualPrice,
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
  } = useDashboardData()

  return (
    <div className="app-shell">
      <div className="background-orb orb-left" />
      <div className="background-orb orb-right" />

      <HeroHeader
        apiBaseUrl={apiBaseUrl}
        statusMessage={status?.message ?? 'Service-Informationen werden geladen...'}
        onRefresh={loadRootStatus}
        isLoading={loadingMap.status}
      />

      {(pageMessage || errorMessage) && (
        <section className="message-row">
          {pageMessage && <div className="message success">{pageMessage}</div>}
          {errorMessage && <div className="message error">{errorMessage}</div>}
        </section>
      )}

      <AlgorithmNav
        algorithms={algorithms}
        selectedAlgorithmKey={selectedAlgorithmKey}
        onSelectAlgorithm={setSelectedAlgorithmKey}
      />

      <StatsSection
        selectedAlgorithmKey={selectedAlgorithmKey}
        summary={summary}
        selectedAlgorithm={selectedAlgorithm}
        selectedAlgorithmModel={selectedAlgorithmModel}
      />

      <main className="dashboard-grid">
        {selectedAlgorithmKey === 'linear_regression' && (
          <LinearRegressionTools
            predictForm={predictForm}
            finetunedForm={finetunedForm}
            compareForm={compareForm}
            onPredictAreaChange={(area) => setPredictForm({ area })}
            onFinetunedAreaChange={(area) => setFinetunedForm({ area })}
            onCompareAreaChange={(area) => setCompareForm({ area })}
            onPredict={handlePredict}
            onFinetunedPredict={handleFinetunedPredict}
            onCompare={handleCompare}
            predictResult={predictResult}
            finetunedResult={finetunedResult}
            compareResult={compareResult}
            loadingMap={loadingMap}
          />
        )}

        {selectedAlgorithmKey === 'linear_regression' && (
          <MarketPriceSection
            latestMarketPriceRows={latestMarketPriceRows}
            summary={summary}
            actualPriceInputs={actualPriceInputs}
            onActualPriceInputChange={updateActualPriceInput}
            onSaveActualPrice={handleSaveActualPrice}
            loadingMap={loadingMap}
          />
        )}

        <AlgorithmWorkspace
          selectedAlgorithm={selectedAlgorithm}
          algorithmHyperparameters={algorithmHyperparameters}
          trainingSamples={trainingSamples}
          algorithmPredictionInput={algorithmPredictionInput}
          selectedAlgorithmModel={selectedAlgorithmModel}
          selectedAlgorithmFinetunedModel={selectedAlgorithmFinetunedModel}
          loadingMap={loadingMap}
          customTrainingResult={customTrainingResult}
          customPredictResult={customPredictResult}
          onHyperparameterChange={updateHyperparameter}
          onTrainingSampleChange={updateTrainingSample}
          onAddTrainingSample={addTrainingSample}
          onRemoveTrainingSample={removeTrainingSample}
          onPredictionInputChange={updatePredictionInput}
          onApplyPredictionExample={applyPredictionExample}
          onTrain={handleCustomTraining}
          onPredict={handleCustomPredict}
        />

        {selectedAlgorithmKey !== 'linear_regression' && selectedAlgorithm && (
          <AlgorithmFinetuningSection
            selectedAlgorithm={selectedAlgorithm}
            finetuningSampleDraft={finetuningSampleDraft}
            finetuningSampleNote={finetuningSampleNote}
            finetuningSamples={finetuningSamples}
            customFinetuneLimit={customFinetuneLimit}
            loadingMap={loadingMap}
            onFinetuningSampleDraftChange={updateFinetuningSampleDraft}
            onFinetuningSampleNoteChange={setFinetuningSampleNote}
            onSaveFinetuningSample={handleSaveFinetuningSample}
            onDeleteFinetuningSample={handleDeleteFinetuningSample}
            onCustomFinetuneLimitChange={setCustomFinetuneLimit}
            onFinetune={handleCustomFinetune}
            customFinetuneResult={customFinetuneResult}
          />
        )}

        {selectedAlgorithmKey !== 'linear_regression' && selectedAlgorithm && (
          <AlgorithmFinetunedUsageSection
            selectedAlgorithm={selectedAlgorithm}
            algorithmPredictionInput={algorithmPredictionInput}
            selectedAlgorithmFinetunedModel={selectedAlgorithmFinetunedModel}
            loadingMap={loadingMap}
            customFinetunedPredictResult={customFinetunedPredictResult}
            customCompareResult={customCompareResult}
            onPredictionInputChange={updatePredictionInput}
            onApplyPredictionExample={applyPredictionExample}
            onFinetunedPredict={handleCustomFinetunedPredict}
            onCompare={handleCustomCompare}
          />
        )}

        {selectedAlgorithmKey === 'linear_regression' && (
          <LinearRegressionFinetuneSection
            finetuneLimit={finetuneLimit}
            loadingMap={loadingMap}
            finetuneResult={finetuneResult}
            onFinetuneLimitChange={setFinetuneLimit}
            onFinetune={handleFinetune}
          />
        )}

        {selectedAlgorithmKey === 'linear_regression' ? (
          <LinearRegressionDataSections
            summary={summary}
            summaryLimit={summaryLimit}
            historyLimit={historyLimit}
            historyFilter={historyFilter}
            filteredHistory={filteredHistory}
            actualPriceInputs={actualPriceInputs}
            schema={schema}
            loadingMap={loadingMap}
            onSummaryLimitChange={setSummaryLimit}
            onHistoryLimitChange={setHistoryLimit}
            onHistoryFilterChange={setHistoryFilter}
            onLoadSummary={() => loadSummary()}
            onLoadHistory={() => loadHistory()}
            onLoadSchema={loadSchema}
            onActualPriceInputChange={updateActualPriceInput}
            onSaveActualPrice={handleSaveActualPrice}
          />
        ) : (
          <AlgorithmInsightsSection
            selectedAlgorithm={selectedAlgorithm}
            selectedAlgorithmModel={selectedAlgorithmModel}
            selectedAlgorithmFinetunedModel={selectedAlgorithmFinetunedModel}
            trainingSamples={trainingSamples}
          />
        )}
      </main>
    </div>
  )
}

export default App