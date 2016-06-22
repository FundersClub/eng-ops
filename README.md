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


#### Things to model

* Issue
* Pipeline
* Label
* User
* Milestone
* Estimate ?
* PRs
* Comments on PRs/Issues

These relationships are fluid – an Issue might enter/leave a Pipeline multiple times, and the timing around that is important. Its Estimates and Assignees may change, and we need to know that.

Modeling option: Issues -> PipelineStates (state: started: ended:?)


#### Potential roadmap

* V0: Build nuanced definition of Issue that only stores current snapshot into a Postgres DB, visualize in RJMetrics
* V0.1: Build Slack integration for pre-standups (What closed in last 24, what's in each Pipeline)
* V0.2: Model PRs/Comments
* V0.3: Improve Slack integration to include Comments and PRs.
* V1: Build and track nuanced PipelineStates over time
* V1.1: Assess tracking nuanced Label/User/Milestone/Estimate/etc changes over time
* V2: Support for individual engineer queries
