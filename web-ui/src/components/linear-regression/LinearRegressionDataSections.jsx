import SummaryItem from '../common/SummaryItem'
import { formatNumber, formatTimestamp } from '../common/formatters'

function LinearRegressionDataSections({
  summary,
  summaryLimit,
  historyLimit,
  historyFilter,
  filteredHistory,
  actualPriceInputs,
  schema,
  loadingMap,
  onSummaryLimitChange,
  onHistoryLimitChange,
  onHistoryFilterChange,
  onLoadSummary,
  onLoadHistory,
  onLoadSchema,
  onActualPriceInputChange,
  onSaveActualPrice,
}) {
  return (
    <>
      <section className="card">
        <div className="section-heading inline-controls">
          <div>
            <p className="eyebrow">Reporting</p>
            <h2>Zusammenfassung</h2>
          </div>
          <div className="control-group">
            <input type="number" min="1" max="1000" value={summaryLimit} onChange={(event) => onSummaryLimitChange(event.target.value)} />
            <button type="button" className="secondary-button" onClick={onLoadSummary}>
              Aktualisieren
            </button>
          </div>
        </div>

        {summary ? (
          <dl className="summary-grid">
            <SummaryItem label="Min. Flaeche" value={formatNumber(summary.min_area)} />
            <SummaryItem label="Max. Flaeche" value={formatNumber(summary.max_area)} />
            <SummaryItem label="Durchschnitt Flaeche" value={formatNumber(summary.avg_area)} />
            <SummaryItem label="Min. Prognosepreis" value={formatNumber(summary.min_predicted_price)} />
            <SummaryItem label="Max. Prognosepreis" value={formatNumber(summary.max_predicted_price)} />
            <SummaryItem label="Zeilen mit Marktpreis" value={formatNumber(summary.actual_price_count)} />
            <SummaryItem label="Durchschnitt Marktpreis" value={formatNumber(summary.avg_actual_price)} />
            <SummaryItem label="Durchschn. absolute Abweichung" value={formatNumber(summary.avg_absolute_error)} />
            <SummaryItem label="Erste Speicherung" value={formatTimestamp(summary.first_prediction_at)} />
            <SummaryItem label="Letzte Speicherung" value={formatTimestamp(summary.last_prediction_at)} />
          </dl>
        ) : (
          <p className="muted-copy">Zusammenfassung wird geladen.</p>
        )}
      </section>

      <section className="card wide-card">
        <div className="section-heading inline-controls">
          <div>
            <p className="eyebrow">Verlauf</p>
            <h2>SQLite-Vorhersageeintraege des Preis-Workflows</h2>
          </div>
          <div className="toolbar">
            <input type="number" min="1" max="500" value={historyLimit} onChange={(event) => onHistoryLimitChange(event.target.value)} />
            <input type="search" value={historyFilter} placeholder="Zeilen filtern" onChange={(event) => onHistoryFilterChange(event.target.value)} />
            <button type="button" className="secondary-button" onClick={onLoadHistory}>
              Aktualisieren
            </button>
          </div>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Flaeche</th>
                <th>Vorhergesagter Preis</th>
                <th>Marktpreis</th>
                <th>Modellquelle</th>
                <th>Erstellt</th>
                <th>Aktion</th>
              </tr>
            </thead>
            <tbody>
              {filteredHistory.length > 0 ? (
                filteredHistory.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{formatNumber(item.area)}</td>
                    <td>{formatNumber(item.predicted_price)}</td>
                    <td>
                      <div className="inline-price-editor">
                        <input
                          type="number"
                          min="1"
                          step="0.01"
                          value={actualPriceInputs[item.id] ?? ''}
                          placeholder="z. B. 485000"
                          onChange={(event) => onActualPriceInputChange(item.id, event.target.value)}
                        />
                        <span className="price-hint">
                          Aktuell: {item.actual_price === null ? '-' : formatNumber(item.actual_price)}
                        </span>
                      </div>
                    </td>
                    <td>
                      <span className={`tag ${item.model_source}`}>{item.model_source}</span>
                    </td>
                    <td>{formatTimestamp(item.created_at)}</td>
                    <td>
                      <button
                        type="button"
                        className="secondary-button table-button"
                        onClick={() => onSaveActualPrice(item.id)}
                        disabled={loadingMap[`actual-price-${item.id}`]}
                      >
                        {loadingMap[`actual-price-${item.id}`] ? 'Speichere...' : 'Marktpreis speichern'}
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="empty-state">
                    Keine Zeilen passen zum aktuellen Filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card wide-card">
        <div className="section-heading inline-controls">
          <div>
            <p className="eyebrow">Datenbank</p>
            <h2>SQLite-Schema</h2>
          </div>
          <button type="button" className="secondary-button" onClick={onLoadSchema}>
            Schema aktualisieren
          </button>
        </div>

        <div className="schema-grid">
          {schema.map((item) => (
            <article key={`${item.name}-${item.type}`} className="schema-card">
              <span className="schema-type">{item.type}</span>
              <h3>{item.name}</h3>
              <pre>{item.sql}</pre>
            </article>
          ))}
        </div>
      </section>
    </>
  )
}

export default LinearRegressionDataSections