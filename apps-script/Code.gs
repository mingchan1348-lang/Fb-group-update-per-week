/*
 * Google Apps Script bridge for Weekly Property Updates.
 * Paste this file into script.google.com, set the two values below, then deploy as a Web App.
 */
const SHEET_ID = '1OpGUbkCuFmu_lW6eE-fi98bq2U2_47WYSivIrq0iLec';
const SHARED_SECRET = 'REPLACE_WITH_A_LONG_RANDOM_PASSPHRASE';
const TAB_NAME = 'posts';

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.secret !== SHARED_SECRET) return reply({ok: false, error: 'Unauthorized'});
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_NAME);
    if (!sheet) throw new Error(`Missing sheet tab: ${TAB_NAME}`);
    const values = sheet.getDataRange().getValues();
    const headers = values.shift();
    if (body.action === 'list') {
      return reply({ok: true, rows: values.map((row, index) => Object.assign({__row_number: index + 2}, Object.fromEntries(headers.map((header, col) => [header, String(row[col] ?? '')]))))});
    }
    if (body.action === 'update') {
      const row = Number(body.row_number);
      if (row < 2) throw new Error('Invalid row number');
      Object.entries(body.changes || {}).forEach(([field, value]) => {
        const column = headers.indexOf(field);
        if (column === -1) throw new Error(`Missing column: ${field}`);
        sheet.getRange(row, column + 1).setValue(value);
      });
      return reply({ok: true});
    }
    throw new Error('Unknown action');
  } catch (error) {
    return reply({ok: false, error: String(error)});
  }
}

function reply(value) {
  return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
}
