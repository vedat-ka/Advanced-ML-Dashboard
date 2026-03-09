import { useState } from "react";
import AlgorithmCard from "./components/AlgorithmCard";
import { algorithms } from "./data/algorithms";
import "./App.css";

const CATEGORIES = ["Alle", ...Array.from(new Set(algorithms.map((a) => a.category)))];

function App() {
  const [selectedCategory, setSelectedCategory] = useState("Alle");
  const [searchQuery, setSearchQuery] = useState("");

  const filtered = algorithms.filter((alg) => {
    const matchesCategory =
      selectedCategory === "Alle" || alg.category === selectedCategory;
    const query = searchQuery.toLowerCase();
    const matchesSearch =
      query === "" ||
      alg.name.toLowerCase().includes(query) ||
      alg.useCase.toLowerCase().includes(query) ||
      alg.category.toLowerCase().includes(query);
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">Advanced ML Dashboard</h1>
        <p className="app__subtitle">
          Vorhersagen, Verlauf und algorithmusspezifisches Training
        </p>
      </header>

      <main className="app__main">
        <div className="app__controls">
          <input
            type="search"
            placeholder="Algorithmus suchen…"
            className="app__search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Algorithmus suchen"
          />
          <nav className="app__categories" aria-label="Kategoriefilter">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                className={`app__category-btn${selectedCategory === cat ? " app__category-btn--active" : ""}`}
                onClick={() => setSelectedCategory(cat)}
                aria-pressed={selectedCategory === cat}
              >
                {cat}
              </button>
            ))}
          </nav>
        </div>

        {filtered.length === 0 ? (
          <p className="app__empty">Keine Algorithmen gefunden.</p>
        ) : (
          <div className="app__grid">
            {filtered.map((alg) => (
              <AlgorithmCard key={alg.id} algorithm={alg} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
