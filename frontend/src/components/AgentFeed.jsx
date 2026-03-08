function AgentFeed({ events, isLoading, compact = false }) {
  if (!events || events.length === 0) {
    if (isLoading) {
      return (
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-sage-500 rounded-full animate-pulse" />
            <span className="text-gray-600 text-sm">Sage is thinking...</span>
          </div>
        </div>
      )
    }
    return null
  }

  return (
    <div className={`bg-white border border-gray-200 rounded-xl ${compact ? 'p-4' : 'p-6'}`}>
      <div className={`agent-feed space-y-2 ${compact ? 'max-h-96' : 'max-h-[600px]'} overflow-y-auto`}>
        {events.map((event, i) => (
          <div
            key={i}
            className={`flex items-start gap-3 ${compact ? 'py-1' : 'py-2'}`}
          >
            <div className="w-2 h-2 mt-1.5 bg-sage-400 rounded-full flex-shrink-0" />
            <div>
              <span className="text-xs font-mono text-sage-600 uppercase tracking-wide">
                {event.tool}
              </span>
              <p className={`text-gray-600 ${compact ? 'text-xs' : 'text-sm'}`}>
                {event.input_summary}
              </p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-center gap-3 py-2">
            <div className="w-2 h-2 bg-sage-500 rounded-full animate-pulse" />
            <span className="text-gray-400 text-sm">Reasoning...</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default AgentFeed
