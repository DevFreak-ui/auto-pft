export function shortenReportId(id: string): string {
  if (id.length <= 8) return id;
  return id.slice(0, 5) + '...' + id.slice(-3);
}
