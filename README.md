# checkout-demo

A small checkout service (cart, coupons, shipping, tax and order history) used to demo [ci-fix-agent-mcp](https://github.com/vicdevman/ci-fix-agent-mcp): an AI agent that fixes failing CI builds.

`main` is green. Each demo branch is one plausible commit that breaks the tests in a different way:

| Branch | What breaks |
|---|---|
| `refactor/order-history-pagination` | Page 1 of order history skips the newest orders |
| `refactor/simplify-order-total` | Tax is charged before the coupon discount |
| `chore/shipping-threshold-cleanup` | An order of exactly $50.00 is charged shipping |
| `perf/skip-string-conversion` | Float amounts round to the wrong cent |
| `refactor/rename-coupon-helper` | A rename leaves callers using the old name |

Open a PR from any branch. CI fails, the **CI triage** workflow starts automatically, and the agent comments on the PR with the root cause, a patch and before/after test results.

## Setup

1. Add a repository secret `GEMINI_API_KEY` (Settings → Secrets and variables → Actions).
2. Settings → Actions → General → Workflow permissions: allow read and write.

Run the tests locally:

```bash
pip install pytest
pytest -q
```
