import { readFile, writeFile } from 'node:fs/promises';

export async function appendRecord(recordPath, record) {
  let records = [];
  try {
    const parsed = JSON.parse(await readFile(recordPath, 'utf8'));
    if (Array.isArray(parsed)) records = parsed;
  } catch {}
  records.push(record);
  await writeFile(recordPath, `${JSON.stringify(records, null, 2)}\n`, 'utf8');
  return record;
}
