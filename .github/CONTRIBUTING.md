## Contributing
You are here to help the Python Multicast Project? Awesome, feel welcome and read the following sections in order to know what and how to work on something. If you get stuck at any point you can create a ticket on GitHub.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.


When reporting an issue, please list the version of Python Multicast Library you are using and any relevant information about your software environment (python version, OS type and version, etc). Also avoid vague language like "it doesn't work." Please describe as specifically as you can what behavior you are actually seeing (eg: an error message? a nil return value?).


For all contributions, please respect the following guidelines:

Each pull request should implement ONE feature or bugfix. If you want to add or fix more than one thing, submit more than one pull request.
- Do not commit changes to files that are irrelevant to your feature or bugfix (eg: .gitignore).
- Do not add new external dependencies unless ABSOLUTELY necessary (these could cause Load Errors on certain systems).
- Add new tests for new code if able (otherwise add descriptive pseudo-tests as issues).
- Be willing to accept criticism and work on improving your code; care must be taken not to introduce bugs or vulnerabilities.

#### Known Issues and Possible Improvements

For Details on current issues:
- see [Issues](https://github.com/reactive-firewall/multicast/issues)

## Triaging tickets
Here is a brief explanation on how I triage incoming tickets to get a better sense of what needs to be done on what end.

>>Note
>>
>>You will need Triage permission on the project in order to do this. You can ask one of the members of the Team to give you access. (Please join the beta first.)

## Initial triage
When sitting down to do some triaging work, start with the list of untriaged tickets. Consider all tickets that do not have a label as untriaged. The first step is to categorize the ticket into one of the following categories and either close the ticket or assign an appropriate lable. The reported issue

 *  is not valid
If you think the ticket is invalid comment why you think it is invalid, then close the ticket. Tickets might be invalid if they were already fixed in the past or it was decided that the proposed feature will not be implemented because it does not conform with the overall goal of Multicast Project. Also if you happen to know that the problem was already reported, label the ticket with Status: duplicate, reference the other ticket that is already addressing the problem and close the duplicate.

Examples:

This is an issue. (A good starting point for first person to discover)


 *  does not provide enough information
Add the label question if the reported issue does not contain enough information to decide if it is valid or not and ask on the ticket for the required information to go forward. I will re-triage all tickets that have the label question assigned. If the original reporter left new information we can try to re-categorize the ticket. If the reporter did not come back to provide more required information after a long enough time, we will close the ticket (this should be roughly about two weeks).

Examples:

My builds stopped working. Please help! Ask for a link to the build log and for which project is affected.


 *  is a valid enhancement proposal
If the ticket contains an enhancement proposal that aligns with the goals of Multicast, then add the label Enhancement. If the proposal seems valid but requires further discussion between core contributors because there might be different possibilities on how to implement the enhancement, then also add the label question.

Examples:

Improve documentation Examples in contribute docs.
Provide better integration with security feature XYZ
Refactor module X for better readability (see #48)
Achieve world domination (also needs the label question)


 *  is a valid problem within the code base:
If it’s a valid bug, then add the label Bug. Try to reference related issues if you come across any.

Examples:

Multicast Library fails to transmit the leter 'x' or 'y' (logs attached)


 *  is a question and needs answering:
If the ticket contains a question about Multicast messages or the code, then move question to FAQ on wiki and add task to answer question on wiki to the issue (or close if already answered).

Examples:

My message was seen by two hosts. Why?
Why are my builds failing?


Helpful links for triaging
Here is a list of links for contributors that look for work:

Untriaged tickets: Go and triage them!


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

- [ ] Do the tests pass for all of the following? If not, write a note in the PR, or fix them yourself.

	- [ ] Python 3.12 - Mac (OPTIONAL)
	- [ ] Python 3.11 - Linux
	- [ ] Python 3.12 - Linux
	- [ ] Python 3.9 (or Newer) - Mac
	- [ ] Python 3.10 - Linux
	- [ ] Python any - Windows (OPTIONAL)

## Check the Docs

- [ ] Does it have docs? If not:

	- [ ] Comment on the PR "Can you please add docs for this feature to the wiki", or...
	- [ ] Write the docs yourself.

- [ ] If any new functions/classes are added, do they contain docstrings?

## Credit the Authors

- [ ] Add name and URL to `README.md` for security fixes.
- [ ] Thank them for their hard work.

## Check the copyright year:

- [ ] reads:

> Copyright (c) 2017-2024, Author


## Close Issues

- [ ] Merge the PR branch. This will close the PR's issue.
- [ ] Close any duplicate or related issues that can now be closed. Write thoughtful comments explaining how the issues were resolved.

## Release (optional)

- [ ] Decide whether the changes in master make sense as a major, minor, or patch release.
- [ ] Look at the clock. If you're tired, release later when you have time to deal with release problems.
- [ ] Then follow all the steps in [EXAMPLE Release Checklist](https://github.com/reactive-firewall/Pocket-PiAP/issues/87) FIXME!
