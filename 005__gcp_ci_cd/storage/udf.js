/**
 * User-defined function (UDF) to transform elements as part of a Dataflow
 * template job.
 *
 * @param {string} inJson input JSON message (stringified)
 * @return {?string} outJson output JSON message (stringified)
 */
function process(inJson) {
  const obj = JSON.parse(inJson);

  obj.id = "id-" + obj.id
  obj.message = "message-" + obj.message

  return JSON.stringify(obj);
}
