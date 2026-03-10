import ResultCard from '../common/ResultCard'

function LinearRegressionFinetuneSection({ finetuneLimit, loadingMap, finetuneResult, onFinetuneLimitChange, onFinetune }) {
  return (
    <section className="card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">SQLite-Finetuning</p>
          <h2>LinearRegression ueber echte Vergleichspreise nachtrainieren</h2>
        </div>
      </div>

      <form className="tool-form compact-form" onSubmit={onFinetune}>
        <label>
          Optionales Zeilenlimit
          <input
            type="number"
            min="1"
            step="1"
            value={finetuneLimit}
            placeholder="Alle Zeilen mit actual_price verwenden"
            onChange={(event) => onFinetuneLimitChange(event.target.value)}
          />
        </label>
        <button type="submit" disabled={loadingMap.finetune}>
          {loadingMap.finetune ? 'Trainiere...' : 'Finetuning starten'}
        </button>
      </form>

      {finetuneResult ? (
        <ResultCard title="Finetuning-Ergebnis" data={finetuneResult} />
      ) : (
        <p className="muted-copy">
          Fuer das Finetuning werden nur Datensaetze verwendet, fuer die bereits ein echter Marktpreis hinterlegt wurde.
        </p>
      )}
    </section>
  )
}

export default LinearRegressionFinetuneSection