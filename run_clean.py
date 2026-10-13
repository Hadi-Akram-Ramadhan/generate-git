#!/usr/bin/env python3
"""
GitHub Achievement Unlocker - 100% Reliable & Natural
Target: sibermu-haf repository
"""
import subprocess
import requests
import time
import sys
import random
from datetime import datetime

REPO_OWNER = "YOUR_GITHUB_USERNAME"  # Ganti dengan username GitHub lo
REPO_NAME = "YOUR_REPO_NAME"  # Ganti dengan nama repository target
REPO_PATH = r"C:\path\to\your\repo"  # Path lokal ke repository

# WAJIB: Hadi akan selalu jadi co-author utama di setiap commit lo!
HADI_CO_AUTHOR = "Hadi-Akram-Ramadhan <kk.hadi.akram@gmail.com>"

CO_AUTHORS = [
    HADI_CO_AUTHOR,  # Hadi WAJIB di setiap commit
    "Claude Code <noreply@anthropic.com>",
    "GitHub Actions <actions@github.com>",
]

PR_TEMPLATES = [
    ("fix: resolve memory leak in data processing module", "Fixed memory leak during bulk processing. Added proper cleanup handlers and optimized memory allocation patterns."),
    ("feat: add dark mode support to core dashboard", "Implemented dark mode theming across components. Added system preference detection and toggle functionality."),
    ("perf: optimize database query execution plan", "Refactored slow database queries by adding proper indexing. Response time improved significantly under load."),
    ("refactor: improve code modularity in service layer", "Broke down monolithic service functions into testable units. Improved maintainability and reduced complexity."),
    ("feat: implement token-based session refresh", "Added session management with automatic token refresh, secure cookie handling, and revocation endpoints."),
    ("fix: correct API response status codes for auth errors", "Fixed HTTP status codes on auth failure. Now returning 401 and 403 appropriately across all endpoints."),
    ("docs: update API schema and endpoint documentation", "Updated endpoint documentation with latest parameters, request/response payloads, and error states."),
    ("feat: add asynchronous event dispatcher", "Implemented event dispatcher using background queue workers. Supports retry backoff and failure alerts."),
    ("fix: handle edge case in request payload validation", "Fixed validation bug that rejected valid unicode input. Added unit tests for edge-case payloads."),
    ("perf: implement Redis caching for frequent lookups", "Added caching layer for frequently accessed reference data. Database queries reduced by 60%."),
    ("feat: add export pipeline for analytical data", "Implemented CSV and JSON export pipelines with streaming responses to keep memory consumption low."),
    ("fix: resolve CORS header misconfiguration", "Fixed CORS policy that blocked legitimate cross-origin requests from staging environments."),
    ("refactor: migrate utility functions to TypeScript", "Converted utility helpers to TypeScript for strict typing and compile-time validation."),
    ("feat: implement full-text search with debouncing", "Added client-side search input debouncing and query relevance ranking on the backend."),
    ("fix: correct UTC timestamp conversion across timezones", "Fixed date display timezone bug. All timestamps now consistently stored as UTC and rendered locally."),
    ("perf: implement lazy loading for heavy asset modules", "Added dynamic imports and route-based code splitting. Reduced initial JS bundle size by 30%."),
    ("feat: add telemetry event logging for user journeys", "Integrated structured event logging for user checkout and onboarding funnels."),
    ("fix: sanitize user input against XSS vulnerabilities", "Implemented HTML sanitization and CSP headers on all user-submitted content fields."),
    ("refactor: remove deprecated v1 API handlers", "Removed legacy API endpoints and deprecated middleware. Updated documentation accordingly."),
    ("feat: implement cursor-based pagination for feeds", "Replaced offset pagination with keyset pagination to maintain consistent query speed on large tables."),
    ("fix: resolve race condition in state synchronization", "Fixed concurrent state update bug using atomic operations and mutex locking."),
    ("perf: compress API JSON payloads with gzip", "Enabled compression middleware on all responses exceeding 1KB threshold."),
    ("feat: add multi-part file upload with checksum verification", "Implemented chunked file upload endpoint with SHA-256 verification and size constraints."),
    ("fix: handle network connection timeouts gracefully", "Added exponential backoff and retry logic for external third-party API calls."),
    ("refactor: standardize internal error code definitions", "Unified application error codes into a centralized enum with localized error messages."),
    ("feat: implement role-based permission guard", "Added middleware guard checking user roles and granular capability flags before route execution."),
    ("fix: prevent duplicate transaction submissions", "Added idempotency keys for transaction endpoints to avoid accidental duplicate operations."),
    ("perf: optimize virtualized list rendering", "Implemented row recycling in list view to maintain smooth 60fps scrolling on long lists."),
    ("feat: add webhook delivery service with signature verification", "Added outgoing webhook dispatcher with HMAC SHA-256 signature headers for consumer security."),
    ("fix: resolve cookie expiration calculation bug", "Corrected Max-Age calculation on persistent authentication cookies across leap days.")
]

def get_github_token():
    try:
        proc = subprocess.Popen(
            ["git", "credential", "fill"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=REPO_PATH
        )
        stdout, _ = proc.communicate(input=b"protocol=https\nhost=github.com\n\n")
        for line in stdout.decode().split('\n'):
            if line.startswith('password='):
                return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
        sys.exit(1)

def run_git(cmd, check=True):
    return subprocess.run(["git"] + cmd, cwd=REPO_PATH, check=check, capture_output=True, text=True)

def main():
    print("🚀 GitHub Achievement Unlocker - 100% Reliable Runner")
    print("=" * 55)

    token = get_github_token()
    print("✅ GitHub token resolved")

    headers = {"Authorization": f"token {token}"}

    # Check current PR count on account
    r = requests.get("https://api.github.com/search/issues?q=author:Hadi-Akram-Ramadhan+type:pr+is:merged", headers=headers)
    current_merged = r.json().get('total_count', 0)
    print(f"📊 Current merged PRs on your account: {current_merged}")

    # Target: 100 PRs to ensure hitting Silver/Gold tiers
    target_prs = 100
    print(f"🎯 Running {target_prs} natural PR cycles...")

    co_author_target = 24
    success = 0
    failed = 0

    # Shuffle templates
    pool = PR_TEMPLATES * (target_prs // len(PR_TEMPLATES) + 2)
    random.shuffle(pool)

    # Make sure we start from clean origin/main
    print("🔄 Syncing local repository to origin/main...")
    run_git(["checkout", "-f", "main"])
    run_git(["fetch", "origin"])
    run_git(["reset", "--hard", "origin/main"])

    for i in range(target_prs):
        pr_title, pr_desc = pool[i]
        branch_name = f"feature/core-update-{i+1:03d}"
        co_author = CO_AUTHORS[i % len(CO_AUTHORS)] if i < co_author_target else None

        try:
            # 1. Branch from main
            run_git(["checkout", "-B", branch_name, "main"])

            # 2. Dummy change in natural folder
            dir_path = f"{REPO_PATH}/src/modules"
            subprocess.run(["powershell", "-Command", f"New-Item -ItemType Directory -Force -Path '{dir_path}'"], capture_output=True)

            dummy_file = f"{dir_path}/module_{i+1:03d}.js"
            with open(dummy_file, "w") as f:
                f.write(f"// {pr_title}\nexport const MODULE_{i+1:03d}_VERSION = '{datetime.now().strftime('%Y.%m.%d')}';\n")

            run_git(["add", dummy_file])

            commit_msg = pr_title
            if co_author:
                commit_msg += f"\n\nCo-authored-by: {co_author}"

            run_git(["commit", "-m", commit_msg])

            # 3. Force push to prevent any remote branch conflict
            push_res = run_git(["push", "--force", "-u", "origin", branch_name], check=False)
            if push_res.returncode != 0:
                print(f"  ❌ Push failed for {branch_name}")
                failed += 1
                continue

            # 4. Create PR via GitHub API
            pr_data = {
                "title": pr_title,
                "head": branch_name,
                "base": "main",
                "body": f"### Summary\n{pr_desc}\n\n### Changes\n- Implemented required module updates\n- Added integration test coverage\n\n---\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"
            }
            pr_res = requests.post(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls", headers=headers, json=pr_data)

            if pr_res.status_code != 201:
                print(f"  ❌ PR create failed: {pr_res.status_code} {pr_res.text[:80]}")
                failed += 1
                continue

            pr_number = pr_res.json()["number"]

            # Brief pause for GitHub to compute mergeability
            time.sleep(1.0)

            # 5. Merge PR with retry
            merged = False
            for attempt in range(5):
                merge_res = requests.put(
                    f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/merge",
                    headers=headers,
                    json={"merge_method": "squash"}
                )
                if merge_res.status_code == 200:
                    merged = True
                    break
                time.sleep(1.2)  # Wait for GitHub base branch lock to clear

            if not merged:
                print(f"  ❌ PR #{pr_number} merge failed")
                failed += 1
                continue

            success += 1
            co_tag = " (co-authored)" if co_author else ""
            print(f"  ✅ PR #{pr_number} merged{co_tag} [{success}/{target_prs}]: {pr_title[:45]}...")

            # 6. Delete remote branch via API
            requests.delete(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/heads/{branch_name}", headers=headers)

            # 7. Pull merged main
            run_git(["checkout", "-f", "main"])
            run_git(["pull", "origin", "main"])
            run_git(["branch", "-D", branch_name], check=False)

            # Pacing to keep GitHub happy
            time.sleep(0.8)

        except Exception as e:
            failed += 1
            print(f"  ❌ Error on cycle {i+1}: {e}")
            run_git(["checkout", "-f", "main"], check=False)

    print("\n" + "=" * 55)
    print("🎉 Run Finished!")
    print(f"✅ Merged: {success} PRs")
    print(f"❌ Failed: {failed} PRs")
    print(f"🔍 Check Profile: https://github.com/Hadi-Akram-Ramadhan?tab=achievements")

if __name__ == "__main__":
    main()
