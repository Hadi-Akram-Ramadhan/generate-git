#!/usr/bin/env python3
"""
Galaxy Brain Gold Unlocker (32 Accepted Answers via Discussions)
Helper Account: hadooyy90-afkrere
Main Account: Hadi-Akram-Ramadhan
Target Repo: sibermu-haf
"""
import subprocess
import requests
import time
import sys

REPO_ID = "YOUR_REPO_ID"  # GraphQL Node ID dari repo target
QA_CATEGORY_ID = "YOUR_QA_CATEGORY_ID"  # ID kategori Q&A dari Discussions
HELPER_TOKEN = "ghp_YOUR_HELPER_TOKEN"  # PAT akun helper/collaborator
REPO_PATH = r"C:\path\to\your\repo"  # Path lokal ke repo target

DISCUSSIONS_QA = [
    ("How to optimize SQL query indexing for large tables?", "Use compound indexes covering frequent WHERE and JOIN columns. Run EXPLAIN ANALYZE to verify execution plans."),
    ("Best practice for JWT token expiration?", "Set short access token lifespan (15m) with refresh token rotation stored in HttpOnly cookies."),
    ("How to prevent race conditions in payment gateways?", "Implement distributed locks via Redis or database row-level locking (SELECT FOR UPDATE) combined with idempotency keys."),
    ("What is the difference between debounce and throttle?", "Debounce delays execution until after a specified silence duration, while throttle ensures execution at most once per interval."),
    ("How to handle WebSocket disconnections gracefully?", "Implement exponential backoff reconnect logic on the client, with heartbeats/ping-pong to detect dead connections early."),
    ("When should you choose PostgreSQL over MySQL?", "PostgreSQL excels with complex queries, JSONB indexing, custom extensions, and strict ACID compliance in heavy analytics."),
    ("How does connection pooling improve database performance?", "It reuses existing established connections instead of opening/closing TCP handshakes for every request, reducing server latency."),
    ("What is the advantage of using Redis caching?", "In-memory key-value storage offers sub-millisecond read speeds, reducing load on relational databases for read-heavy operations."),
    ("How to avoid memory leaks in Node.js event listeners?", "Always call removeListener or use AbortController when components unmount, and monitor heap snapshots using Chrome DevTools."),
    ("How to implement CORS security properly?", "Whitelist specific allowed origins rather than using wildcard *, and restrict allowed methods and headers explicitly."),
    ("What are idempotency keys in REST APIs?", "Unique client-generated tokens preventing duplicate request execution if a network timeout triggers a retry."),
    ("How to optimize Docker image sizes for production?", "Use multi-stage builds, minimal base images (like Alpine or distroless), and avoid caching package manager layers."),
    ("What is database sharding and when is it needed?", "Horizontal partitioning of database data across multiple servers when a single node cannot handle storage or write concurrency."),
    ("How to secure API endpoints against rate-limit abuse?", "Use token bucket or sliding window rate limiters in reverse proxies (e.g. Nginx, Cloudflare) or middleware with Redis counters."),
    ("What is the difference between soft delete and hard delete?", "Soft delete flags records as deleted using timestamps for audit/recovery, whereas hard delete permanently removes rows from disk."),
    ("How does a reverse proxy like Nginx handle load balancing?", "Distributes incoming traffic across upstream backend servers using algorithms like round-robin, least-connections, or ip-hash."),
    ("How to write reliable unit tests with mocks?", "Mock external I/O boundaries (APIs, databases) while asserting pure business logic behavior without testing implementation details."),
    ("What is circuit breaker pattern in microservices?", "Prevents cascading failures by stopping calls to a failing downstream service once a failure threshold is crossed."),
    ("How to properly hash user passwords?", "Use modern adaptive hashing algorithms like Argon2id or bcrypt with appropriate salt and cost factors."),
    ("What is zero-downtime deployment?", "Deploying new code without interrupting active traffic using blue-green deployments or rolling container updates behind a load balancer."),
    ("How does GraphQL solve over-fetching and under-fetching?", "Clients request exact field shapes in a single query, preventing over-fetching large payloads or making multiple round-trips."),
    ("What is the purpose of database migrations?", "Version control for database schema changes ensuring deterministic environment parity across dev, staging, and production."),
    ("How to handle background asynchronous queues?", "Use dedicated message brokers like RabbitMQ or Redis BullMQ to offload slow tasks from HTTP request lifecycles."),
    ("What is event-driven architecture?", "Services communicate by emitting and reacting to events asynchronously, enabling loose coupling and independent scalability."),
    ("How to prevent SQL injection in modern ORMs?", "Always use parameterized queries and avoid manual raw string concatenation within query builders."),
    ("What is the role of an API Gateway?", "Central entry point handling cross-cutting concerns: authentication, rate limiting, telemetry, and request routing."),
    ("How to structure modular monolith applications?", "Group code by domain boundaries rather than technical layers, keeping communication between modules clean and decoupled."),
    ("What is optimistic concurrency control?", "Allows concurrent updates by checking record version columns before write commits, aborting if conflicts occur."),
    ("How does gzip/brotli compression speed up web responses?", "Compresses text-based responses (HTML, CSS, JSON) by up to 70% before network transmission, reducing download latency."),
    ("What are the advantages of HTTP/2 over HTTP/1.1?", "Multiplexing multiple requests over a single TCP connection, header compression (HPACK), and server push capabilities."),
    ("How to monitor application latency and errors in real-time?", "Collect structured telemetry via APM tools (e.g., Sentry, Prometheus, Datadog) to alert on error rates and p99 latency spikes."),
    ("Why use semantic versioning (SemVer) for libraries?", "Provides predictable change expectations (MAJOR.MINOR.PATCH) for consumers to manage dependencies safely.")
]

def get_main_token():
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
        print(f"❌ Failed to get main token: {e}")
        sys.exit(1)

def run_graphql(token, query, variables=None):
    headers = {"Authorization": f"token {token}"}
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    res = requests.post("https://api.github.com/graphql", headers=headers, json=payload)
    return res.json()

def main():
    print("🧠 Starting Galaxy Brain Gold Unlocker")
    print("=" * 55)
    main_token = get_main_token()
    print("✅ Main token retrieved")
    print("✅ Helper token configured")

    # Target 32 questions for GOLD tier
    total = len(DISCUSSIONS_QA)
    print(f"🎯 Target: {total} accepted answers (Galaxy Brain Gold)\n")

    success = 0

    for i, (question, answer) in enumerate(DISCUSSIONS_QA):
        title = f"[Q&A] {question}"
        body = f"Hello team,\n\n{question}\nLooking for best practices.\n\nThanks!"

        # 1. Helper creates discussion in Q&A category
        create_disc_mutation = """
        mutation CreateDisc($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
          createDiscussion(input: {repositoryId: $repoId, categoryId: $catId, title: $title, body: $body}) {
            discussion {
              id
              number
            }
          }
        }
        """
        disc_res = run_graphql(HELPER_TOKEN, create_disc_mutation, {
            "repoId": REPO_ID,
            "catId": QA_CATEGORY_ID,
            "title": title,
            "body": body
        })

        disc = disc_res.get("data", {}).get("createDiscussion", {}).get("discussion")
        if not disc:
            print(f"  ❌ Failed to create discussion {i+1}: {disc_res}")
            continue

        disc_id = disc["id"]
        disc_num = disc["number"]
        time.sleep(0.5)

        # 2. Main account answers the discussion
        answer_body = f"Here is the recommended approach:\n\n{answer}\n\nHope this helps!"
        add_comment_mutation = """
        mutation AddComment($discId: ID!, $body: String!) {
          addDiscussionComment(input: {discussionId: $discId, body: $body}) {
            comment {
              id
            }
          }
        }
        """
        comment_res = run_graphql(main_token, add_comment_mutation, {
            "discId": disc_id,
            "body": answer_body
        })

        comment = comment_res.get("data", {}).get("addDiscussionComment", {}).get("comment")
        if not comment:
            print(f"  ❌ Failed to post answer for #{disc_num}: {comment_res}")
            continue

        comment_id = comment["id"]
        time.sleep(0.5)

        # 3. Helper marks main account's answer as Accepted Answer
        mark_answer_mutation = """
        mutation MarkAnswer($commentId: ID!) {
          markDiscussionCommentAsAnswer(input: {id: $commentId}) {
            discussion {
              id
              answer {
                id
              }
            }
          }
        }
        """
        mark_res = run_graphql(HELPER_TOKEN, mark_answer_mutation, {
            "commentId": comment_id
        })

        ans_check = mark_res.get("data", {}).get("markDiscussionCommentAsAnswer", {}).get("discussion", {}).get("answer")
        if ans_check:
            success += 1
            print(f"  ✨ Accepted answer #{success}/{total} on Discussion #{disc_num} (Gold Tier)")
        else:
            print(f"  ❌ Failed to mark answer on #{disc_num}: {mark_res}")

        time.sleep(0.8)

    print("\n" + "=" * 55)
    print("🎉 Galaxy Brain Gold Unlock Completed!")
    print(f"✅ Total Accepted Answers: {success}/{total}")
    print("⏳ Profile badge will update on next GitHub indexing cycle.")

if __name__ == "__main__":
    main()
