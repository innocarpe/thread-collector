---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-88
title: "Building An Indie App Business #88"
published_at: 2026-02-01
collected_at: 2026-04-15
author: ""
lang: en
categories: ["ai-llm", "startup-philosophy", "productivity"]
extras:
  word_count: 1495
  adapter: rss
---

This week was a bit different. I spent most of it tinkering with the latest hype topic: [OpenClaw](http://openclaw.ai) (a personal AI assistant), developing my apps in the meantime, and honestly... completely changing how I think about AI and work. If you’ve been reading my newsletter for a while, you know I’ve been pretty careful about the whole AI hype. I’m not someone who jumps on every new trend just because Twitter is going crazy about it. But this week something clicked for me. I’m not just using AI as a coding helper anymore. I’m starting to see it as a complete productivity game changer. Let me tell you why. But first, let’s talk about some REAL work I did on [FocusKit](https://tryfocuskit.com)!

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### **🛠️ FocusKit 1.2.1: Small Details That Actually Matter**

I made good progress on FocusKit 1.2.1 this week. This update is all about polish. You know, those small UX things that users don’t really notice consciously, but they definitely feel the difference when they use the app.

The main thing I added was an active session indicator in the History tab. Here’s the problem I was trying to solve: When you start a focus session and then go to the History tab to check your timeline, it looks completely empty. That’s because the current session isn’t finished yet, so there’s nothing to show. People were confused by this. I got a few support emails from users who thought the app wasn’t tracking their sessions properly. Not a great experience.

So now when you’re in an active session, it shows up in the history with a nice pulsating animation. You can see it right there, doing its thing, tracking your focus time. Pretty simple fix, but it makes the app feel way more alive and responsive. Sometimes it’s really the small stuff that counts.

I also tried to add a feature where you could long-press the toolbar date picker to jump back to today. Seemed like a really good idea. You’re looking at last week’s history, and with one long-press you’re back to today. Simple, right? Turns out it’s not possible with SwiftUI right now. At least not in a clean way. Getting a date picker into the toolbar was already a pain with SwiftUI. Adding a long-press context menu on top of that? The APIs just don’t play nice together. I spent about an hour trying different approaches before I accepted defeat. Sometimes you just have to let features go and move on. Maybe I’ll find a workaround later. For now, it stays on the “nice to have” list.

#### **🤖 Building a Productivity System (With AI Help)**

Okay, here’s the bigger story this week. I built a complete Second Brain web app from scratch. And when I say “I built”, I mean I mostly directed an AI to build it for me. Let me explain.

I’ve been using countless tools for my personal knowledge management for years, but I always wanted something simpler that completely suits my personal needs. Something that just works with plain markdown files, syncs with GitHub, and doesn’t require me to be online all the time. Here’s what I wanted:

- 

Markdown-based notes organized in PARA folders (Projects, Areas, Resources, Archive)

- 

A file browser with a nice tree view on the side

- 

A clean editor for writing that doesn’t get in the way

- 

Task checkboxes that you can actually click to check them off

- 

Everything auto-saves so I never lose work

- 

Everything auto-commits to GitHub so I have version history

I know, it sounds like Obsidian, but this should just be the base. I want to extend it with lots of diferrent custom solutions for time tracking, todo management, ...

Now here’s where it gets interesting. On Wednesday night, before going to bed, I told my AI assistant: “Build me a second brain app with these features.” I described what I wanted, explained why I needed each feature, and gave some examples of how I would use it. Then I went to sleep.

When I woke up on Wednesday morning, there was a working React app waiting for me. 33 files. Almost 8,000 lines of code. Most of the features I asked for were already there and working. The AI had built it, tested it, pushed it to GitHub, and sent me a message when it was done. I didn’t watch it build the app. I didn’t sit there and code with it. I literally just told it what I wanted, went to bed, and woke up to a functioning application.

I know this sounds like I’m exaggerating, but I’m not. This is what I mean when I say things are changing fast. It’s not about coding WITH AI anymore. It’s more like managing AI developers. I describe what I want (not HOW to build it, just WHAT I need and WHY it matters). My AI assistant spawns a sub-agent that goes off and builds it. The sub-agent messages me when it’s done. Then I review it, test it, and either approve it or give feedback for the next iteration.

The crazy part? The sub-agents didn’t just build what I asked for. They also fixed bugs I didn’t even mention, optimized some performance issues, and added little UX improvements I hadn’t thought about. Then they wrote documentation explaining what they changed and why. It’s like having a team of developers who actually read your mind and anticipate what you need.

Now I can talk to my bot on Telegram, and it automatically adds or removes tasks from my dashboard. I can ask it to create a new project note, and it does. I can ask it to show me all tasks due this week, and it pulls them from my markdown files. All of this built in basically one night while I was sleeping.

#### **💭 What This Means For Indie Developers**

I’ve been thinking a lot about what this means for people like us. The evolution has been wild to watch:

- Three years ago, we were all learning to code from scratch

- Two years ago, we started using AI coding assistants like Copilot

- Last year, we were learning how to write better prompts and have conversations with AI

- Now? We’re learning how to delegate entire projects to AI agents

Don’t get me wrong, you still need to know how to code. You need to understand what the AI is doing, what’s technically possible, and where problems might show up. You can’t just blindly trust everything an AI produces. But the day-to-day work is different now. It’s less about typing code and more about thinking clearly about problems and solutions.

For indie developers, this is absolutely huge. We never have enough time. There’s always more stuff we want to build than we can actually ship. Being able to delegate the building part to AI, and actually trust that it will do a decent job, means we can move way faster than before. We can spend more time on the things that actually matter: figuring out what users really need, making the product better, talking to customers, and growing the business. You know, the stuff that actually makes money.

I’ll be honest though, I also feel a bit conflicted about all of this. I feel really bad for junior programmers searching for a job right now. The industry is changing so fast, and the skills that got you hired five years ago might not be enough anymore. The future seems to belong to those who can see the problem clearly, design the right solution, AND orchestrate AI agents to build it. Pure coding skills without the bigger picture thinking? That’s becoming less valuable every day.

I don’t know exactly where this is all going, but I know I want to be part of it. And I want to share what I learn with you along the way.

#### **🎙️ Launched Podcast**

On a completely different note: At the end of last year, I had the honor to be a guest on one of my favorite podcasts! Charlie Chapman invited me to the “Launched” podcast, and the episode is finally out.

We talked about a lot of things that I think you’ll find interesting: the power of building in public (and how it helped me grow HabitKit), how persistence pays off when growth feels painfully slow, and why focusing on what users actually need (instead of what you think is cool) can lead to unexpected success in indie app development.

[If you want to hear me ramble for about an hour about my indie journey, check out the latest episode](https://launchedfm.com/episode/84-habitkit-sebastian-rohl). And let me know what you think! I always love hearing from you guys.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.