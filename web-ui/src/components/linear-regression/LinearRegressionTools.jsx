import ResultCard from '../common/ResultCard'

function LinearRegressionTools({
  predictForm,
  finetunedForm,
  compareForm,
  onPredictAreaChange,
  onFinetunedAreaChange,
  onCompareAreaChange,
  onPredict,
  onFinetunedPredict,
  onCompare,
  predictResult,
  finetunedResult,
  compareResult,
  loadingMap,
}) {
  return (
    <section className="card wide-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Vorhersage-Werkzeuge</p>
          <h2>Bestehende Preisvorhersage-Endpunkte nur fuer die lineare Regression</h2>
        </div>
      </div>

      <div className="forms-grid">
        <form className="tool-form" onSubmit={onPredict}>
          <h3>Originalmodell</h3>
          <label>
            Flaeche in qm
            <input
              type="number"
              min="1"
              step="0.1"
              value={predictForm.area}
              onChange={(event) => onPredictAreaChange(event.target.value)}
            />
          </label>
          <button type="submit" disabled={loadingMap.predict}>
            {loadingMap.predict ? 'Berechne...' : 'Vorhersage speichern'}
          </button>
          {predictResult && <ResultCard title="Letzte Vorhersage Originalmodell" data={predictResult} />}
        </form>

        <form className="tool-form" onSubmit={onFinetunedPredict}>
          <h3>Finetuntes Modell</h3>
          <label>
            Flaeche in qm
            <input
              type="number"
              min="1"
              step="0.1"
              value={finetunedForm.area}
              onChange={(event) => onFinetunedAreaChange(event.target.value)}
            />
          </label>
          <button type="submit" disabled={loadingMap['predict-finetuned']}>
            {loadingMap['predict-finetuned'] ? 'Berechne...' : 'Mit finetuntem Modell vorhersagen'}
          </button>
          {finetunedResult && <ResultCard title="Letzte Vorhersage finetuntes Modell" data={finetunedResult} />}
        </form>

        <form className="tool-form" onSubmit={onCompare}>
          <h3>Modellvergleich</h3>
          <label>
            Flaeche in qm
            <input
              type="number"
              min="1"
              step="0.1"
              value={compareForm.area}
              onChange={(event) => onCompareAreaChange(event.target.value)}
            />
          </label>
          <button type="submit" disabled={loadingMap.compare}>
            {loadingMap.compare ? 'Vergleiche...' : 'Modelle vergleichen'}
          </button>
          {compareResult && <ResultCard title="Ergebnis Modellvergleich" data={compareResult} />}
        </form>
      </div>
    </section>
  )
}

export default LinearRegressionTools