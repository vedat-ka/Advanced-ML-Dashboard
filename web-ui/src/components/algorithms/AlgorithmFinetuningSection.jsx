import FieldInput from '../common/FieldInput'
import ResultCard from '../common/ResultCard'
import { formatTimestamp } from '../common/formatters'

function AlgorithmFinetuningSection({
  selectedAlgorithm,
  finetuningSampleDraft,
  finetuningSampleNote,
  finetuningSamples,
  customFinetuneLimit,
  loadingMap,
  onFinetuningSampleDraftChange,
  onFinetuningSampleNoteChange,
  onSaveFinetuningSample,
  onDeleteFinetuningSample,
  onCustomFinetuneLimitChange,
  onFinetune,
  customFinetuneResult,
}) {
  return (
    <section className="card wide-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Reales Finetuning</p>
          <h2>Vergleichsdaten erfassen und daraus {selectedAlgorithm.label} finetunen</h2>
        </div>
      </div>

      <div className="forms-grid">
        <form className="tool-form" onSubmit={onSaveFinetuningSample}>
          <h3>Reales Finetuning-Sample speichern</h3>
          {selectedAlgorithm.training_fields.map((field) => (
            <label key={`finetune-sample-${field.name}`}>
              {field.label}
              <FieldInput
                field={field}
                value={finetuningSampleDraft[field.name] ?? ''}
                onChange={(value) => onFinetuningSampleDraftChange(field.name, value)}
              />
            </label>
          ))}
          <label>
            Notiz
            <textarea
              rows="3"
              value={finetuningSampleNote}
              placeholder="z. B. echter Freigabefall, validiertes Gehalt, manuell gepruefte Spam-Klassifikation"
              onChange={(event) => onFinetuningSampleNoteChange(event.target.value)}
            />
          </label>
          <button type="submit" disabled={loadingMap['save-finetuning-sample']}>
            {loadingMap['save-finetuning-sample'] ? 'Speichere...' : 'Finetuning-Sample speichern'}
          </button>
        </form>

        <div className="tool-form">
          <h3>Gespeicherte Realdaten in SQLite</h3>
          <p className="muted-copy">
            Diese Datensaetze werden beim Finetuning als echte Vergleichswerte verwendet, nicht die alten Original-Trainingsruns.
          </p>
          <div className="finetuning-sample-list">
            {finetuningSamples.length > 0 ? (
              finetuningSamples.map((item) => (
                <article key={`stored-finetune-${item.id}`} className="finetuning-sample-card">
                  <pre>{JSON.stringify(item.sample, null, 2)}</pre>
                  <p className="price-hint">{item.note || 'Ohne Notiz'}</p>
                  <p className="price-hint">{formatTimestamp(item.created_at)}</p>
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => onDeleteFinetuningSample(item.id)}
                    disabled={loadingMap[`delete-finetuning-sample-${item.id}`]}
                  >
                    {loadingMap[`delete-finetuning-sample-${item.id}`] ? 'Loesche...' : 'Sample loeschen'}
                  </button>
                </article>
              ))
            ) : (
              <p className="muted-copy">Noch keine realen Finetuning-Samples gespeichert.</p>
            )}
          </div>
        </div>

        <form className="tool-form" onSubmit={onFinetune}>
          <h3>Aus realen Samples finetunen</h3>
          <label>
            Optionales Sample-Limit
            <input
              type="number"
              min="1"
              step="1"
              value={customFinetuneLimit}
              placeholder="Alle gespeicherten Finetuning-Samples verwenden"
              onChange={(event) => onCustomFinetuneLimitChange(event.target.value)}
            />
          </label>
          <p className="muted-copy">
            Verfuegbar in SQLite: {finetuningSamples.length} Samples.
          </p>
          <button type="submit" disabled={loadingMap['custom-finetune'] || finetuningSamples.length === 0}>
            {loadingMap['custom-finetune'] ? 'Trainiere...' : 'Finetuning starten'}
          </button>
          {customFinetuneResult && <ResultCard title="Finetuning-Ergebnis" data={customFinetuneResult} />}
        </form>
      </div>
    </section>
  )
}

export default AlgorithmFinetuningSection