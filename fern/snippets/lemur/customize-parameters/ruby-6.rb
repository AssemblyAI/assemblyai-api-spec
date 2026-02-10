# First get the request_id from a previous LeMUR task response
request_id = lemur_result["request_id"]

delete_uri = URI("#{base_url}/lemur/v3/#{request_id}")
delete_request = Net::HTTP::Delete.new(delete_uri, headers)
deletion_response = http.request(delete_request)
