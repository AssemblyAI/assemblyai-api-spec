// First get the request_id from a previous LeMUR task response
const request_id = result.data.request_id;

const delete_url = `https://api.assemblyai.com/lemur/v3/${request_id}`;
const deletion_response = await axios.delete(delete_url, { headers });
