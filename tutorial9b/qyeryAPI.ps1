# Define the API URL
$apiUrl = "http://127.0.0.1:8005/chain/invoke"

# Prompt the user for text input (already included in the $body)
$body = @{
  input = @{
    input = "How many servers are there and give me all the details includig OS"
  }
  config = @{}
  kwargs = @{}
}

# Convert the body to JSON format
$jsonBody = $body | ConvertTo-Json

# Send POST request to the API
try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $jsonBody -ContentType "application/json"
    Write-Output "$($response.output)"
} catch {
    Write-Error "API call failed: $_"
}
