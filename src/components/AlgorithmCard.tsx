import { useState } from "react";
import type { Algorithm } from "../data/algorithms";
import "./AlgorithmCard.css";

interface AlgorithmCardProps {
  algorithm: Algorithm;
}

function AlgorithmCard({ algorithm }: AlgorithmCardProps) {
  const [expanded, setExpanded] = useState(false);

  const categoryColors: Record<string, string> = {
    Regression: "category--regression",
    Ensemble: "category--ensemble",
    Klassifikation: "category--classification",
    Clustering: "category--clustering",
    "Deep Learning": "category--deep-learning",
  };

  const categoryClass =
    categoryColors[algorithm.category] ?? "category--default";

  return (
    <div className="algorithm-card" data-testid={`algorithm-card-${algorithm.id}`}>
      <div className="algorithm-card__header">
        <div className="algorithm-card__title-row">
          <h2 className="algorithm-card__name">{algorithm.name}</h2>
          <span className={`algorithm-card__category ${categoryClass}`}>
            {algorithm.category}
          </span>
        </div>

        <section className="algorithm-card__use-case" aria-label="Einsatzzweck">
          <h3 className="algorithm-card__section-title">
            <span className="algorithm-card__icon" aria-hidden="true">🎯</span>
            Bester Einsatzzweck
          </h3>
          <p className="algorithm-card__use-case-summary">{algorithm.useCase}</p>
          <ul className="algorithm-card__use-case-details">
            {algorithm.useCaseDetails.map((detail, index) => (
              <li key={index}>{detail}</li>
            ))}
          </ul>
        </section>

        <section className="algorithm-card__model-file" aria-label="Modelldatei">
          <h3 className="algorithm-card__section-title">
            <span className="algorithm-card__icon" aria-hidden="true">💾</span>
            Gespeicherte Modelldatei
          </h3>
          <code className="algorithm-card__model-filename">
            {algorithm.modelFile}
          </code>
        </section>
      </div>

      <div className="algorithm-card__training-section">
        <button
          className="algorithm-card__toggle-btn"
          onClick={() => setExpanded(!expanded)}
          aria-expanded={expanded}
          aria-controls={`training-fields-${algorithm.id}`}
        >
          <span className="algorithm-card__icon" aria-hidden="true">⚙️</span>
          Trainingsfelder
          <span className="algorithm-card__toggle-icon">
            {expanded ? "▲" : "▼"}
          </span>
        </button>

        {expanded && (
          <div
            id={`training-fields-${algorithm.id}`}
            className="algorithm-card__training-fields"
            data-testid={`training-fields-${algorithm.id}`}
          >
            {algorithm.trainingFields.map((field) => (
              <div key={field.name} className="training-field">
                <label
                  htmlFor={`${algorithm.id}-${field.name}`}
                  className="training-field__label"
                >
                  {field.label}
                </label>
                {field.type === "select" ? (
                  <select
                    id={`${algorithm.id}-${field.name}`}
                    className="training-field__input"
                    defaultValue={field.defaultValue}
                  >
                    {field.options?.map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    id={`${algorithm.id}-${field.name}`}
                    type={field.type}
                    className="training-field__input"
                    defaultValue={field.defaultValue}
                    step={field.type === "number" ? "any" : undefined}
                  />
                )}
                <p className="training-field__description">{field.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AlgorithmCard;
