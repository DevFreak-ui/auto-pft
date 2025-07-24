export function shortenReportId(id: string): string {
  if (id.length <= 8) return id;
  return id.slice(0, 5) + '...' + id.slice(-3);
}

// Convert Date to Day, MON, Year format
export function formatReportDate(dateString: string): string {
  const date = new Date(dateString);
  const day = date.getDate();
  const month = date.getMonth();
  const year = date.getFullYear();
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const suffix = day % 10 === 1 && day !== 11 ? 'st' : day % 10 === 2 && day !== 12 ? 'nd' : day % 10 === 3 && day !== 13 ? 'rd' : 'th';
  return `${day}${suffix} ${months[month]}, ${year}`;
}