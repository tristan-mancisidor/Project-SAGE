import { useState } from 'react'
import UploadZone from './components/UploadZone'
import AgentFeed from './components/AgentFeed'
import ReportViewer from './components/ReportViewer'
import ApprovalPanel from './components/ApprovalPanel'

const API_BASE = import.meta.env.VITE_API_URL || ''

function App() {
  const [stage, setStage] = useState('upload') // upload | analyzing | report
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [agentEvents, setAgentEvents] = useState([])
  const [report, setReport] = useState(null)
  const [conversationHistory, setConversationHistory] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [error, setError] = useState(null)

  const handleFilesUploaded = (files) => {
    setUploadedFiles(files)
  }

  const handleStartAnalysis = async (demoMode = true) => {
    setStage('analyzing')
    setIsLoading(true)
    setIsConnecting(true)
    setError(null)
    setAgentEvents([])

    try {
      const fileIds = uploadedFiles.map(f => f.file_id)
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 120000)

      const response = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_ids: fileIds,
          demo_mode: demoMode,
          conversation_history: [],
        }),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)
      setIsConnecting(false)

      if (!response.ok) throw new Error(`Analysis failed: ${response.statusText}`)

      const text = await response.text()
      if (!text) throw new Error('SAGE is warming up — please try again in a moment.')
      let data
      try {
        data = JSON.parse(text)
      } catch {
        throw new Error('SAGE is warming up — please try again in a moment.')
      }
      setAgentEvents(data.tool_calls || [])
      setConversationHistory(data.conversation_history || [])
      setReport({
        response: data.response,
        status: data.status,
      })
      setStage('report')
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('SAGE is warming up — please try again in a moment.')
      } else {
        setError(err.message)
      }
      setStage('upload')
    } finally {
      setIsLoading(false)
      setIsConnecting(false)
    }
  }

  const handleApproval = async (action, section, feedback) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action,
          section,
          feedback,
          conversation_history: conversationHistory,
        }),
      })

      if (!response.ok) throw new Error(`Approval failed: ${response.statusText}`)

      const data = await response.json()
      setAgentEvents(prev => [...prev, ...(data.tool_calls || [])])
      setConversationHistory(data.conversation_history || [])
      setReport({
        response: data.response,
        status: data.status,
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setStage('upload')
    setUploadedFiles([])
    setAgentEvents([])
    setReport(null)
    setConversationHistory([])
    setError(null)
    setIsConnecting(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-sage-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">SAGE</h1>
            <p className="text-sage-200 text-sm">Senior AI Guidance Engine</p>
          </div>
          {stage !== 'upload' && (
            <button
              onClick={handleReset}
              className="text-sage-200 hover:text-white text-sm underline"
            >
              New Analysis
            </button>
          )}
        </div>
      </header>

      {/* Error banner */}
      {error && (
        <div className="max-w-7xl mx-auto px-6 mt-4">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        </div>
      )}

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Upload Stage */}
        {stage === 'upload' && (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">
                Financial Plan Analysis
              </h2>
              <p className="text-gray-500">
                Upload client documents or run the demo with hypothetical data
              </p>
            </div>

            <UploadZone onFilesUploaded={handleFilesUploaded} uploadedFiles={uploadedFiles} />

            <div className="mt-8 flex flex-col gap-3">
              <button
                onClick={() => handleStartAnalysis(true)}
                className="w-full bg-sage-600 hover:bg-sage-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Run Demo Analysis (James & Sarah Chen)
              </button>
              {uploadedFiles.length > 0 && (
                <button
                  onClick={() => handleStartAnalysis(false)}
                  className="w-full bg-gray-700 hover:bg-gray-800 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                >
                  Analyze Uploaded Documents ({uploadedFiles.length} files)
                </button>
              )}
            </div>
          </div>
        )}

        {/* Analyzing Stage */}
        {stage === 'analyzing' && (
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {isConnecting ? 'Connecting to SAGE...' : 'Sage is analyzing...'}
              </h2>
              <p className="text-gray-500">
                {isConnecting
                  ? 'This may take up to 60 seconds on first load...'
                  : 'Reasoning through client data step by step'
                }
              </p>
              {isConnecting && (
                <div className="mt-6 flex justify-center">
                  <div className="w-8 h-8 border-4 border-sage-200 border-t-sage-600 rounded-full animate-spin" />
                </div>
              )}
            </div>
            {!isConnecting && <AgentFeed events={agentEvents} isLoading={isLoading} />}
          </div>
        )}

        {/* Report Stage */}
        {stage === 'report' && report && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Agent Feed sidebar */}
            <div className="lg:col-span-1 order-2 lg:order-1">
              <div className="sticky top-8">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                  Reasoning Trail
                </h3>
                <AgentFeed events={agentEvents} isLoading={isLoading} compact />
              </div>
            </div>

            {/* Report + Approval */}
            <div className="lg:col-span-2 order-1 lg:order-2">
              <ReportViewer report={report} />
              <div className="mt-6">
                <ApprovalPanel
                  status={report.status}
                  onApproval={handleApproval}
                  isLoading={isLoading}
                />
              </div>
            </div>
          </div>
        )}
      </main>

    </div>
  )
}

export default App
