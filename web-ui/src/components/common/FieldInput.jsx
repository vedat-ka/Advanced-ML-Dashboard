function FieldInput({ field, value, onChange, isHyperparameter = false }) {
  const type = isHyperparameter ? field.parameter_type : field.input_type

  if (type === 'select' || type === 'bool') {
    const options = type === 'bool'
      ? [
          { label: 'Ja', value: 'true' },
          { label: 'Nein', value: 'false' },
        ]
      : (field.options ?? []).map((option) => ({ label: option, value: option }))

    return (
      <select value={String(value ?? '')} onChange={(event) => onChange(event.target.value)}>
        {field.nullable && <option value="">Leer</option>}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    )
  }

  if (type === 'number' || type === 'int' || type === 'float') {
    return (
      <input
        type="number"
        min={field.min_value ?? field.minimum ?? undefined}
        max={field.maximum ?? undefined}
        step={field.step ?? '0.1'}
        value={value ?? ''}
        placeholder={field.nullable ? 'Leer fuer Standard' : ''}
        onChange={(event) => onChange(event.target.value)}
      />
    )
  }

  if (type === 'textarea') {
    return (
      <textarea
        rows={field.rows ?? 5}
        value={value ?? ''}
        placeholder={field.description ?? ''}
        onChange={(event) => onChange(event.target.value)}
      />
    )
  }

  return <input type="text" value={value ?? ''} onChange={(event) => onChange(event.target.value)} />
}

export default FieldInput