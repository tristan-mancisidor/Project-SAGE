function ReportViewer({ report }) {
  if (!report) return null

  const { response, status } = report

  // Split response into sections by numbered headers or markdown headers
  const sections = parseReportSections(response)

  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm">
      {/* Status bar */}
      <div className="border-b border-gray-100 px-6 py-3 flex items-center justify-between">
        <h2 className="font-semibold text-gray-800">Sage's Analysis</h2>
        <StatusBadge status={status} />
      </div>

      {/* Report content */}
      <div className="px-6 py-6 prose max-w-none">
        {sections.length > 1 ? (
          sections.map((section, i) => (
            <div key={i} className="mb-6 last:mb-0">
              {section.title && (
                <h3 className="text-lg font-bold text-gray-800 border-b border-gray-100 pb-2 mb-3">
                  {section.title}
                </h3>
              )}
              <div className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
                {section.content}
              </div>
            </div>
          ))
        ) : (
          <div className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
            {response}
          </div>
        )}
      </div>
    </div>
  )
}

function StatusBadge({ status }) {
  const styles = {
    'in_progress': 'bg-blue-100 text-blue-700',
    'awaiting_approval': 'bg-amber-100 text-amber-700',
    'complete': 'bg-green-100 text-green-700',
  }
  const labels = {
    'in_progress': 'In Progress',
    'awaiting_approval': 'Awaiting Approval',
    'complete': 'Complete',
  }

  return (
    <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${styles[status] || styles['in_progress']}`}>
      {labels[status] || status}
    </span>
  )
}

function parseReportSections(text) {
  if (!text) return [{ title: null, content: '' }]

  // Split on numbered section headers like "1. CLIENT SNAPSHOT" or "## Section"
  const sectionPattern = /(?:^|\n)(?:(\d+)\.\s+(.+)|##\s+(.+))\n/g
  const sections = []
  let lastIndex = 0
  let match

  while ((match = sectionPattern.exec(text)) !== null) {
    // Push content before this header
    if (match.index > lastIndex) {
      const prevContent = text.slice(lastIndex, match.index).trim()
      if (prevContent && sections.length === 0) {
        sections.push({ title: null, content: prevContent })
      } else if (prevContent && sections.length > 0) {
        sections[sections.length - 1].content = prevContent
      }
    }
    const title = match[2] || match[3]
    sections.push({ title, content: '' })
    lastIndex = match.index + match[0].length
  }

  // Remaining content
  if (lastIndex < text.length) {
    const remaining = text.slice(lastIndex).trim()
    if (sections.length > 0) {
      sections[sections.length - 1].content = remaining
    } else {
      sections.push({ title: null, content: remaining })
    }
  }

  return sections.length > 0 ? sections : [{ title: null, content: text }]
}

export default ReportViewer
