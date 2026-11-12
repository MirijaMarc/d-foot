// French number formatting: 0.39 -> "0,39", 590 -> "590".
// minDigits keeps trailing zeros where they carry meaning: fmt(6, 1) -> "6,0".
export function fmt(value: number, minDigits = 0): string {
  return value.toLocaleString("fr-FR", {
    minimumFractionDigits: minDigits,
    maximumFractionDigits: 2,
  });
}
