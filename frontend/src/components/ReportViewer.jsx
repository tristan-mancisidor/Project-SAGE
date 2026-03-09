import ReactMarkdown from 'react-markdown'

function ReportViewer({ report }) {
  if (!report) return null

  const { response, status } = report

  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm">
      {/* Status bar */}
      <div className="border-b border-gray-100 px-6 py-3 flex items-center justify-between">
        <h2 className="font-semibold text-gray-800">Sage's Analysis</h2>
        <StatusBadge status={status} />
      </div>

      {/* Report content */}
      <div className="px-6 py-6 prose prose-sm max-w-none
        prose-headings:text-gray-800 prose-headings:font-bold
        prose-h1:text-2xl prose-h1:border-b prose-h1:border-gray-200 prose-h1:pb-2 prose-h1:mb-4
        prose-h2:text-xl prose-h2:mt-8 prose-h2:mb-3
        prose-h3:text-lg prose-h3:mt-6 prose-h3:mb-2
        prose-p:text-gray-700 prose-p:leading-relaxed
        prose-strong:text-gray-800
        prose-li:text-gray-700
        prose-hr:my-6 prose-hr:border-gray-200
        prose-ul:my-2 prose-ol:my-2
      ">
        <ReactMarkdown>{response || ''}</ReactMarkdown>
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

export default ReportViewer
