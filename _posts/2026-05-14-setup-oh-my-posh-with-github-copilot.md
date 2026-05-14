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

GitHub Copilot CLI has an experimental statusline feature that lets you render custom output at the bottom of the Copilot terminal UI. If you already use Oh My Posh, you can reuse the same rendering engine, colors, and segments to create a beautiful Copilot-aware statusline in just a few minutes.

This guide shows how to set it up on Windows with PowerShell, but the approach is portable to macOS and Linux.

## How It Works

1. Copilot calls a local script when the statusline needs to update
2. Copilot sends session state (tokens used, duration, branch, etc.) as JSON on stdin
3. Your script maps those values into environment variables
4. Oh My Posh renders a small statusline theme using those variables

The result: a beautiful statusline showing git branch, runtime info, token usage, and more—all styled with your favorite Oh My Posh theme.

## Example Output

```
main +2/-1 | .NET 10.0 | 123.5k/200.0k | ######.... | 00:12:34 | +42/-8
```

This shows: branch, changes, runtime, token usage gauge, elapsed time, and line changes—all from Oh My Posh rendering!

## Prerequisites

- **GitHub Copilot CLI** with experimental statusline support
- **PowerShell 7+** (`pwsh`)
- **Oh My Posh** installed and on your PATH
- A **Nerd Font** (optional, but recommended for icons)

Verify your setup:

```powershell
oh-my-posh version
gh copilot --help
```

## Step 1: Create the Statusline Directory

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.copilot" | Out-Null
```

## Step 2: Create the Command Wrapper

Create `%USERPROFILE%\.copilot\statusline.cmd`:

```cmd
@echo off
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0statusline.ps1"
```

This wrapper ensures stdin is preserved when Copilot calls your statusline script.

## Step 3: Create the PowerShell Renderer

Create `%USERPROFILE%\.copilot\statusline.ps1`. This is where the magic happens—it reads Copilot's JSON payload and feeds data into Oh My Posh:

```powershell
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

# Helper functions for formatting
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

# Read Copilot's JSON payload from stdin
$payload = [Console]::In.ReadToEnd()

try {
    $json = $payload | ConvertFrom-Json
} catch {
    Write-Host -NoNewline 'Copilot status unavailable'
    exit 0
}

# Extract context and cost data
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

# Set environment variables for Oh My Posh to use
$env:COPILOT_TOKENS_CURRENT = Format-TokenCount $currentTokens
$env:COPILOT_TOKENS_LIMIT = Format-TokenCount $contextLimit
$env:COPILOT_CONTEXT_GAUGE = New-Gauge $contextPercent
$env:COPILOT_DURATION = Format-Duration $cost.total_milliseconds
$env:COPILOT_BRANCH = $json.branch_name

# Call Oh My Posh to render the statusline theme
& oh-my-posh print line --config "$env:USERPROFILE\.copilot\statusline.omp.json"
```

## Step 4: Create Your Statusline Theme

Create `%USERPROFILE%\.copilot\statusline.omp.json` with your Oh My Posh theme:

```json
{
  "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
  "version": 3,
  "blocks": [
    {
      "type": "prompt",
      "alignment": "left",
      "segments": [
        {
          "type": "text",
          "properties": {
            "text": " {{ .Env.COPILOT_BRANCH }} "
          },
          "style": "plain",
          "foreground": "#0098FF"
        },
        {
          "type": "text",
          "properties": {
            "text": "{{ .Env.COPILOT_TOKENS_CURRENT }}/{{ .Env.COPILOT_TOKENS_LIMIT }}"
          },
          "style": "plain",
          "foreground": "#90EE90"
        },
        {
          "type": "text",
          "properties": {
            "text": " {{ .Env.COPILOT_CONTEXT_GAUGE }} "
          },
          "style": "plain",
          "foreground": "#FFD700"
        },
        {
          "type": "text",
          "properties": {
            "text": "⏱ {{ .Env.COPILOT_DURATION }}"
          },
          "style": "plain",
          "foreground": "#FFA500"
        }
      ]
    }
  ]
}
```

## Step 5: Enable the Statusline in Copilot Settings

Open your Copilot settings at `%USERPROFILE%\.copilot\settings.json` and add:

```json
{
  "statusLine": {
    "enabled": true,
    "command": "%USERPROFILE%\\.copilot\\statusline.cmd"
  },
  "feature_flags": {
    "enabled": ["STATUS_LINE"]
  }
}
```

## Step 6: Restart Copilot

If Copilot CLI is already running, restart it:

```powershell
/restart
```

Then start a new Copilot chat. Your statusline should appear at the bottom!

## Customization

Your statusline is now powered by Oh My Posh. To customize it:

- **Add more segments**: Reference additional environment variables in your theme
- **Change colors**: Update the foreground/background hex values
- **Adjust spacing**: Modify the text properties in the JSON theme
- **Reuse your main theme**: Copy styling from your shell prompt theme

Remember: keep the statusline fast! Use only the data Copilot provides, and avoid expensive operations.

## Troubleshooting

**Statusline doesn't appear:**
- Verify the feature flag is enabled: `STATUS_LINE` in `feature_flags.enabled`
- Check that `statusLine.command` points to the correct `.cmd` file path
- Ensure PowerShell can access the script: `Test-Path "$env:USERPROFILE\.copilot\statusline.ps1"`

**Broken output in statusline:**
- Verify `oh-my-posh print line` works manually: `& oh-my-posh print line --config "..."`
- Check environment variables are set: `$env:COPILOT_TOKENS_CURRENT`
- Confirm your Nerd Font supports the glyphs (if using icons)

**Performance issues:**
- Keep the statusline theme minimal—fewer segments render faster
- Avoid calling external commands in the renderer

## Next Steps

- Share your custom statusline theme with the community
- Extend the renderer to include additional Copilot context
- Customize colors to match your Oh My Posh shell theme

Happy Copilot-ing! 🚀
