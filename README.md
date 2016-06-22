# eng-ops

We have API access to both ZenHub and GitHub:
https://github.com/ZenHubIO/API
https://developer.github.com/v3/issues/
If we start storing and modeling Issues and their lifecycles, can we start answering nuanced questions about our workflows and productivity?

Issue-specific questions:

* How long did it take to close this issue?
* What type of issue was it? e.g. Eng Sanity, Feature, Support, etc (based on label)
* What Milestones was it a part of?
* How long did it take to go from "New Issue" to "In Progress"? From "Ready to do" to "Closed"? (or any other two pipelines)


Aggregate questions:

* On average, how long does a "1", or "2", or "5" take?
* How long do issues stay as "Ready to do", on average?
* Where do we spend the most eng time? e.g. Support, Feature, Bug, etc
* Which areas (e.g. Bug, etc) have the most issues created for them?
* How long does the average "Bug" take to resolve?

Questions about individual engineers:

* How many points does each person average per week?
* What's the breakdown of each person's tasks (e.g. Bug, Support, etc)
* Can we highlight times when someone has too much/too little assigned to them?


Team questions:

* Could the team "do more"? Do we have the capacity to resolve more issues/week?
* How much does our productivity vary each week?
* Can we automate standups? e.g. Slack us each a message beforehand with our recent updates, etc
