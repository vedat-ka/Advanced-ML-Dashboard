import { formatNumber } from './formatters'

function StatsSection({ selectedAlgorithmKey, summary, selectedAlgorithm, selectedAlgorithmModel }) {
  if (selectedAlgorithmKey === 'linear_regression') {
    return (
      <section className="stats-grid">
        <article className="stat-card accent-sand">
          <span>Vorhersagen gesamt</span>
          <strong>{formatNumber(summary?.total_predictions)}</strong>
        </article>
        <article className="stat-card accent-ice">
          <span>Zeilen Originalmodell</span>
          <strong>{formatNumber(summary?.original_prediction_count)}</strong>
        </article>
        <article className="stat-card accent-coral">
          <span>Zeilen mit Marktpreis</span>
          <strong>{formatNumber(summary?.actual_price_count)}</strong>
        </article>
        <article className="stat-card accent-mint">
          <span>Durchschn. absolute Abweichung</span>
          <strong>{formatNumber(summary?.avg_absolute_error)}</strong>
        </article>
      </section>
    )
  }

  return (
    <section className="stats-grid">
      <article className="stat-card accent-sand">
        <span>Szenario</span>
        <strong>{selectedAlgorithm?.scenario_name ?? '-'}</strong>
      </article>
      <article className="stat-card accent-ice">
        <span>Task-Typ</span>
        <strong>{selectedAlgorithm?.task_type ?? '-'}</strong>
      </article>
      <article className="stat-card accent-coral">
        <span>Trainingsfelder</span>
        <strong>{selectedAlgorithm?.training_fields?.length ?? 0}</strong>
      </article>
      <article className="stat-card accent-mint">
        <span>Letztes Modell-Samplecount</span>
        <strong>{formatNumber(selectedAlgorithmModel?.sample_count)}</strong>
      </article>
    </section>
  )
}

export default StatsSection