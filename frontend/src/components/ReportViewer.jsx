import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';

const SECTION_CONFIG = {
  client_snapshot:  { color: '#16a34a', border: '#16a34a', bg: '#f0fdf4', icon: '👤' },
  net_worth:        { color: '#2563eb', border: '#2563eb', bg: '#eff6ff', icon: '📊' },
  income_cashflow:  { color: '#4f46e5', border: '#4f46e5', bg: '#eef2ff', icon: '💰' },
  monte_carlo:      { color: '#d97706', border: '#d97706', bg: '#fffbeb', icon: '📈' },
  planning_gaps:    { color: '#dc2626', border: '#dc2626', bg: '#fef2f2', icon: '⚠️' },
  next_steps:       { color: '#059669', border: '#059669', bg: '#ecfdf5', icon: '✅' },
  approval:         { color: '#64748b', border: '#e2e8f0', bg: '#f8fafc', icon: '🔍' },
  full:             { color: '#374151', border: '#e5e7eb', bg: '#ffffff', icon: '📄' },
};

const SECTION_PATTERNS = [
  { id: 'client_snapshot',  keywords: ['client snapshot'] },
  { id: 'net_worth',        keywords: ['net worth'] },
  { id: 'income_cashflow',  keywords: ['income', 'cash flow', 'cashflow'] },
  { id: 'monte_carlo',      keywords: ['monte carlo'] },
  { id: 'planning_gaps',    keywords: ['planning gap', 'gap report'] },
  { id: 'next_steps',       keywords: ['next steps', 'recommended next'] },
  { id: 'approval',         keywords: ['approval request', 'would you like to approve'] },
];

function detectSectionId(headerText) {
  const lower = headerText.toLowerCase();
  for (const { id, keywords } of SECTION_PATTERNS) {
    if (keywords.some(k => lower.includes(k))) return id;
  }
  return null;
}

function parseReportSections(text) {
  if (!text) return [];
  const lines = text.split('\n');
  const sections = [];
  let current = null;

  for (const line of lines) {
    const headerMatch = line.match(/^#{1,2}\s+(.+)$/);
    if (headerMatch) {
      const title = headerMatch[1].replace(/^\d+\.\s*/, '').trim();
      const id = detectSectionId(title) || `section_${sections.length}`;
      if (current) sections.push(current);
      current = { id, title, content: '' };
    } else {
      if (!current) current = { id: 'full', title: 'Analysis', content: '' };
      current.content += line + '\n';
    }
  }
  if (current) sections.push(current);

  // If no sections detected, return single block
  if (sections.length <= 1 && sections[0]?.id === 'full') {
    return [{ id: 'full', title: 'Analysis', content: text }];
  }
  return sections;
}

function injectGapBadges(content) {
  const domainPills = [
    'Retirement & Investment Planning',
    'Tax Planning',
    'Estate Planning',
    'Risk Management & Insurance',
  ];

  let result = content;

  // Urgency/Impact badges
  result = result.replace(/\b(Urgency|Impact):\s*(High)\b/g,
    '$1: High <span class="urgency-badge high">HIGH</span>');
  result = result.replace(/\b(Urgency|Impact):\s*(Medium)\b/g,
    '$1: Medium <span class="urgency-badge medium">MEDIUM</span>');
  result = result.replace(/\b(Urgency|Impact):\s*(Low)\b/g,
    '$1: Low <span class="urgency-badge low">LOW</span>');

  // HIGH URGENCY / MEDIUM URGENCY section labels
  result = result.replace(/\bHIGH URGENCY\b/g,
    'HIGH URGENCY <span class="urgency-badge high">HIGH</span>');
  result = result.replace(/\bMEDIUM URGENCY\b/g,
    'MEDIUM URGENCY <span class="urgency-badge medium">MEDIUM</span>');
  result = result.replace(/\bLOW URGENCY\b/g,
    'LOW URGENCY <span class="urgency-badge low">LOW</span>');

  // Domain pills
  for (const domain of domainPills) {
    result = result.replace(
      new RegExp(`\\*\\*${domain}\\*\\*`, 'g'),
      `**<span class="domain-pill">${domain}</span>**`
    );
  }

  return result;
}

function SectionCard({ section }) {
  const config = SECTION_CONFIG[section.id] || SECTION_CONFIG['full'];
  const isApproval = section.id === 'approval';

  const content = section.id === 'planning_gaps'
    ? injectGapBadges(section.content)
    : section.content;

  if (isApproval) {
    return (
      <div style={{
        background: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        padding: '24px',
        marginBottom: '24px',
        color: '#475569',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <span style={{ fontSize: '1.1rem' }}>🔍</span>
          <span style={{ fontWeight: 600, color: '#334155' }}>Approval Request</span>
        </div>
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown rehypePlugins={[rehypeRaw]}>{content}</ReactMarkdown>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      background: '#ffffff',
      border: '1px solid #e5e7eb',
      borderRadius: '12px',
      marginBottom: '24px',
      overflow: 'hidden',
      boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    }}>
      {/* Card header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        padding: '14px 20px',
        borderLeft: `4px solid ${config.border}`,
        background: config.bg,
        borderBottom: '1px solid #f1f5f9',
      }}>
        <span style={{ fontSize: '1.1rem' }}>{config.icon}</span>
        <span style={{
          fontFamily: "'Playfair Display', serif",
          fontWeight: 600,
          fontSize: '1rem',
          color: config.color,
          letterSpacing: '0.01em',
        }}>
          {section.title}
        </span>
      </div>
      {/* Card body */}
      <div style={{ padding: '20px 24px' }} className="prose prose-sm max-w-none">
        <ReactMarkdown rehypePlugins={[rehypeRaw]}>{content}</ReactMarkdown>
      </div>
    </div>
  );
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

export default function ReportViewer({ report }) {
  if (!report) return null;

  const { response, status } = report;
  const sections = parseReportSections(response);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-800">Sage's Analysis</h2>
        <StatusBadge status={status} />
      </div>
      {sections.map((section, i) => (
        <SectionCard key={`${section.id}-${i}`} section={section} />
      ))}
    </div>
  );
}
