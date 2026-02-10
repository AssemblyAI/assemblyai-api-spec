// First get the request_id from a previous LeMUR task response
string request_id = lemurResponse.RequestId;

string delete_url = $"https://api.assemblyai.com/lemur/v3/{request_id}";
using var deletion_response = await httpClient.DeleteAsync(delete_url);
