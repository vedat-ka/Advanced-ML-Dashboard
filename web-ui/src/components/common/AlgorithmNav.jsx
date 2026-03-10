function AlgorithmNav({ algorithms, selectedAlgorithmKey, onSelectAlgorithm }) {
  return (
    <section className="algorithm-nav card wide-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Algorithmus-Navigation</p>
          <h2>Zwischen Modellen umschalten und ihren Einsatzzweck vergleichen</h2>
        </div>
      </div>

      <div className="algorithm-tab-row">
        {algorithms.map((algorithm) => (
          <button
            key={algorithm.algorithm_key}
            type="button"
            className={`algorithm-tab ${selectedAlgorithmKey === algorithm.algorithm_key ? 'active' : ''}`}
            onClick={() => onSelectAlgorithm(algorithm.algorithm_key)}
          >
            <span>{algorithm.label}</span>
            <strong>{algorithm.scenario_name}</strong>
            <small>{algorithm.task_type}</small>
          </button>
        ))}
      </div>
    </section>
  )
}

export default AlgorithmNav