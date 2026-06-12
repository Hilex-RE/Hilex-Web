"""
Morning Focus autopilot — pulls Google Tasks + Compass inbox via Composio,
asks Claude to write the brief, emails it to michael.abraham@compass.com.

ONE-TIME SETUP (Michael):
1. composio.dev → create free account → connect Gmail (compass) + Google Tasks
2. Repo Settings > Secrets > Actions: add ANTHROPIC_API_KEY and COMPOSIO_API_KEY
The script auto-discovers your connected account IDs.
Replies are NEVER sent by this script — only the brief, to your own address.
"""
import os, json, requests

CKEY = os.environ["COMPOSIO_API_KEY"]
AKEY = os.environ["ANTHROPIC_API_KEY"]
CBASE = "https://backend.composio.dev/api/v3"
CH = {"x-api-key": CKEY, "Content-Type": "application/json"}
ME = "michael.abraham@compass.com"

def accounts():
    r = requests.get(f"{CBASE}/connected_accounts", headers=CH, timeout=30).json()
    out = {}
    for a in r.get("items", r if isinstance(r, list) else []):
        slug = (a.get("toolkit") or {}).get("slug") or a.get("appName", "")
        if a.get("status", "").upper() == "ACTIVE":
            out.setdefault(slug.lower(), a.get("id"))
    return out

def execute(slug, args, account_id):
    r = requests.post(f"{CBASE}/tools/execute/{slug}", headers=CH, timeout=120,
        json={"connected_account_id": account_id, "arguments": args})
    r.raise_for_status()
    return r.json().get("data", {})

def main():
    acc = accounts()
    tasks = execute("GOOGLETASKS_LIST_ALL_TASKS",
        {"max_tasks_total": 500, "showCompleted": False}, acc["googletasks"])
    emails = execute("GMAIL_FETCH_EMAILS",
        {"max_results": 25, "query": "in:inbox newer_than:1d", "user_id": "me"}, acc["gmail"])

    # Trim email payloads for the prompt
    slim = [{"from": m.get("sender"), "subject": m.get("subject"),
             "preview": (m.get("preview") or {}).get("body", "")[:200]}
            for m in emails.get("messages", [])]
    slim_tasks = [{"list": t.get("tasklist_title"), "title": t.get("title"),
                   "due": (t.get("due") or "")[:10]} for t in tasks.get("tasks", [])]

    prompt = f"""You are Michael's Chief of Staff. Build today's Morning Focus brief.
RULES: $250K AMRE weights highest BUT any goal with a deadline within 14 days ranks #1
(Nueva Vista lists 2026-06-26, closes ~2026-08-10). THE 3 = top three only-Michael-can-do
items, hard cap 3. Sections: Nueva Vista countdown capsule, wins, Constraint (one line),
THE 3, From your inboxes (NEEDS-ACTION only, skip newsletters/marketing), Plus one each
(health/family/hottest project), Buy Back (delegate/automate), Winning today (one sentence),
button to https://hilex.io/dashboard/os/.
STYLE: Apple email — table layout, inline CSS only, white cards on #F5F5F7, system font stack,
rounded 14px cards, red countdown capsule, green win/winning capsules. Max 600px wide.
Return ONLY JSON: {{"subject": "...", "html": "..."}} — no markdown fences.

GOOGLE TASKS: {json.dumps(slim_tasks)[:14000]}
LAST 24H COMPASS INBOX: {json.dumps(slim)[:10000]}"""

    a = requests.post("https://api.anthropic.com/v1/messages", timeout=300,
        headers={"x-api-key": AKEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-4-6", "max_tokens": 8000,
              "messages": [{"role": "user", "content": prompt}]})
    a.raise_for_status()
    text = "".join(b.get("text", "") for b in a.json()["content"] if b.get("type") == "text")
    brief = json.loads(text.replace("```json", "").replace("```", "").strip())

    execute("GMAIL_SEND_EMAIL", {"recipient_email": ME, "subject": brief["subject"],
        "body": brief["html"], "is_html": True, "user_id": "me"}, acc["gmail"])
    print("Brief sent:", brief["subject"])

if __name__ == "__main__":
    main()
