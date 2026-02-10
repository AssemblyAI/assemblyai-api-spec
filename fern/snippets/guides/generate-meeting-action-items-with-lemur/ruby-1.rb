require 'net/http'
require 'json'
require 'rest-client'
require 'httparty'

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization" => "<YOUR_API_KEY>",
    "content-type" => "application/json"
}
