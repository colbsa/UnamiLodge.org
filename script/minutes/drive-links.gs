/**
 * drive-links.gs -- Google Apps Script helper for publishing sanitized minutes.
 *
 * WHAT IT DOES
 *   Walks a Drive folder (the sanitized output you uploaded), sets every file to
 *   "Anyone with the link can view", and writes `links.csv` (columns: path,url)
 *   into the same folder.  `build_reports.py --links links.csv` consumes that CSV.
 *
 * HOW TO USE (run it as a Lodge account that owns/manages the shared drive)
 *   1. Upload the sanitized output folder (the one containing manifest.json) to the
 *      Lodge's shared drive.  Note the folder's ID (the last part of its URL).
 *   2. Go to https://script.google.com, create a new project, paste this file.
 *   3. Set ROOT_FOLDER_ID below and run `publishAndListLinks` (authorize when asked).
 *      Re-running is safe: it only changes sharing on files that are not yet public.
 *   4. Download links.csv from the folder and give it to build_reports.py.
 *
 * NOTE: shared-drive policies may forbid "anyone with the link" sharing; if
 * setSharing throws, ask the shared-drive manager to allow external link sharing.
 */
var ROOT_FOLDER_ID = 'PASTE_FOLDER_ID_HERE';

function publishAndListLinks() {
  var root = DriveApp.getFolderById(ROOT_FOLDER_ID);
  var rows = [['path', 'url']];
  walk_(root, '', rows);
  var csv = rows.map(function (r) { return r.map(csvCell_).join(','); }).join('\n');
  var existing = root.getFilesByName('links.csv');
  while (existing.hasNext()) { existing.next().setTrashed(true); }
  root.createFile('links.csv', csv, MimeType.CSV);
  Logger.log('Wrote links.csv with ' + (rows.length - 1) + ' files.');
}

// Recursively visit `folder`; `prefix` is the path relative to the root folder.
function walk_(folder, prefix, rows) {
  var files = folder.getFiles();
  while (files.hasNext()) {
    var f = files.next();
    var name = f.getName();
    if (name === 'links.csv' || name === 'manifest.json' || name === 'report.json') { continue; }
    if (f.getSharingAccess() !== DriveApp.Access.ANYONE_WITH_LINK &&
        f.getSharingAccess() !== DriveApp.Access.ANYONE) {
      f.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    }
    rows.push([prefix + name, f.getUrl()]);
  }
  var subs = folder.getFolders();
  while (subs.hasNext()) {
    var sub = subs.next();
    walk_(sub, prefix + sub.getName() + '/', rows);
  }
}

function csvCell_(v) { return '"' + String(v).replace(/"/g, '""') + '"'; }
