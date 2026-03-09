# Advanced ML Dashboard

Advanced ML Dashboard für Vorhersagen, Verlauf und algorithmusspezifisches Training.

## Features

- 🎯 **Einsatzzweck je Algorithmus** – Jede Algorithmuskarte zeigt den besten Anwendungsfall mit konkreten Beispielen.
- ⚙️ **Algorithmusspezifische Trainingsfelder** – Klappbare Trainingsparameter, die individuell auf jeden Algorithmus zugeschnitten sind.
- 💾 **Gespeicherte Modelldatei** – Jeder Algorithmus hat seine eigene Modelldatei (`.pkl`).
- 🔍 **Suche & Kategoriefilter** – Algorithmen nach Name oder Kategorie filtern.

## Algorithms

| Algorithm | Category | Model File |
|---|---|---|
| Lineare Regression | Regression | `linear_regression_model.pkl` |
| Random Forest | Ensemble | `random_forest_model.pkl` |
| Support Vector Machine (SVM) | Klassifikation | `svm_model.pkl` |
| Entscheidungsbaum | Klassifikation | `decision_tree_model.pkl` |
| K-Means Clustering | Clustering | `kmeans_model.pkl` |
| Neuronales Netzwerk (MLP) | Deep Learning | `neural_network_model.pkl` |

## Setup

```bash
npm install
npm run dev
```

The app runs at `http://localhost:5173/`.

## Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start development server |
| `npm run build` | Production build |
| `npm run lint` | Run ESLint |
| `npm test` | Run Vitest unit tests |

## Tech Stack

- [React 19](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vite.dev/) for bundling
- [Vitest](https://vitest.dev/) + [React Testing Library](https://testing-library.com/) for tests

![Advanced ML Dashboard](https://github.com/user-attachments/assets/75481351-4d26-4394-9ee2-ec1174baf639)
