const SHEET_NAME = 'Record';
const USER_SHEET_NAME = 'User';

// Helper function to get Chinese name by email
function getUserNameByEmail(email) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(USER_SHEET_NAME);
  if (!sheet) return email; // fallback to email if User sheet missing
  
  const data = sheet.getDataRange().getValues();
  // Assume Row 1 is header. Column A (0) is Name, Column B (1) is Email
  for (let i = 1; i < data.length; i++) {
    if (data[i][1] === email) {
      return data[i][0]; // Return the Chinese name
    }
  }
  return email; // fallback to email if not found
}

function doGet(e) {
  const email = e.parameter.email;
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'Sheet "Record" not found.' }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  // Get the Chinese name for this email
  const userName = getUserNameByEmail(email);

  const data = sheet.getDataRange().getValues();
  const result = [];
  
  // Start from row 1 (index 1) assuming row 0 is headers
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    // Check if the row is not empty and matches the User Name (or email as fallback)
    if (row[0] && (row[1] === userName || row[1] === email)) {
      
      let dateStr = row[0];
      if (dateStr instanceof Date) {
        dateStr = Utilities.formatDate(dateStr, Session.getScriptTimeZone(), "yyyy/MM/dd");
      }
      
      let logTime = row[4];
      if (logTime instanceof Date) {
         logTime = Utilities.formatDate(logTime, Session.getScriptTimeZone(), "HH:mm");
      }
      
      // Return: [Date, Type, Reps, LogTime, RowIndex]
      result.push([
        dateStr,
        row[2], // Type
        row[3], // Reps
        logTime, // Log time
        i + 1   // Row Index (1-based)
      ]);
    }
  }

  return ContentService.createTextOutput(JSON.stringify({ 
    status: 'success', 
    data: result,
    username: userName 
  })).setMimeType(ContentService.MimeType.JSON);
}


function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    const data = JSON.parse(e.postData.contents);
    const action = data.action;

    if (action === 'add') {
      const userName = getUserNameByEmail(data.email);
      // Append a new row: [Date, User, Type, Reps, LogTime]
      sheet.appendRow([
        data.date, 
        userName, 
        data.type, 
        data.count, 
        data.time
      ]);
      return ContentService.createTextOutput(JSON.stringify({ status: 'success' }))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === 'edit') {
      // Update the reps count for the specific row
      const rowIndex = data.rowIndex;
      // Update Column D (Reps), which is column index 4
      sheet.getRange(rowIndex, 4).setValue(data.count);
      return ContentService.createTextOutput(JSON.stringify({ status: 'success' }))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === 'delete') {
      // Clear the row contents (don't deleteRow to prevent shifting indices)
      const rowIndex = data.rowIndex;
      sheet.getRange(rowIndex, 1, 1, 5).clearContent();
      return ContentService.createTextOutput(JSON.stringify({ status: 'success' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: 'Unknown action' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doOptions(e) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
  return ContentService.createTextOutput('').setMimeType(ContentService.MimeType.JSON);
}
