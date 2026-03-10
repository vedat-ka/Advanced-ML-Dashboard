function ResultCard({ title, data }) {
  return (
    <div className="result-card">
      <h4>{title}</h4>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

export default ResultCard