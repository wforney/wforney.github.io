---
title: "Render GitHub Copilot CLI's Statusline with Oh My Posh"
date: 2026-05-14
categories: ["Development", "Terminal", "GitHub Copilot"]
tags: ["GitHub Copilot", "Oh My Posh", "PowerShell", "CLI", "Statusline"]
image:
  path: /assets/img/posts/oh-my-posh-copilot.jpg
  alt: "Code on a computer screen"
---

# Render GitHub Copilot CLI's Statusline with Oh My Posh

GitHub Copilot CLI supports a custom statusline command. You can use that hook to run a PowerShell script, map Copilot session data to environment variables, and render the output with Oh My Posh.

This is the working Windows setup I use locally.

## Prerequisites

- GitHub Copilot CLI
- PowerShell 7+
- Oh My Posh installed and on `PATH`
- Nerd Font (recommended for glyphs)

Quick check:

```powershell
oh-my-posh version
gh copilot --help
```

## 1. Create the Copilot config folder

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.copilot" | Out-Null
```

## 2. Create the statusline command wrapper

Create `%USERPROFILE%\.copilot\statusline.cmd`:

```cmd
@echo off
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0statusline.ps1"
```

## 3. Create the PowerShell renderer

Create `%USERPROFILE%\.copilot\statusline.ps1`:

```powershell
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# Cache directory for performance optimization
$cacheDir = "$env:USERPROFILE\.copilot\.cache"
if (-not (Test-Path $cacheDir)) {
    New-Item -ItemType Directory -Force $cacheDir | Out-Null
}

function Format-TokenCount {
    param([Nullable[double]]$Value)

    if ($null -eq $Value) { return '?' }
    if ($Value -ge 1000000) { return ('{0:0.0}m' -f ($Value / 1000000)) }
    if ($Value -ge 1000) { return ('{0:0.0}k' -f ($Value / 1000)) }
    return ([int]$Value).ToString()
}

function Format-Duration {
    param([Nullable[double]]$Milliseconds)

    if ($null -eq $Milliseconds -or $Milliseconds -le 0) { return '00:00:00' }
    $duration = [TimeSpan]::FromMilliseconds($Milliseconds)
    return '{0:00}:{1:00}:{2:00}' -f [int]$duration.TotalHours, $duration.Minutes, $duration.Seconds
}

function New-Gauge {
    param([Nullable[double]]$Percent)

    if ($null -eq $Percent) { return '..........' }
    $bounded = [Math]::Max(0, [Math]::Min(100, [Math]::Round($Percent)))
    $filled = [int][Math]::Floor($bounded / 10)
    return ('#' * $filled) + ('.' * (10 - $filled))
}

$payload = [Console]::In.ReadToEnd()

# Cache check - return cached output if payload hasn't changed
$payloadHash = (Get-FileHash -InputStream ([System.IO.MemoryStream]::new([System.Text.Encoding]::UTF8.GetBytes($payload))) -Algorithm SHA256).Hash
$cacheFile = Join-Path $cacheDir "payload-$payloadHash.txt"
$cacheOutput = Join-Path $cacheDir "output-$payloadHash.txt"

if ((Test-Path $cacheFile) -and (Test-Path $cacheOutput)) {
    Write-Host -NoNewline (Get-Content $cacheOutput)
    exit 0
}

try {
    $json = $payload | ConvertFrom-Json
} catch {
    Write-Host -NoNewline 'Copilot status unavailable'
    exit 0
}

$context = $json.context_window
$cost = $json.cost

$currentTokens = if ($null -ne $context.current_context_tokens) {
    [double]$context.current_context_tokens
} else {
    $null
}

$contextLimit = if ($null -ne $context.displayed_context_limit) {
    [double]$context.displayed_context_limit
} else {
    $null
}

$contextPercent = if ($null -ne $context.current_context_used_percentage) {
    [double]$context.current_context_used_percentage
} elseif ($null -ne $context.used_percentage) {
    [double]$context.used_percentage
} else {
    $null
}

$linesAdded = if ($null -ne $cost.total_lines_added) { [int]$cost.total_lines_added } else { 0 }
$linesRemoved = if ($null -ne $cost.total_lines_removed) { [int]$cost.total_lines_removed } else { 0 }

$tokenPercent = if ($null -ne $currentTokens -and $null -ne $contextLimit -and $contextLimit -gt 0) {
    [Math]::Round(($currentTokens / $contextLimit) * 100)
} else {
    0
}

$model = 'GPT-4'
if ($null -ne $json.model) {
    if ($json.model -is [string]) {
        $model = $json.model
    } elseif ($null -ne $json.model.display_name) {
        $model = [string]$json.model.display_name
    } elseif ($null -ne $json.model.id) {
        $model = [string]$json.model.id
    } else {
        $model = [string]$json.model
    }
}

$copilotError = if ($json.error) { $json.error } else { $null }
$status = if ($copilotError) { "ERROR: $copilotError" } else { "ready" }
$fileCount = if ($json.files -is [array]) { $json.files.Count } elseif ($null -ne $json.files) { 1 } else { 0 }
$responseMs = if ($null -ne $json.response_time_ms) { [int]$json.response_time_ms } else { 0 }

$env:COPILOT_STATUS_CONTEXT = "$(Format-TokenCount $currentTokens)/$(Format-TokenCount $contextLimit)"
$env:COPILOT_STATUS_GAUGE = New-Gauge $contextPercent
$env:COPILOT_STATUS_DURATION = Format-Duration $cost.total_duration_ms
$env:COPILOT_STATUS_CHANGES = if ($linesAdded -or $linesRemoved) { "+$linesAdded/-$linesRemoved" } else { '' }
$env:COPILOT_TOKEN_PERCENT = $tokenPercent
$env:COPILOT_MODEL = $model
$env:COPILOT_STATUS = $status
$env:COPILOT_FILE_COUNT = $fileCount
$env:COPILOT_RESPONSE_MS = $responseMs

$theme = Join-Path $PSScriptRoot 'statusline.omp.json'
$cwd = if ($json.cwd) { [string]$json.cwd } else { (Get-Location).Path }

try {
    $output = & oh-my-posh print primary --config $theme --pwd $cwd --force --escape=false 2>$null
    if ([string]::IsNullOrWhiteSpace($output)) {
        throw 'Oh My Posh returned no output.'
    }

    Set-Content -Path $cacheFile -Value $payload -Force | Out-Null
    Set-Content -Path $cacheOutput -Value $output.TrimEnd() -Force | Out-Null

    Write-Host -NoNewline $output.TrimEnd()
} catch {
    $segments = @(
        "🤖 $($env:COPILOT_MODEL)"
        "ctx $($env:COPILOT_STATUS_CONTEXT)"
        "$($env:COPILOT_STATUS_GAUGE)"
        "⏱ $($env:COPILOT_STATUS_DURATION)"
    )

    if ($env:COPILOT_FILE_COUNT -gt 0) {
        $segments += "📄 $($env:COPILOT_FILE_COUNT)"
    }

    if ($env:COPILOT_STATUS_CHANGES) {
        $segments += $env:COPILOT_STATUS_CHANGES
    }

    if ($env:COPILOT_STATUS -ne 'ready') {
        $segments += "⚠️ $($env:COPILOT_STATUS)"
    }

    $fallback = $segments -join " | "

    Set-Content -Path $cacheFile -Value $payload -Force | Out-Null
    Set-Content -Path $cacheOutput -Value $fallback -Force | Out-Null

    Write-Host -NoNewline $fallback
}
```

## 4. Create the statusline theme (plain segments + right-end triangle)

Create `%USERPROFILE%\.copilot\statusline.omp.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
  "version": 4,
  "final_space": false,
  "blocks": [
    {
      "type": "prompt",
      "alignment": "left",
      "segments": [
        {
          "type": "text",
          "style": "plain",
          "foreground": "#ffffff",
          "background": "#c386f1",
          "template": " \uf489 Copilot "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#ffffff",
          "background": "#ff479c",
          "template": " 🤖 {{ .Env.COPILOT_MODEL }} "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#ffffff",
          "background": "#6CA35E",
          "template": " \uea83 ctx {{ .Env.COPILOT_STATUS_CONTEXT }} ({{ .Env.COPILOT_TOKEN_PERCENT }}%) "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#193549",
          "background": "#fffb38",
          "template": " {{ .Env.COPILOT_STATUS_GAUGE }} "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#ffffff",
          "background": "#8ED1F7",
          "template": " \ueba2 {{ .Env.COPILOT_STATUS_DURATION }} "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#111111",
          "background": "#6CA35E",
          "template": " 📄 {{ .Env.COPILOT_FILE_COUNT }} "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#111111",
          "background": "#FF9248",
          "template": " ⚡ {{ .Env.COPILOT_RESPONSE_MS }}ms "
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#ffffff",
          "background": "#00897b",
          "template": "{{ if .Env.COPILOT_STATUS_CHANGES }} {{ .Env.COPILOT_STATUS_CHANGES }} {{ else if eq .Env.COPILOT_STATUS \"ready\" }} ✓ {{ else }} ⚠️ {{ end }}"
        },
        {
          "type": "text",
          "style": "plain",
          "foreground": "#00897b",
          "background": "transparent",
          "template": "\ue0b0"
        }
      ]
    }
  ]
}
```

## 5. Enable statusline in Copilot settings

In `%USERPROFILE%\.copilot\settings.json`:

```json
{
  "statusLine": {
    "enabled": true,
    "type": "command",
    "command": "%USERPROFILE%\\.copilot\\statusline.cmd",
    "padding": 1
  },
  "feature_flags": {
    "enabled": ["STATUS_LINE"]
  }
}
```

If you prefer, you can use an absolute path instead of `%USERPROFILE%`.

## 6. Restart Copilot CLI

Close Copilot CLI and launch it again:

```powershell
gh copilot
```

## Troubleshooting

**No statusline appears**
- Confirm `STATUS_LINE` exists in `feature_flags.enabled`
- Confirm `statusLine.enabled` is `true`
- Confirm `statusLine.command` points to `statusline.cmd`

**Broken output**
- Run this manually to verify rendering:
  `oh-my-posh print primary --config "$env:USERPROFILE\.copilot\statusline.omp.json" --force`
- Confirm script exists:
  `Test-Path "$env:USERPROFILE\.copilot\statusline.ps1"`

**Slow rendering**
- Clear cache once if needed:
  `Remove-Item "$env:USERPROFILE\.copilot\.cache\*" -Force -ErrorAction SilentlyContinue`

That’s it. You now have a Copilot statusline rendered by Oh My Posh with the same working theme and script used in this post.
