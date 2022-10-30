# Reviewing:

This is the checklist that I try to go through for every single pull request that I get. If you're wondering why it takes so long for me to accept pull requests, this is why.

## General

- [ ] Is this change useful to me, or something that I think will benefit others greatly?
- [ ] Check for overlap with other PRs.
- [ ] Think carefully about the long-term implications of the change. How will it affect existing projects that are dependent on this? How will it affect my projects? If this is complicated, do I really want to maintain it forever? Is there any way it could be implemented as a separate package, for better modularity and flexibility?

## Check the Code

- [ ] If it does too much, ask for it to be broken up into smaller PRs.
- [ ] Does it pass `make test-style` (flake8, etc.)?
- [ ] Is it consistent?
- [ ] Review the changes carefully, line by line. Make sure you understand every single part of every line. Learn whatever you do not know yet.
- [ ] Take the time to get things right. PRs almost always require additional improvements to meet the bar for quality. Be very strict about quality. This usually takes several commits on top of the original PR.

## Check the Tests

- [ ] Does it have tests? If not:

- [ ] Comment on the PR "Can you please add tests for this code to `tests/test_blah.py`", or...
- [ ] Write the tests yourself.

- [ ] Do the tests pass for all of the CI tests? If not, write a note in the PR to fix CI, or fix them yourself.

## Check the Docs

- [ ] Does it have docs? If not:

- [ ] Comment on the PR "Can you please add docs for this feature to the wiki", or...
- [ ] Write the docs yourself.

- [ ] If any new functions/classes are added, do they contain docstrings?

## Credit the Authors

- [ ] Add name and URL to `README.md` for security fixes.
- [ ] Thank them for their hard work.

## Close Issues

- [ ] Merge the PR branch. This will close the PR's issue.
- [ ] Close any duplicate or related issues that can now be closed. Write thoughtful comments explaining how the issues were resolved.

## Release (optional)

- [ ] Decide whether the changes in master make sense as a major, minor, or patch release.
- [ ] Look at the clock. If you're tired, release later when you have time to deal with release problems.
- [ ] Then follow all the steps in [Release Checklist]
