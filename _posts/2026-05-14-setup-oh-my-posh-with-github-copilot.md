---
title: "Setup Oh My Posh with GitHub Copilot"
date: 2026-05-14
categories: ["Development", "Terminal", "Productivity"]
tags: ["Oh My Posh", "GitHub Copilot", "PowerShell", "Terminal", "Setup"]
image:
  path: /assets/img/posts/oh-my-posh-copilot.jpg
  alt: "Code on a computer screen"
---

# Setup Oh My Posh with GitHub Copilot

I recently integrated **GitHub Copilot CLI** directly into my **Oh My Posh** prompt, and it's transformed how I work in the terminal. Instead of switching contexts to ask Copilot for help, I now have intelligent command suggestions baked right into my prompt as a custom segment.

In this post, I'll show you how to add a Copilot segment to Oh My Posh—complete with working configuration and troubleshooting tips—so you can get smart command suggestions without leaving your shell.

## Why Integrate Copilot into Your Prompt?

- **Zero Context Switching**: Ask Copilot without typing a separate command
- **Visual Integration**: See suggestions as part of your prompt theme
- **Faster Workflows**: Common tasks become muscle memory
- **Learning Tool**: Discover better approaches to command-line tasks
- **AI-Powered Help**: Natural language → shell command translations

## Prerequisites

- Oh My Posh installed and configured
- GitHub Copilot CLI (`gh copilot`) set up and authenticated
- PowerShell 7.4+, Bash, or Zsh
- A Nerd Font (for icons—recommended but optional)

## Step 1: Install & Authenticate GitHub Copilot CLI

First, ensure you have the GitHub CLI installed and authenticated:

```bash
# Install GitHub CLI (if not already installed)
# On Windows: winget install GitHub.cli
# On macOS: brew install gh
# On Linux: Follow https://cli.github.com/

# Authenticate
gh auth login

# Verify Copilot CLI is available
gh copilot --help
```

## Step 2: Create a Copilot Segment for Oh My Posh

Oh My Posh uses custom segments to add elements to your prompt. Create a new JSON configuration file for your Copilot segment or update your existing Oh My Posh theme.

Here's a minimal example that adds a Copilot-aware segment to your prompt. Create or edit your `oh-my-posh` config file (typically at `$env:POSH_THEMES_PATH/copilot-theme.omp.json`):

```json
{
  "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
  "version": 3,
  "palette": {
    "copilot-blue": "#0098FF"
  },
  "blocks": [
    {
      "type": "prompt",
      "alignment": "left",
      "segments": [
        {
          "type": "text",
          "style": "plain",
          "properties": {
            "prefix": " ",
            "text": "copilot"
          },
          "foreground": "#0098FF"
        },
        {
          "type": "path",
          "style": "plain",
          "properties": {
            "style": "full"
          }
        }
      ]
    }
  ]
}
```

## Step 3: Add a Function to Your Profile

To make Copilot integration seamless, add this function to your PowerShell profile (`$PROFILE`):

```powershell
function copilot {
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$Arguments
    )
    
    $query = $Arguments -join ' '
    
    if ([string]::IsNullOrWhiteSpace($query)) {
        Write-Host "Usage: copilot <description of what you want to do>"
        Write-Host "Example: copilot find all files modified in the last hour"
        return
    }
    
    gh copilot suggest -t shell -d $query
}
```

Then use it directly in your prompt:

```powershell
copilot find all files modified in the last hour
copilot list all Docker containers and their sizes
copilot backup my database
```

## Step 4: Initialize Oh My Posh with Your Theme

In your PowerShell profile, initialize Oh My Posh with your custom theme:

```powershell
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/copilot-theme.omp.json" | Out-String | Invoke-Expression
```

If you've named it differently, adjust the path accordingly.

## Practical Examples

Once integrated, your workflow becomes much faster:

**Before** (switching contexts):
```powershell
# You're in the terminal
cd myproject
# Now open a browser or separate window to ask Copilot
# Come back and type commands manually
```

**After** (integrated):
```powershell
cd myproject
copilot recursively find all TypeScript files with console.log
# Copilot suggests: find . -name "*.ts" -exec grep -l "console.log" {} \;
copilot show git log with one line per commit from last week
# Copilot suggests: git log --oneline --since="1 week ago"
```

## Troubleshooting

**"gh copilot" command not found:**
- Run `gh auth status` to verify you're authenticated
- Run `gh extension list` to check if Copilot CLI is installed
- If missing, run `gh auth refresh --scopes copilot`

**Copilot suggestions not working in your prompt:**
- Verify `gh copilot suggest --help` works in isolation
- Check that your shell has GitHub credentials cached: `gh auth token`
- Ensure your GitHub Copilot subscription is active

**Slow prompt rendering:**
- If your custom segment slows things down, remove it and call `copilot` on-demand instead of embedding it in the prompt

## Next Steps

- **Explore Copilot modes**: Try `gh copilot explain` for command explanations
- **Automate common tasks**: Create aliases for frequent Copilot queries
- **Share your setup**: Show your colleagues how to integrate Copilot into their prompts
- **Customize further**: Adjust colors, icons, and theme positioning to match your style

Happy prompting! 🚀
