import { useState } from 'react'

function ApprovalPanel({ status, onApproval, isLoading }) {
  const [feedback, setFeedback] = useState('')
  const [selectedSection, setSelectedSection] = useState('')

  if (status === 'complete') {
    return (
      <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
        <p className="text-green-800 font-semibold">Plan Finalized</p>
        <p className="text-green-600 text-sm mt-1">
          All sections approved. The plan is ready for presentation.
        </p>
      </div>
    )
  }

  const handleApprove = () => {
    onApproval('approve', selectedSection || null, null)
    setFeedback('')
    setSelectedSection('')
  }

  const handleModify = () => {
    if (!feedback.trim()) return
    onApproval('modify', selectedSection || null, feedback)
    setFeedback('')
    setSelectedSection('')
  }

  const handleRedirect = () => {
    if (!feedback.trim()) return
    onApproval('redirect', null, feedback)
    setFeedback('')
    setSelectedSection('')
  }

  const sections = [
    'Client Snapshot',
    'Net Worth Analysis',
    'Income & Cash Flow',
    'Monte Carlo Projection',
    'Planning Gap Report',
    'Recommended Next Steps',
  ]

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      <h3 className="font-semibold text-gray-800 mb-4">Advisor Review</h3>

      {/* Section selector */}
      <div className="mb-4">
        <label className="text-sm text-gray-500 mb-1 block">Section (optional)</label>
        <select
          value={selectedSection}
          onChange={(e) => setSelectedSection(e.target.value)}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sage-500"
        >
          <option value="">All sections</option>
          {sections.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Feedback input */}
      <div className="mb-4">
        <label className="text-sm text-gray-500 mb-1 block">
          Feedback (required for modify/redirect)
        </label>
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="e.g., Adjust Monte Carlo to use 5.5% return assumption..."
          rows={3}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sage-500 resize-none"
        />
      </div>

      {/* Action buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleApprove}
          disabled={isLoading}
          className="flex-1 bg-sage-600 hover:bg-sage-700 disabled:bg-gray-300 text-white font-medium py-2.5 px-4 rounded-lg transition-colors text-sm"
        >
          {isLoading ? 'Processing...' : 'Approve'}
        </button>
        <button
          onClick={handleModify}
          disabled={isLoading || !feedback.trim()}
          className="flex-1 bg-amber-500 hover:bg-amber-600 disabled:bg-gray-300 text-white font-medium py-2.5 px-4 rounded-lg transition-colors text-sm"
        >
          Modify
        </button>
        <button
          onClick={handleRedirect}
          disabled={isLoading || !feedback.trim()}
          className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-300 text-white font-medium py-2.5 px-4 rounded-lg transition-colors text-sm"
        >
          Redirect
        </button>
      </div>
    </div>
  )
}

export default ApprovalPanel
