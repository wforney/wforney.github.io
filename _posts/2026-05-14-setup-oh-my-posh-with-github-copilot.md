---
title: "Setup Oh My Posh with GitHub Copilot"
date: 2026-05-14
categories: ["Development", "Terminal", "Productivity"]
tags: ["Oh My Posh", "GitHub Copilot", "PowerShell", "Terminal", "Setup"]
image:
  path: https://images.unsplash.com/premium_photo-1678565999332-1cde462f7b24?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080
  alt: "Code on a computer screen"
---

# Setup Oh My Posh with GitHub Copilot

I recently set up **Oh My Posh** with **GitHub Copilot** integration, and it's absolutely transformed my command-line experience. For those unfamiliar, Oh My Posh is a powerful and extensible shell prompt framework that makes your terminal beautiful and productive, and GitHub Copilot AI brings intelligent command suggestions right to your prompt.

In this post, I'll walk you through the complete setup process—from installation through configuration—so you can get the same productivity boost on your machine.

## Why Oh My Posh + GitHub Copilot?

- **Visual Clarity**: Real-time git status, exit codes, and context at a glance
- **AI-Powered Suggestions**: GitHub Copilot suggests commands based on your intent
- **Cross-Platform**: Works on Windows (PowerShell), macOS, and Linux
- **Highly Customizable**: Themes, segments, and colors galore
- **Performance**: Minimal overhead even with complex prompts

## Prerequisites

- PowerShell 7.4+ (or your preferred shell)
- GitHub Copilot CLI access (requires GitHub Copilot subscription or trial)
- Administrator access for initial installation

## Quick Start

For the impatient, here's the 5-minute version. For detailed steps, see the [complete gist instructions](#).

```powershell
# 1. Install Oh My Posh
winget install JanDeDobbeleer.OhMyPosh

# 2. Install a Nerd Font (e.g., Meslo LGM NF)
# Download from: https://www.nerdfonts.com/
# Or use the Oh My Posh theme installer

# 3. Update your PowerShell profile
# Add to $PROFILE:
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/cloud-native.omp.json" | Out-String | Invoke-Expression

# 4. Install GitHub Copilot CLI
npm install -g @github/cli

# 5. Authenticate
gh auth login
```

Then reload PowerShell, and you're ready to go!

## The Full Guide

I've created a detailed gist with step-by-step instructions, troubleshooting tips, and custom configuration examples. The guide covers:

- System requirements and dependency installation
- Configuring your shell profile
- Customizing Oh My Posh themes and segments
- GitHub Copilot CLI setup and authentication
- Custom prompt segments for your workflows
- Performance tuning for slow machines
- Common issues and solutions

**[Complete Oh My Posh + GitHub Copilot Setup Gist →](https://gist.github.com/wforney/b0f7ff64d10556cea273fe1daba6e78b)****

## What's Next?

Once you've got the basics running, consider:

1. **Explore Themes**: Check out `oh-my-posh theme list` to preview the 150+ built-in themes
2. **Custom Segments**: Add segments for languages you work with (Node, Python, Go, .NET, etc.)
3. **Performance Tweaking**: Disable segments you don't need to keep your prompt responsive
4. **Git Integration**: Leverage the git segment to stay aware of your repo status

## Feedback & Questions?

Got stuck? Found a better approach? Drop me a comment or open an issue on the gist. I'm always interested in how others have customized their setups.

Happy prompting! 🚀
