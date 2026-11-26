# 4. Git/GitHub workflow – do this yourself (the rubric checks YOUR history)

## Setup
```bash
git init && git add . && git commit -m "chore: initial project skeleton"
git branch -M main
git remote add origin https://github.com/<you>/campus-events.git
git push -u origin main
```

## TDD cycle (do it for real, one commit per step so history proves it)
`test(pricing): add failing test for student discount` -> `feat(pricing): implement StudentDiscount` -> `refactor(pricing): extract choose_strategy`.
Tip: delete one module (e.g. EarlyBird) and its tests, then re-create them test-first on a branch.

## Suggested branches / PRs
1. `feature/user-module` -> PR, review, **accepted**
2. `feature/event-factory` -> PR, reviewer requests change ("validate capacity"), you revise, accepted
3. `feature/pricing-strategy` -> PR **rejected/closed** (e.g. first version hard-coded discounts), reopen as `feature/pricing-strategy-v2`
4. `feature/payment-adapter`, `feature/observer-notifications`, `docs/openapi`, `ci/github-actions`
Ask a classmate to review (or use two GitHub accounts) – leave real review comments.

## Create a genuine merge conflict (and document it)
```bash
git checkout -b feature/fee-change main
# edit app/factory.py: change workshop fee 200.0 -> 250.0; commit
git checkout -b feature/capacity-change main
# edit the SAME line: workshop fee 200.0 -> 180.0, capacity 40 -> 50; commit
git checkout main && git merge feature/fee-change
git merge feature/capacity-change     # CONFLICT in app/factory.py
# open file, keep the agreed value, remove <<<<<<< ======= >>>>>>> markers
python -m pytest && git add app/factory.py && git commit
```
Report note: which lines conflicted, how you decided the final value, and that tests passed after resolving.
Screenshots to take: branch graph, PR with review, conflict markers, green CI run, coverage output.
