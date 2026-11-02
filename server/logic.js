// Demo mode is intentionally conservative: it never infers structured facts.
export function extractDraft(text) { return { task: text, location: '', timing: '', compensation: '' }; }
