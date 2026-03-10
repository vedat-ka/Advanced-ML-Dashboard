function HeroHeader({ apiBaseUrl, statusMessage, onRefresh, isLoading }) {
  return (
    <header className="hero">
      <div>
        <p className="eyebrow">FastAPI + React Steuerzentrale</p>
        <h1>Advanced-ML-Dashboard fuer Vorhersagen, Verlauf und algorithmusspezifisches Training.</h1>
        <p className="hero-copy">
          Diese Oberflaeche verbindet klassische Preisvorhersage mit einer umschaltbaren
          Modellnavigation. Jeder Algorithmus zeigt seinen besten Einsatzzweck, seine eigenen
          Trainingsfelder und seine eigene gespeicherte Modelldatei.
        </p>
      </div>

      <div className="hero-panel">
        <span className="panel-label">API-Basis-URL</span>
        <strong>{apiBaseUrl}</strong>
        <span className="panel-label">Service-Status</span>
        <strong>{statusMessage}</strong>
        <button className="secondary-button" type="button" onClick={onRefresh} disabled={isLoading}>
          {isLoading ? 'Aktualisiere...' : 'Status aktualisieren'}
        </button>
      </div>
    </header>
  )
}

export default HeroHeader