---
layout: post
title: Running coding agents from a phone
date: 2026-10-13
byline: By Eyal and Claude. The idea is Eyal's. Claude Code wrote it up with him.
description: What it takes to run several AI coding agents and check on them from a phone.
noindex: true
---

I run several AI coding agents at the same time, and most of the time I check on them from my phone. **The agents spend hours on the actual work; my part is to start them, answer their questions and approve their next step, and none of that needs a big screen.** The agents were already good enough; what I had to build was the tooling around them.

## The problem

With several agents running, I couldn't tell what any of them was doing without walking back to my desk. An agent that stops to ask for approval just waits, sometimes for an hour, until someone notices.

## What helped

The most useful piece is a single list of all the sessions, with a status next to each one, so I can see which are working, which are done and which are waiting for me. The second is a notification as soon as one of them asks something. After that come smaller things, like reflowing the terminal to the phone's width so the text is readable, and dictating instructions instead of typing them. I built these into tmux-web, my own web client for the terminal sessions the agents run in.

## Where the laptop wins

Reading a large code change on a phone is still hard, so for reviewing big diffs I sit at the laptop.
