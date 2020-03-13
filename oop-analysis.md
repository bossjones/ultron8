Design Analysis: Ultron8
======

## Overview

Ultron8 is a automated Instance diagnostic and remediation platform. It uses a hive / drone(master/agent) approach to auditing instances, issuing ad-hoc commands or runbooks to distributed task managers. Ultron8 can be observed via the `ultronctl` commandline tool to see what is running on each agent along with the state of that host and its resources. It can also be used to issue commands to certain hosts based on a variety of different criteria. The agent component is composed of a small aio http server via the fastapi framework. It exposes a REST API that can be used to interact directly with both the master and the agent nodes. It requires authentication, supports tls, and passes on tasks to a distributed task queue via [celery](http://www.celeryproject.org/) that is using [Redis](https://redis.io/) as the Broker backend. MongoDB might be another possible option at some point. Both Netflix Bolt and Stackstorm were used as inspiration.

## Highlevel

* Facilitated Troubleshooting - triggering on system failures captured by [node-exporter](https://github.com/prometheus/node_exporter), Sensu, New Relic and other monitoring systems, running a series of diagnostic checks on physical nodes, OpenStack or Amazon instances, and application components, and posting results to a shared communication context, like HipChat or JIRA.

* Automated remediation - identifying and verifying hardware failure on OpenStack compute node, properly evacuating instances and emailing admins about potential downtime, but if anything goes wrong - freezing the workflow and calling PagerDuty to wake up a human.

* Continuous deployment - build and test with Travis, provision a new VM cluster, turn on some traffic with the load balancer, and roll-forward or roll-back, based on NewRelic app(or similar) performance data.

## Design Decisions

* Actions should be version controlled ( eventually )
* Ultron8 client libraries and cli should communicate directly with the instances themselves
* History of execustions stay on the instances, but can be displayed by querying the master node
* Language support Python(via venvs)/Bash Shell scripts

## Adaptors for VM environment ( What makes everything work )

### Sensors

Sensors are Python plugins for either inbound or outbound integration that receives or watches for events respectively. When an event from external systems occurs and is processed by a sensor, a Ultron8 trigger will be emitted into the system.

### Triggers

Triggers are Ultron8 representations of external events. There are generic triggers (e.g. timers, webhooks) and integration triggers (e.g. Sensu alert, JIRA issue updated). A new trigger type can be defined by writing a sensor plugin.

### Actions

#### Actions: Overview
Actions are Ultron8 outbound integrations. There are generic actions (ssh, REST call), integrations (OpenStack, Docker, Puppet), or custom actions. Actions are either Python plugins, or any scripts, consumed into Ultron8 by adding a few lines of metadata. Actions can be invoked directly by user via CLI or API, or used and called as part of rules and workflows.

#### Actions: Use cases

To give you a better idea, here is a short list of tasks which can be implemented as actions:

* acknowledge a Nagios/PagerDuty alert
* create a new cloud server
* restart a service on a server
* run a Nagios check
* send a message to Slack
* send a notification or alert via email or SMS
* send a notification to an IRC channel
* snapshot a VM
* start a Docker container

Actions can be executed when a Rule with matching criteria is triggered. Multiple actions can be strung together into a Workflow. Actions can also be executed directly from the clients via CLI, API, or UI.

### Rules

Rules map triggers to actions (or to workflows), applying matching criteria and mapping trigger payload to action inputs.

### Workflows

Workflows stitch actions together into "uber-actions", defining the order, transition conditions, and passing the data. Most automations are more than one-step and thus need more than one action. Workflows, just like "atomic" actions, are available in the Action library, and can be invoked manually or triggered by rules.

### Packs

Packs are the units of content deployment. They simplify the management and sharing of Ultron8 pluggable content by grouping integrations (triggers and actions) and automations (rules and workflows). A growing number of packs are available on Ultron8 Exchange. Users can create their own packs, share them on Github, or submit to the Ultron8 Exchange.

### Audit trail

Audit trail of action executions, manual or automated, is recorded and stored with full details of triggering context and execution results. It is also captured in audit logs for integrating with external logging and analytical tools: LogStash, Splunk, statsd, syslog.

## How it works ( high level )

1. Events are aggregated (Push/Pull) from various services via Sensors
2. Events are compared against Triggers, and generate Actions
3. Processed actions from workflows are palces on message queue (Redis/RabbitMQ)
4. Actions reach out to various services to perform workflow actions
5. Log and Audit History is pushed to database for storage (Mongodb, sqlite, mysql)
6. Processed Results are sent back to the rules engine for further processing


### General Termonology

### Master

### Nodes

*Considerations: Should we use bcc-tools?*

* Resources:
  * CPU:
    * Who: Which PIDs, programs, users
    * Why: Code paths, context
    * What: CPU instructions, cycles
    * How: Changing over time
  * Memory:
    * Who: Which PIDs, programs, users
    * Why: Code paths, context
    * What: What systemcalls, malloc(), free()
    * How: Changing over time
    * Which: Are we talking Memory, Real Memory, Private Memory, Purgeable Mem, or Compressed Mem?
  * Disk:
    * What: files are being accessed, and how? By what or whom? Bytes, I/O counts?
    * What: is the source of file system latency? Is it disks, the code path, locks?
    * How: effective is prefetch/read-ahead? Should this be tuned?
  * Networking:
    * Who: Which PIDs, programs, users
    * Why: Code paths, context
    * What: RX/TX throughput / max bandwidth(network interface), saturation related NIC or OS events; eg "dropped", "overruns"
    * How:
    * Which:

### CLI interactions




## Appendix

[Linux Profiling at Netflix by brendangregg](http://www.brendangregg.com/Slides/SCALE2015_Linux_perf_profiling.pdf)
[Dtrace - File Systems](http://www.brendangregg.com/DTrace/DTrace_Chapter_5_File_Systems.pdf)

[memory flamegraphs brendangregg](http://www.brendangregg.com/FlameGraphs/memoryflamegraphs.html)
[Use Method brendangregg](http://www.brendangregg.com/usemethod.html)
[Stackstorm Overview](https://docs.stackstorm.com/overview.html#how-it-works)
[Node Exporter](https://github.com/prometheus/node_exporter)
