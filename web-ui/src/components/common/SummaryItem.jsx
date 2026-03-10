function SummaryItem({ label, value }) {
  return (
    <div className="summary-item">
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  )
}

export default SummaryItem