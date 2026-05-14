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

Create `%USERPROFILE%\.copilot\statusline.omp.json` using the jandedobbeleer theme style but optimized for the statusline:

```json
{
  "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
  "version": 4,
  "blocks": [
    {
      "type": "prompt",
      "alignment": "left",
      "segments": [
        {
          "type": "text",
          "style": "diamond",
          "leading_diamond": "\ue0b6",
          "trailing_diamond": "\ue0b0",
          "background": "#c386f1",
          "foreground": "#ffffff",
          "template": " branch: {{ .Env.COPILOT_BRANCH }} "
        },
        {
          "type": "text",
          "style": "powerline",
          "powerline_symbol": "\ue0b0",
          "background": "#fffb38",
          "foreground": "#193549",
          "template": " tokens: {{ .Env.COPILOT_TOKENS_CURRENT }}/{{ .Env.COPILOT_TOKENS_LIMIT }} "
        },
        {
          "type": "text",
          "style": "powerline",
          "powerline_symbol": "\ue0b0",
          "background": "#6CA35E",
          "foreground": "#ffffff",
          "template": " {{ .Env.COPILOT_CONTEXT_GAUGE }} "
        },
        {
          "type": "text",
          "style": "powerline",
          "powerline_symbol": "\ue0b0",
          "background": "#8ED1F7",
          "foreground": "#111111",
          "template": " \ueba2 {{ .Env.COPILOT_DURATION }} "
        },
        {
          "type": "text",
          "style": "diamond",
          "leading_diamond": "\ue0b6",
          "trailing_diamond": "\ue0b4",
          "background": "#00897b",
          "foreground": "#ffffff",
          "template": " ready "
        }
      ]
    }
  ],
  "final_space": true,
  "version": 4
}
```

This statusline uses the same powerline style and color palette as the jandedobbeleer theme for visual consistency.

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
- **Change colors**: Update the foreground/background hex values to match your jandedobbeleer theme
- **Adjust spacing**: Modify the text templates and powerline symbols
- **Reuse your main theme**: The jandedobbeleer colors work great—purple (#c386f1), pink (#ff479c), yellow (#fffb38), green (#6CA35E), blue (#8ED1F7)

Remember: keep the statusline fast! Use only the data Copilot provides, and avoid expensive operations.

## Suggested Improvements

Here are some enhancements to consider implementing:

### 1. **Dynamic Token Warning Colors**

Change the token segment color based on usage percentage. Update your PowerShell renderer to calculate percent:

```powershell
if ($null -ne $currentTokens -and $null -ne $contextLimit -and $contextLimit -gt 0) {
    $env:COPILOT_TOKEN_PERCENT = [Math]::Round(($currentTokens / $contextLimit) * 100)
} else {
    $env:COPILOT_TOKEN_PERCENT = 0
}
```

Then use conditional backgrounds in your theme:

```json
{
  "type": "text",
  "style": "powerline",
  "background_templates": [
    "{{ if gt .Env.COPILOT_TOKEN_PERCENT 90 }}#ff4500{{ else if gt .Env.COPILOT_TOKEN_PERCENT 70 }}#FFD700{{ else }}#6CA35E{{ end }}"
  ],
  "powerline_symbol": "\ue0b0",
  "foreground": "#ffffff",
  "template": " tokens: {{ .Env.COPILOT_TOKENS_CURRENT }}/{{ .Env.COPILOT_TOKENS_LIMIT }} "
}
```

### 2. **Show Model Name**

Extract and display the model being used:

```powershell
$env:COPILOT_MODEL = if ($json.model) { $json.model } else { 'GPT-4' }
```

Add to your theme:

```json
{
  "type": "text",
  "style": "powerline",
  "background": "#6CA35E",
  "foreground": "#ffffff",
  "powerline_symbol": "\ue0b0",
  "template": " 🤖 {{ .Env.COPILOT_MODEL }} "
}
```

### 3. **Cache Renders to Reduce Oh My Posh Calls**

Avoid calling Oh My Posh on every Copilot status update if nothing changed:

```powershell
$cacheFile = "$env:USERPROFILE\.copilot\statusline.cache"
$payload | Out-File $cacheFile

# On next run, compare payloads:
if ((Get-Content $cacheFile -Raw) -eq $payload) {
    Get-Content "$cacheFile.output" 2>$null
    exit 0
}
```

### 4. **Error Status Indicator**

If Copilot encounters an error, show it in the statusline:

```powershell
$env:COPILOT_STATUS = if ($json.error) { 
    "ERROR: $($json.error)" 
} else { 
    "ready" 
}
```

Add a status segment to your theme that changes color on error.

### 5. **File Changes from Context**

If the payload includes file metadata, show how many files are in the context:

```powershell
$env:COPILOT_FILE_COUNT = $json.files.count
```

### 6. **Response Time Gauge**

Track how long Copilot took to generate suggestions:

```powershell
$env:COPILOT_RESPONSE_MS = $json.response_time_ms
```

Add an icon that changes based on response speed (fast = green, slow = yellow).

### 7. **Batch Renderer Invocations**

For Windows, the `.cmd` wrapper adds overhead. Consider a faster implementation:

```powershell
# Instead of calling external Oh My Posh, build the output directly
$segments = @(
    "✓ $($env:COPILOT_BRANCH)",
    "$($env:COPILOT_TOKENS_CURRENT)/$($env:COPILOT_TOKENS_LIMIT)",
    $env:COPILOT_CONTEXT_GAUGE,
    "⏱ $($env:COPILOT_DURATION)"
)
Write-Host ($segments -join " | ")
```

This trades Oh My Posh styling for faster startup.

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
