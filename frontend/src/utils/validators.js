export function validateDocumentFile(file) {
  const allowed = ['.pdf', '.txt', '.md', '.doc', '.docx'];
  const name = file.name.toLowerCase();
  const validExt = allowed.some((ext) => name.endsWith(ext));
  if (!validExt) {
    return { valid: false, error: 'Please upload a PDF, TXT, or markdown document.' };
  }
  if (file.size > 10 * 1024 * 1024) {
    return { valid: false, error: 'File size exceeds 10MB limit.' };
  }
  return { valid: true };
}