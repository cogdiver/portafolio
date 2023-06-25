/**
 * User-defined function (UDF) to transform elements as part of a Dataflow
 * template job.
 *
 * @param {string} inJson input JSON message (stringified)
 * @return {?string} outJson output JSON message (stringified)
 */
function process(inJson) {
  const obj = JSON.parse(inJson);

  // Add a field: obj.newField = 1;
  obj.newField = 1
  // Modify a field: obj.existingField = '';
  obj.existingField = ''
  // Filter a record: return null;

  return JSON.stringify(obj);
}
