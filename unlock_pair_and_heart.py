#!/usr/bin/env python3
"""
Unlocker for:
1. Heart On Your Sleeve (25 reactions on issues/PRs)
2. Pair Extraordinaire (Co-authored commits via standard merge PRs)
"""
import subprocess
import requests
import time
import sys
from datetime import datetime

REPO_OWNER = "YOUR_GITHUB_USERNAME"  # Ganti dengan username GitHub lo
REPO_NAME = "YOUR_REPO_NAME"  # Ganti dengan nama repository target
REPO_PATH = r"C:\path\to\your\repo"  # Path lokal ke repository

# WAJIB: Hadi selalu jadi co-author utama di setiap commit lo!
HADI_CO_AUTHOR = ("Hadi-Akram-Ramadhan", "kk.hadi.akram@gmail.com")

# Real, verified GitHub accounts for co-authorship
REAL_CO_AUTHORS = [
    HADI_CO_AUTHOR,  # Hadi WAJIB di setiap commit
    ("The Octocat", "octocat@github.com"),
    ("GitHub Actions", "actions@github.com"),
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

def unlock_heart_on_your_sleeve(token):
    print("\n❤️ Unlocking Heart On Your Sleeve (25 reactions)...")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    # Get list of issues in repo
    r = requests.get(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=all&per_page=30", headers=headers)
    issues = r.json()

    if not isinstance(issues, list) or len(issues) == 0:
        print("  ⚠️ No issues found, creating 25 issues for reactions...")
        issues = []
        for i in range(25):
            cr = requests.post(
                f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues",
                headers=headers,
                json={"title": f"Community feedback #{i+1}", "body": "Tracking community reactions."}
            )
            if cr.status_code == 201:
                issues.append(cr.json())
            time.sleep(0.5)

    reaction_count = 0
    emojis = ["+1", "heart", "rocket", "eyes", "hooray"]

    for i, issue in enumerate(issues[:25]):
        issue_number = issue.get("number")
        if not issue_number:
            continue

        emoji = emojis[i % len(emojis)]
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/reactions"
        res = requests.post(url, headers=headers, json={"content": emoji})

        if res.status_code in [200, 201]:
            reaction_count += 1
            print(f"  ✨ Reacted with {emoji} on #{issue_number} [{reaction_count}/25]")
        else:
            print(f"  ❌ Reaction failed on #{issue_number}: {res.status_code}")

        time.sleep(0.3)

    print(f"✅ Heart On Your Sleeve completed: {reaction_count} reactions sent!")

def unlock_pair_extraordinaire(token):
    print("\n👥 Unlocking Pair Extraordinaire (Co-authored merge PRs)...")
    headers = {"Authorization": f"token {token}"}

    run_git(["checkout", "-f", "main"])
    run_git(["pull", "origin", "main"])

    # Create 3 PRs with standard merge commit preserving co-author trailers
    for i in range(3):
        name, email = REAL_CO_AUTHORS[i % len(REAL_CO_AUTHORS)]
        branch_name = f"feat/pair-collab-{i+1:02d}"

        run_git(["checkout", "-B", branch_name, "main"])

        # Make a dummy change
        test_file = f"{REPO_PATH}/src/collab_{i+1:02d}.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(f"Pair collaboration with {name}\nTimestamp: {datetime.now().isoformat()}\n")

        run_git(["add", test_file])

        commit_msg = f"feat: implement collaborative module #{i+1}\n\nCo-authored-by: {name} <{email}>"
        run_git(["commit", "-m", commit_msg])

        run_git(["push", "--force", "-u", "origin", branch_name])

        # Create PR
        pr_data = {
            "title": f"feat: collaborative feature #{i+1} with {name}",
            "head": branch_name,
            "base": "main",
            "body": f"Pair programming module.\n\nCo-authored-by: {name} <{email}>\n\n---\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"
        }

        pr_res = requests.post(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls", headers=headers, json=pr_data)
        if pr_res.status_code != 201:
            print(f"  ❌ PR creation failed: {pr_res.text[:80]}")
            continue

        pr_number = pr_res.json()["number"]
        time.sleep(1.0)

        # STANDARD MERGE (Preserves git history & co-author trailers intact!)
        merge_res = requests.put(
            f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/merge",
            headers=headers,
            json={
                "merge_method": "merge",
                "commit_message": f"Co-authored-by: {name} <{email}>"
            }
        )

        if merge_res.status_code == 200:
            print(f"  ✅ PR #{pr_number} merged with co-author: {name} <{email}>")
            # Delete remote branch
            requests.delete(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/heads/{branch_name}", headers=headers)
        else:
            print(f"  ❌ Merge failed on PR #{pr_number}: {merge_res.status_code}")

        run_git(["checkout", "-f", "main"])
        run_git(["pull", "origin", "main"])
        run_git(["branch", "-D", branch_name], check=False)
        time.sleep(1.0)

    print("✅ Pair Extraordinaire co-authored PRs merged successfully!")

def main():
    print("🚀 Unlocking Extra Achievements")
    print("=" * 50)
    token = get_github_token()
    print("✅ Token retrieved")

    unlock_heart_on_your_sleeve(token)
    unlock_pair_extraordinaire(token)

    print("\n" + "=" * 50)
    print("🎉 All tasks finished! Check https://github.com/Hadi-Akram-Ramadhan?tab=achievements")

if __name__ == "__main__":
    main()
