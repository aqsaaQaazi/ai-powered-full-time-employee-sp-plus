---
id: 1
title: Update constitution for AI Employee
stage: constitution
date_iso: 2026-03-02
surface: agent
model: claude-opus-4-6
feature: ai-employee
branch: main
user: HAROON TRADERS
command: /sp.constitution
labels: ["constitution", "ai-employee", "personal-automation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
prompt_text: |
  Bronze Tier: Foundation (Minimum Viable Deliverable)
  Estimated time: 8-12 hours
  Obsidian vault with Dashboard.md and Company_Handbook.md
  One working Watcher script (Gmail OR file system monitoring)
  Claude Code successfully reading from and writing to the vault
  Basic folder structure: /Inbox, /Needs_Action, /Done
  All AI functionality should be implemented as Agent Skills
  Silver Tier: Functional Assistant
  Estimated time: 20-30 hours
  All Bronze requirements plus:
  Two or more Watcher scripts (e.g., Gmail + Whatsapp + LinkedIn)
  Automatically Post on LinkedIn about business to generate sales
  Claude reasoning loop that creates Plan.md files
  One working MCP server for external action (e.g., sending emails)
  Human-in-the-loop approval workflow for sensitive actions
  Basic scheduling via cron or Task Scheduler
  All AI functionality should be implemented as Agent Skills
  Gold Tier: Autonomous Employee
  Estimated time: 40+ hours
  All Silver requirements plus:
  Full cross-domain integration (Personal + Business)
  Create an accounting system for your business in Odoo Community (self-hosted, local) and integrate it via an MCP server using Odoo's JSON-RPC APIs (Odoo 19+).
  Integrate Facebook and Instagram and post messages and generate summary
  Integrate Twitter (X) and post messages and generate summary
  Multiple MCP servers for different action types
  Weekly Business and Accounting Audit with CEO Briefing generation
  Error recovery and graceful degradation
  Comprehensive audit logging
  Ralph Wiggum loop for autonomous multi-step task completion (see Section 2D)
  Documentation of your architecture and lessons learned
  All AI functionality should be implemented as Agent Skills

  Platinum Tier: Always-On Cloud + Local Executive (Production-ish AI Employee)
  Estimated time: 60+ hours
  All Gold requirements plus:
  Run the AI Employee on Cloud 24/7 (always-on watchers + orchestrator + health monitoring). You can deploy a Cloud VM (Oracle/AWS/etc.) - Oracle Cloud Free VMs can be used for this (subject to limits/availability).
  Work-Zone Specialization (domain ownership):
  Cloud owns: Email triage + draft replies + social post drafts/scheduling (draft-only; requires Local approval before send/post)
  Local owns: approvals, WhatsApp session, payments/banking, and final "send/post" actions
  Delegation via Synced Vault (Phase 1)
  Agents communicate by writing files into:
  /Needs_Action/<domain>/, /Plans/<domain>/, /Pending_Approval/<domain>/
  Prevent double-work using:
  /In_Progress/<agent>/ claim-by-move rule
  single-writer rule for Dashboard.md (Local)
  Cloud writes updates to /Updates/ (or /Signals/), and Local merges them into Dashboard.md.
  For Vault sync (Phase 1) use Git (recommended) or Syncthing.
  Claim-by-move rule: first agent to move an item from /Needs_Action to /In_Progress/<agent>/ owns it; other agents must ignore it.
  Security rule: Vault sync includes only markdown/state. Secrets never sync (.env, tokens, WhatsApp sessions, banking creds). So Cloud never stores or uses WhatsApp sessions, banking credentials, or payment tokens.
  Deploy Odoo Community on a Cloud VM (24/7) with HTTPS, backups, and health monitoring; integrate Cloud Agent with Odoo via MCP for draft-only accounting actions and Local approval for posting invoices/payments.
  Optional A2A Upgrade (Phase 2): Replace some file handoffs with direct A2A messages later, while keeping the vault as the audit record
  Platinum demo (minimum passing gate): Email arrivess as the GUI (Graphical User Interface) and Long-Term Memory.
  Dashboard.md: Real-time summary of bank balance, pending messages, and active business projects.
  Company_Handbook.md: Contains your "Rules of Engagement" (e.g., "Always be polite on WhatsApp," "Flag any payment over $500 for my approval").
  The Muscle (Claude Code): Runs in your terminal, pointed at your Obsidian vault. It uses its File System tools to read your tasks and write reports. The Ralph Wiggum loop (a Stop hook) keeps Claude iterating until multi-step tasks are complete.

  2. Architecture: Perception → Reasoning → Action
  A. Perception (The "Watchers")
  Since Claude Code can't "listen" to the internet 24/7, you use lightweight Python Sentinel Scripts running in the background:
  Comms Watcher: Monitors Gmail and WhatsApp (via local web-automation or APIs) and saves new urgent messages as .md files in a /Needs_Action folder.
  Finance Watcher: Downloads local CSVs or calls banking APIs to log new transactions in /Accounting/Current_Month.md.
  It will also be able to run on your laptop and immediately "wake up" as soon as you open your machine.
  Watcher Architecture
  The Watcher layer is your AI Employee's sensory system. These lightweight Python scripts run continuously, monitoring various inputs and creating actionable files for Claude to process.
  Core Watcher Pattern
  All Watchers follow this structure:
  # base_watcher.py - Template for all watchers
  import time
  import logging
  from pathlib import Path
  from abc import ABC, abstractmethod


  class BaseWatcher(ABC):
      def __init__(self, vault_path: str, check_interval: int = 60):
          self.vault_path = Path(vault_path)
          self.needs_action = self.vault_path / 'Needs_Action'
          self.check_interval = check_interval
          self.logger = logging.getLogger(self.__class__.__name__)

      @abstractmethod
      def check_for_updates(self) -> list:
          '''Return list of new items to process'''
          pass

      @abstractmethod
      def create_action_file(self, item) -> Path:
          '''Create .md file in Needs_Action folder'''
          pass

      def run(self):
          self.logger.info(f'Starting {self.__class__.__name__}')
          while True:
              try:
                  items = self.check_for_updates()
                  for item in items:
                      self.create_action_file(item)
              except Exception as e:
                  self.logger.error(f'Error: {e}')
              time.sleep(self.check_interval)
  Gmail Watcher Implementation
  # gmail_watcher.py
  from google.oauth2.credentials import Credentials
  from googleapiclient.discovery import build
  from base_watcher import BaseWatcher
  from datetime import datetime


  class GmailWatcher(BaseWatcher):
      def __init__(self, vault_path: str, credentials_path: str):
          super().__init__(vault_path, check_interval=120)
          self.creds = Credentials.from_authorized_user_file(credentials_path)
          self.service = build('gmail', 'v1', credentials=self.creds)
          self.processed_ids = set()

      def check_for_updates(self) -> list:
          results = self.service.users().messages().list(
              userId='me', q='is:unread is:important'
          ).execute()
          messages = results.get('messages', [])
          return [m for m in messages if m['id'] not in self.processed_ids]

      def create_action_file(self, message) -> Path:
          msg = self.service.users().messages().get(
              userId='me', id=message['id']
          ).execute()

          # Extract headers
          headers = {h['name']: h['value'] for h in msg['payload']['headers']}

          content = f'''---
  type: email
  from: {headers.get('From', 'Unknown')}
  subject: {headers.get('Subject', 'No Subject')}
  received: {datetime.now().isoformat()}
  priority: high
  status: pending
  ---


  ## Email Content
  {msg.get('snippet', '')}


  ## Suggested Actions
  - [ ] Reply to sender
  - [ ] Forward to relevant party
  - [ ] Archive after processing
  '''
          filepath = self.needs_action / f'EMAIL_{message["id"]}.md'
          filepath.write_text(content)
          self.processed_ids.add(message['id'])
          return filepath
  WhatsApp Watcher (Playwright-based)
  Note: This uses WhatsApp Web automation. Be aware of WhatsApp's terms of service.
  # whatsapp_watcher.py
  from playwright.sync_api import sync_playwright
  from base_watcher import BaseWatcher
  from pathlib import Path
  import json


  class WhatsAppWatcher(BaseWatcher):
      def __init__(self, vault_path: str, session_path: str):
          super().__init__(vault_path, check_interval=30)
          self.session_path = Path(session_path)
          self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help']

      def check_for_updates(self) -> list:
          with sync_playwright() as p:
              browser = p.chromium.launch_persistent_context(
                  self.session_path, headless=True
              )
              page = browser.pages[0]
              page.goto('https://web.whatsapp.com')
              page.wait_for_selector('[data-testid="chat-list"]')

              # Find unread messages
              unread = page.query_selector_all('[aria-label*="unread"]')
              messages = []
              for chat in unread:
                  text = chat.inner_text().lower()
                  if any(kw in text for kw in self.keywords):
                      messages.append({'text': text, 'chat': chat})
              browser.close()
              return messages
  File System Watcher (for local drops)
  # filesystem_watcher.py
  from watchdog.observers import Observer
  from watchdog.events import FileSystemEventHandler
  from pathlib import Path
  import shutil


  class DropFolderHandler(FileSystemEventHandler):
      def __init__(self, vault_path: str):
          self.needs_action = Path(vault_path) / 'Needs_Action'

      def on_created(self, event):
          if event.is_directory:
              return
          source = Path(event.src_path)
          dest = self.needs_action / f'FILE_{source.name}'
          shutil.copy2(source, dest)
          self.create_metadata(source, dest)

      def create_metadata(self, source: Path, dest: Path):
          meta_path = dest.with_suffix('.md')
          meta_path.write_text(f'''---
  type: file_drop
  original_name: {source.name}
  size: {source.stat().st_size}
  ---


  New file dropped for processing.
  ''')


  B. Reasoning (Claude Code)
  When the Watcher detects a change, it triggers a Claude command:
  Read: "Check /Needs_Action and /Accounting."
  Think: "I see a WhatsApp message from a client asking for an invoice and a bank transaction showing a late payment fee."
  Plan: Claude creates a Plan.md in Obsidian with checkboxes for the next steps.
  C. Action (The "Hands")
  Model Context Protocol (MCP) servers are Claude Code's hands for interacting with external systems. Each MCP server exposes specific capabilities that Claude can invoke.
  Claude uses custom MCP (Model Context Protocol) servers to act:
  WhatsApp/Social MCP: To send the reply or post the scheduled update.
  Browser/Payment MCP: To log into a payment portal, draft a payment, and stop.
  Human-in-the-Loop (HITL): Claude writes a file: APPROVAL_REQUIRED_Payment_Client_A.md. It will not click "Send" until you move that file to the /Approved folder.
  Recommended MCP Servers
  Server
  Capabilities
  Use Case
  filesystem
  Read, write, list files
  Built-in, use for vault
  email-mcp
  Send, draft, search emails
  Gmail integration
  browser-mcp
  Navigate, click, fill forms
  Payment portals
  calendar-mcp
  Create, update events
  Scheduling
  slack-mcp
  Send messages, read channels
  Team communication


  Claude Code Configuration
  Configure MCP servers in your Claude Code settings:
  // ~/.config/claude-code/mcp.json
  {
    "servers": [
      {
        "name": "email",
        "command": "node",
        "args": ["/path/to/email-mcp/index.js"],
        "env": {
          "GMAIL_CREDENTIALS": "/path/to/credentials.json"
        }
      },
      {
        "name": "browser",
        "command": "npx",
        "args": ["@anthropic/browser-mcp"],
        "env": {
          "HEADLESS": "true"
        }
      }
    ]
  }
  Human-in-the-Loop Pattern
  For sensitive actions, Claude writes an approval request file instead of acting directly:
  # When Claude detects a sensitive action needed:
  # 1. Create approval request file


  # /Vault/Pending_Approval/PAYMENT_Client_A_2026-01-07.md
  ---
  type: approval_request
  action: payment
  amount: 500.00
  recipient: Client A
  reason: Invoice #1234 payment
  created: 2026-01-07T10:30:00Z
  expires: 2026-01-08T10:30:00Z
  status: pending
  ---


  ## Payment Details
  - Amount: $500.00
  - To: Client A (Bank: XXXX1234)
  - Reference: Invoice #1234


  ## To Approve
  Move this file to /Approved folder.


  ## To Reject
  Move this file to /Rejected folder.
  The Orchestrator watches the /Approved folder and triggers the actual MCP action when files appear.
  D. Persistence (The "Ralph Wiggum" Loop)
  Claude Code runs in interactive mode - after processing a prompt, it waits for more input.
  To keep your AI Employee working autonomously until a task is complete, use the
  Ralph Wiggum pattern: a Stop hook that intercepts Claude's exit and feeds the prompt back.

  How Does It Work?

  Orchestrator creates state file with prompt
  Claude works on task
  Claude tries to exit
  Stop hook checks: Is task file in /Done?
  YES → Allow exit (complete)
  NO → Block exit, re-inject prompt, and allow Claude to see its own previous failed output (loop continues).
  Repeat until complete or max iterations

  Usage

    ```bash
    # Start a Ralph loop
    /ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
      --completion-promise "TASK_COMPLETE" \
      --max-iterations 10
  ```

  Two Completion Strategies:
  Promise-based (simple): Claude outputs `<promise>TASK_COMPLETE</promise>`
  File movement (advanced - Gold tier): Stop hook detects when task file moves to /Done
  More reliable (completion is natural part of workflow)
  Orchestrator creates state file programmatically
  See reference implementation for details

  Reference: https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum

  3. Continuous vs. Scheduled Operations
  Operation Type
  Example Task
  Local Trigger
  Scheduled
  Daily Briefing: Summarize business tasks at 8:00 AM.
  cron (Mac/Linux) or Task Scheduler (Win) calls Claude.
  Continuous
  Lead Capture: Watch WhatsApp for keywords like "Pricing."
  Python watchdog script monitoring the /Inbox folder.
  Project-Based
  Q1 Tax Prep: Categorize 3 months of business expenses.
  Manual drag-and-drop of a file into the /Active_Project folder.


  4. Key Hackathon Feature: The "Business Handover"
  One of the coolest features you can add is the Autonomous Business Audit:
  The Trigger: A scheduled task runs every Sunday night.
  The Process: Claude Code reads your Business_Goals.md, checks your Tasks/Done folder for the week, and checks your Bank_Transactions.md.
  The Deliverable: It writes a "Monday Morning CEO Briefing" in Obsidian, highlighting:
  Revenue: Total earned this week.
  Bottlenecks: Tasks that took too long.
  Proactive Suggestion: "I noticed we spent $200 on software we don't use; shall I cancel the subscription?"
  Business Handover Templates
  The Business Handover feature transforms your AI Employee from reactive to proactive. Here are the required templates with explicit schemas.
  Business_Goals.md Template
  # /Vault/Business_Goals.md
  ---
  last_updated: 2026-01-07
  review_frequency: weekly
  ---


  ## Q1 2026 Objectives


  ### Revenue Target
  - Monthly goal: $10,000
  - Current MTD: $4,500


  ### Key Metrics to Track
  | Metric | Target | Alert Threshold |
  |--------|--------|-----------------|
  | Client response time | < 24 hours | > 48 hours |
  | Invoice payment rate | > 90% | < 80% |
  | Software costs | < $500/month | > $600/month |


  ### Active Projects
  1. Project Alpha - Due Jan 15 - Budget $2,000
  2. Project Beta - Due Jan 30 - Budget $3,500


  ### Subscription Audit Rules
  Flag for review if:
  - No login in 30 days
  - Cost increased > 20%
  - Duplicate functionality with another tool
  Weekly Audit Logic
  Claude uses pattern matching to identify subscription usage:
  # audit_logic.py
  SUBSCRIPTION_PATTERNS = {
      'netflix.com': 'Netflix',
      'spotify.com': 'Spotify',
      'adobe.com': 'Adobe Creative Cloud',
      'notion.so': 'Notion',
      'slack.com': 'Slack',
      # Add your common subscriptions
  }


  def analyze_transaction(transaction):
      for pattern, name in SUBSCRIPTION_PATTERNS.items():
          if pattern in transaction['description'].lower():
              return {
                  'type': 'subscription',
                  'name': name,
                  'amount': transaction['amount'],
                  'date': transaction['date']
              }
      return None
  CEO Briefing Template (Generated Output)
  # /Vault/Briefings/2026-01-06_Monday_Briefing.md
  ---
  generated: 2026-01-06T07:00:00Z
  period: 2025-12-30 to 2026-01-05
  ---


  # Monday Morning CEO Briefing


  ## Executive Summary
  Strong week with revenue ahead of target. One bottleneck identified.


  ## Revenue
  - **This Week**: $2,450
  - **MTD**: $4,500 (45% of $10,000 target)
  - **Trend**: On track


  ## Completed Tasks
  - [x] Client A invoice sent and paid
  - [x] Project Alpha milestone 2 delivered
  - [x] Weekly social media posts scheduled


  ## Bottlenecks
  | Task | Expected | Actual | Delay |
  |------|----------|--------|-------|
  | Client B proposal | 2 days | 5 days | +3 days |


  ## Proactive Suggestions


  ### Cost Optimization
  - **Notion**: No team activity in 45 days. Cost: $15/month.
    - [ACTION] Cancel subscription? Move to /Pending_Approval


  ### Upcoming Deadlines
  - Project Alpha final delivery: Jan 15 (9 days)
  - Quarterly tax prep: Jan 31 (25 days)


  ---
  *Generated by AI Employee v0.1*

  5. Tech Stack Summary
  Knowledge Base: Obsidian (Local Markdown).
  Logic Engine: Claude Code (running claude-4-5-opus or any other LLM using Claude Code Router).
  External Integration: MCP Servers (Local Node.js/Python scripts) for Gmail, WhatsApp, and Banking.
  Playwright for "Computer Use" (interacting with websites for payments).
  Automation Glue: A master Python Orchestrator.py that handles the timing and folder watching.


  6. Security & Privacy Architecture
  Security is non-negotiable when building an autonomous system that handles banking, email, and personal communications. This section outlines required security measures.
  6.1 Credential Management
  Never store credentials in plain text or in your Obsidian vault.
  Use environment variables for API keys: export GMAIL_API_KEY="your-key"
  For banking credentials, use a dedicated secrets manager (e.g., macOS Keychain, Windows Credential Manager, or 1Password CLI)
  Create a .env file (add to .gitignore immediately) for local development
  Rotate credentials monthly and after any suspected breach
  Example .env structure:
  # .env - NEVER commit this file
  GMAIL_CLIENT_ID=your_client_id
  GMAIL_CLIENT_SECRET=your_client_secret
  BANK_API_TOKEN=your_token
  WHATSAPP_SESSION_PATH=/secure/path/session
  6.2 Sandboxing & Isolation
  Protect against unintended actions during development:
  Development Mode: Create a DEV_MODE flag that prevents any real external actions
  Dry Run: All action scripts should support a --dry-run flag that logs intended actions without executing
  Separate Accounts: Use test/sandbox accounts for Gmail and banking during development
  Rate Limiting: Implement maximum actions per hour (e.g., max 10 emails, max 3 payments)
  Example dry-run implementation:
  # In any action script
  DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'


  def send_email(to, subject, body):
      if DRY_RUN:
          logger.info(f'[DRY RUN] Would send email to {to}')
          return
      # Actual send logic here
  6.3 Audit Logging
  Every action the AI takes must be logged for review:
  # Required log format
  {
    "timestamp": "2026-01-07T10:30:00Z",
    "action_type": "email_send",
    "actor": "claude_code",
    "target": "client@example.com",
    "parameters": {"subject": "Invoice #123"},
    "approval_status": "approved",
    "approved_by": "human",
    "result": "success"
  }
  Store logs in /Vault/Logs/YYYY-MM-DD.json and retain for a minimum 90 days.
  6.4 Permission Boundaries
  Action Category
  Auto-Approve Threshold
  Always Require Approval
  Email replies
  To known contacts
  New contacts, bulk sends
  Payments
  < $50 recurring
  All new payees, > $100
  Social media
  Scheduled posts
  Replies, DMs
  File operations
  Create, read
  Delete, move outside vault


  7. Error States & Recovery
  Autonomous systems will fail. Plan for it. This section covers common failure modes and recovery strategies.
  7.1 Error Categories
  Category
  Examples
  Recovery Strategy
  Transient
  Network timeout, API rate limit
  Exponential backoff retry
  Authentication
  Expired token, revoked access
  Alert human, pause operations
  Logic
  Claude misinterprets message
  Human review queue
  Data
  Corrupted file, missing field
  Quarantine + alert
  System
  Orchestrator crash, disk full
  Watchdog + auto-restart


  7.2 Retry Logic
  # retry_handler.py
  import time
  from functools import wraps


  def with_retry(max_attempts=3, base_delay=1, max_delay=60):
      def decorator(func):
          @wraps(func)
          def wrapper(*args, **kwargs):
              for attempt in range(max_attempts):
                  try:
                      return func(*args, **kwargs)
                  except TransientError as e:
                      if attempt == max_attempts - 1:
                          raise
                      delay = min(base_delay * (2 ** attempt), max_delay)
                      logger.warning(f'Attempt {attempt+1} failed, retrying in {delay}s')
                      time.sleep(delay)
          return wrapper
      return decorator
  7.3 Graceful Degradation
  When components fail, the system should degrade gracefully:
  Gmail API down: Queue outgoing emails locally, process when restored
  Banking API timeout: Never retry payments automatically, always require fresh approval
  Claude Code unavailable: Watchers continue collecting, queue grows for later processing
  Obsidian vault locked: Write to temporary folder, sync when available
  7.4 Watchdog Process
  # watchdog.py - Monitor and restart critical processes
  import subprocess
  import time
  from pathlib import Path


  PROCESSES = {
      'orchestrator': 'python orchestrator.py',
      'gmail_watcher': 'python gmail_watcher.py',
      'file_watcher': 'python filesystem_watcher.py'
  }


  def check_and_restart():
      for name, cmd in PROCESSES.items():
          pid_file = Path(f'/tmp/{name}.pid')
          if not is_process_running(pid_file):
              logger.warning(f'{name} not running, restarting. Rules
  Individual
  All code must be original or properly attributed open-source
  Must use Claude Code as the primary reasoning engine
  Projects must include documentation and a demo video
  Ethics & Responsible Automation
  With great automation comes great responsibility. Consider these principles as you build.
  When Should AI NOT Act Autonomously?
  Emotional contexts: Condolence messages, conflict resolution, sensitive negotiations
  Legal matters: Contract signing, legal advice, regulatory filings
  Medical decisions: Health-related actions affecting you or others
  Financial edge cases: Unusual transactions, new recipients, large amounts
  Irreversible actions: Anything that cannot be easily undone
  Transparency Principles
  Disclose AI involvement: When your AI sends emails, consider adding a signature noting AI assistance
  Maintain audit trails: All actions should be logged and reviewable
  Allow opt-out: Give contacts a way to request human-only communication
  Regular reviews: Schedule weekly reviews of AI decisions to catch drift
  Privacy Considerations
  Minimize data collection: Only capture what's necessary
  Local-first: Keep sensitive data on your machine when possible
  Encryption at rest: Consider encryptiian.
  HITL Safety: Sophisticated file-based approval system prevents AI accidents.

  Note for Developers: Why "Watchers" Need Process Management
  In the proposed architecture, your "Watchers" (Gmail, WhatsApp listeners) are essentially daemon processes. They are designed to run indefinitely to poll for events1.
  However, standard Python scripts invoked via terminal (e.g., python watcher.py) are fragile:
  They terminate if the TTY/SSH session closes.
  They crash on unhandled exceptions (e.g., transient API timeouts).
  They do not auto-recover after a system reboot.
  "Process Management" solves this by wrapping your scripts in a supervisor that ensures state persistence.
  The Problem: Script Fragility
  If you run python gmail_watcher.py and your internet blips for 5 seconds, the script throws an exception and exits. Your AI employee is now "dead" until you manually SSH in and restart it.
  The Solution: A Process Manager (PM)
  A PM (like PM2, supervisord, or Systemd) acts as a watchdog. It daemonizes your script and monitors its PID.
  Auto-Restart: If the process exits with a non-zero code (crash), the PM immediately restarts it2.


  Startup Persistence: It hooks into the OS init system (e.g., systemd on Linux) to launch the script on boot3.


  Logging: It captures stdout/stderr to log files, which is critical for debugging silent failures over long periods.
  Quick Recommendation:
  For this hackathon, PM2 is often the easiest developer-friendly tool (originally for Node, but handles Python perfectly):

  # Install PM2
  npm install -g pm2

  # Start your watcher and keep it alive forever
  pm2 start gmail_watcher.py --interpreter python3

  # Freeze this list to start on reboot
  pm2 save
  pm2 startup


  Alternatively, the hackathon document suggests writing a custom Python "Watchdog" script that loops and checks PIDs, effectively building a primitive process manager yourself.
response_text: |
  Created a comprehensive constitution for the Personal AI Employee project based on the hackathon document. The constitution includes six core principles: Local-First Architecture, Human-in-the-Loop Safety, Modularity Through Agent Skills, Persistent Watcher Architecture, Obsidian-Centric Workflow, and Security-First Design. It also defines additional constraints, development workflow, and governance rules aligned with the hackathon requirements.
outcome: success
evaluation: []
---

# Personal AI Employee Constitution - Constitution Update Summary

## Overview
Updated the project constitution to align with the Personal AI Employee Hackathon requirements, focusing on creating a digital FTE (Full-Time Equivalent) that operates as an autonomous agent managing personal and business affairs.

## Key Changes Made
- Defined six core principles reflecting the hackathon's architecture and design goals
- Established local-first architecture as a fundamental requirement
- Emphasized human-in-the-loop safety mechanisms
- Mandated modularity through Agent Skills
- Required persistent watcher architecture for continuous monitoring
- Implemented Obsidian-centric workflow for transparency
- Enforced security-first design principles
- Created governance structure aligned with tiered development approach (Bronze/Silver/Gold/Platinum)

## Compliance Verification
- ✅ All hackathon requirements incorporated
- ✅ Security and privacy considerations addressed
- ✅ Human-in-the-loop safety mechanisms specified
- ✅ Modularity and reusability emphasized
- ✅ Local-first architecture prioritized
- ✅ Obsidian integration as central hub established