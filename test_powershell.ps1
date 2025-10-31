# PowerShell test script for MoodMatch A2A Agent
# Run this after starting the server with: python main.py

Write-Host "`n🎭 MoodMatch A2A Agent - PowerShell Test" -ForegroundColor Cyan
Write-Host "=" * 60

# Test 1: Health Check
Write-Host "`n1️⃣  Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ Health Check Passed!" -ForegroundColor Green
    Write-Host ($healthResponse | ConvertTo-Json)
} catch {
    Write-Host "❌ Health Check Failed: $_" -ForegroundColor Red
    exit 1
}

# Test 2: A2A Request
Write-Host "`n2️⃣  Testing Mood Analysis..." -ForegroundColor Yellow

$body = @{
    jsonrpc = "2.0"
    id = "test-123"
    method = "execute"
    params = @{
        messages = @(
            @{
                role = "user"
                parts = @(
                    @{
                        kind = "text"
                        text = "I'm feeling stressed and need to relax"
                    }
                )
            }
        )
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/a2a/moodmatch" `
                                   -Method Post `
                                   -ContentType "application/json" `
                                   -Body $body
    
    if ($response.result) {
        Write-Host "✅ Request Successful!" -ForegroundColor Green
        Write-Host "`n📊 Task State: $($response.result.status.state)" -ForegroundColor Cyan
        
        # Show agent response
        if ($response.result.history) {
            $agentMessage = $response.result.history | Where-Object { $_.role -eq "agent" } | Select-Object -First 1
            if ($agentMessage -and $agentMessage.parts) {
                Write-Host "`n💬 Agent Response:" -ForegroundColor Cyan
                Write-Host $agentMessage.parts[0].text.Substring(0, [Math]::Min(500, $agentMessage.parts[0].text.Length)) -ForegroundColor White
                Write-Host "..." -ForegroundColor Gray
            }
        }
        
        # Show artifacts
        if ($response.result.artifacts) {
            Write-Host "`n📦 Artifacts ($($response.result.artifacts.Count)):" -ForegroundColor Cyan
            foreach ($artifact in $response.result.artifacts) {
                Write-Host "   • $($artifact.name)" -ForegroundColor White
            }
        }
        
        Write-Host "`n✅ All tests passed!" -ForegroundColor Green
    } elseif ($response.error) {
        Write-Host "❌ Error: $($response.error.message)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Request Failed: $_" -ForegroundColor Red
    Write-Host $_.Exception.Response.StatusCode -ForegroundColor Red
}

Write-Host "`n" + ("=" * 60)
Write-Host "Test complete!" -ForegroundColor Cyan
