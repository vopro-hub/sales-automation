export default function SimpleTable({ columns, rows }) {
  return (
    <table border="1" cellPadding="10">
      <thead>
        <tr>
          {columns.map(c => (
            <th key={c}>{c}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={i}>
            {r.map((cell, j) => (
              <td key={j}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
