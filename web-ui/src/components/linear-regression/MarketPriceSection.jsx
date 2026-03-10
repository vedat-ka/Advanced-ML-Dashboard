import { formatNumber } from '../common/formatters'

function MarketPriceSection({
  latestMarketPriceRows,
  summary,
  actualPriceInputs,
  onActualPriceInputChange,
  onSaveActualPrice,
  loadingMap,
}) {
  return (
    <section className="card wide-card market-price-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Marktpreise erfassen</p>
          <h2>Hier hinterlegst du die echten Vergleichspreise fuer das Finetuning</h2>
          <p className="muted-copy">
            Ablauf: zuerst eine Vorhersage speichern, danach unten den echten Marktpreis eintragen und speichern.
            Das Finetuning startet sinnvoll erst ab 5 validierten Zeilen.
          </p>
        </div>
        <div className="market-price-status">
          <strong>{formatNumber(summary?.actual_price_count)} / 5</strong>
          <span>Zeilen mit echtem Marktpreis</span>
        </div>
      </div>

      {latestMarketPriceRows.length > 0 ? (
        <div className="market-price-grid">
          {latestMarketPriceRows.map((item) => (
            <article key={`market-price-${item.id}`} className="market-price-row-card">
              <div className="market-price-meta">
                <strong>ID {item.id}</strong>
                <span>{formatNumber(item.area)} qm</span>
                <span>Prognose: {formatNumber(item.predicted_price)}</span>
              </div>
              <label>
                Echter Marktpreis
                <input
                  type="number"
                  min="1"
                  step="0.01"
                  value={actualPriceInputs[item.id] ?? ''}
                  placeholder="z. B. 485000"
                  onChange={(event) => onActualPriceInputChange(item.id, event.target.value)}
                />
              </label>
              <div className="market-price-actions">
                <span className="price-hint">
                  Aktuell: {item.actual_price === null ? '-' : formatNumber(item.actual_price)}
                </span>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => onSaveActualPrice(item.id)}
                  disabled={loadingMap[`actual-price-${item.id}`]}
                >
                  {loadingMap[`actual-price-${item.id}`] ? 'Speichere...' : 'Marktpreis speichern'}
                </button>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <p className="muted-copy">
          Es gibt noch keine gespeicherten Vorhersagen. Erstelle zuerst ueber das Originalmodell mindestens eine Preisvorhersage.
        </p>
      )}
    </section>
  )
}

export default MarketPriceSection