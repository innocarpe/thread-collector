---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-90
title: "Building An Indie App Business #90"
published_at: 2026-02-15
collected_at: 2026-04-15
author: ""
lang: en
categories: ["dev-tools", "ai-llm", "productivity"]
extras:
  word_count: 1642
  adapter: rss
---

Welcome back to another issue of my weekly indie log! This week was all about systems. Setting up new tools, finally getting a long-running side project to beta, and finding the right AI coding workflow. If I’m being honest, I spent way more time tinkering with tools and prompting than writing actual code. But sometimes that’s exactly what you need to do to move faster later. Let’s get into it.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### **📊 Business Updates**

Not a lot to report on the revenue side this week. HabitKit is still settling into its post-New-Year baseline, which is completely expected at this point. If you’ve been following along for a while, you know what’s happening. January is the big peak, and then it slowly comes back down to normal levels. Nothing to worry about. I’ve seen this movie before, and I know how it ends: things stabilize, and then we grow again.

FocusKit’s MRR is stagnating a little bit right now, but the total revenue is still doing great. The seasonal dip doesn’t bother me anymore. A year ago I would have been checking my RevenueCat dashboard five times a day and stressing about every small drop. Now I just trust the process and focus on making the app better. That’s really the only thing I can control anyway.

#### **🛠️ Development Corner**

Okay, let’s talk about what actually got built this week.

**A side project finally hit beta.** I’ve been dragging this macOS app around for over 2 years now! It was one of those projects that kept getting pushed back because there was always “real work” to do for my existing apps. Every time I wanted to sit down and work on it, something else came up. A bug fix for HabitKit. A new feature for FocusKit. Support emails. You name it. But this week, with some heavy AI assistance, I finally got it to a state where I can put it in front of the first internal tester. It’s not perfect by any means, but it works. And I can’t tell you how good it feels to actually ship something after procrastinating on it for so long. There’s something about getting a project out of your head and into the real world that feels incredibly freeing. More details coming soon, I promise.

**FocusKit 1.2.1 shipped.** This was a polish update focused on small UX details that really matter. The main thing: I added an active session indicator in the History tab with a nice pulsating animation. Here’s the problem I was solving: users would start a focus session, switch to the History tab, and it would look completely empty. They were confused and thought the app wasn’t tracking their session. Not a great experience. Now they can see their active session right there, doing its thing. Simple fix, but it makes the app feel so much more alive.

I also tried to add a long-press gesture on the toolbar date picker to jump back to today. Seemed like a great idea in my head. You’re looking at last week’s history, long-press, and you’re back to today. Turns out SwiftUI doesn’t play nice with this at all. Getting a date picker into the toolbar was already a struggle. Adding a long-press on top of that? The APIs just refuse to work together cleanly. I spent about an hour trying different approaches before accepting defeat. Sometimes you just have to let features go and move on. It stays on the “nice to have” list for now. Maybe one day, I’ll find a creative workaround. We’ll see.

**FocusKit WatchKit integration is underway.** This is the big project for the next few weeks and I’m really excited about it. I spent a lot of time this week refactoring the SessionManager to make it callable from everywhere, including the Watch app. Right now it’s a lot of groundwork and not very glamorous, but it’s necessary to get right. The goal is to let users start a focus session from their wrist, see live progress on the Watch, and get those nice haptic notifications when the timer ends. My vision for FocusKit has always been to make it as Apple-like as possible, deeply integrated into the whole ecosystem. iOS, widgets (coming soon as well), and now watchOS. I want it to feel like it belongs there, like Apple could have built it themselves.

**The OpenClaw setup is getting serious.** If you’ve been reading my past issues, you know I’ve been building out a personal AI assistant setup with OpenClaw. This week I found some time to tinker with it again. I let it creat a custom skill that automatically summarizes YouTube videos and saves them to my knowledge base. So now instead of watching a 30-minute video, I can just feed it the link and get a clean summary in seconds. It’s been great for keeping up with all the AI content without losing entire evenings to YouTube.

I also set up a dedicated area where the AI can keep its own tasks, capabilities, and even journal entries. I basically gave my AI assistant its own workspace where it can organize itself. It actually makes the whole setup way more useful. The more context the AI has about itself and what it can do, the better it performs.

Looking ahead, I want to explore some new models as well. The new MiniMax M2.5 model looks interesting, and I’m curious how it compares to my current setup with Opus and Codex. The AI landscape is moving at an insane speed right now, and it feels like every week there’s something new to try.

#### **💡 Indie Insights**

I think I finally cracked my AI coding workflow (until the next wave of disruptive models drop). For the past couple of weeks, I’ve been experimenting with different setups, trying to find the sweet spot between letting AI do the work and staying in control of my codebase. And here’s what’s working really well for me right now:

- 

**Opus 4.6 for planning.** I describe the feature I want to build, the architecture, the edge cases, everything I can think of. Opus thinks through the whole thing and gives me a solid plan with all the steps laid out. It’s like having a senior developer do the design review before you write a single line of code. I also gave it a bunch on skills and rules for best practices on SwiftUI and my codebase in general.

- 

**Codex 5.3 for implementation.** Once I have the plan, I hand it to Codex in Cursor and let it write the actual code. Having a clear plan makes a huge difference here. The more specific the plan, the better the output.

- 

**Me for review.** I read what it produced, test it, fix the obvious mistakes, and iterate. This is the part where my actual coding knowledge comes in. You still need to understand what’s happening under the hood.

This workflow has been incredibly productive for me lately. I’m moving faster than I ever could coding everything myself, but I still feel fully in control of what’s happening in my codebase. The AI handles the boring implementation details, and I focus on the architecture and UX decisions. You know, the stuff that actually matters for the user.

I’m starting to think less about “how do I code this?” and more about “how do I describe what I want so an AI can build it?” It’s a completely different skill set. Less syntax memorization, more clear thinking and communication. I finally feel like a product manager, writing specs for a really fast developer who never needs a coffee break.

**One more thing I want to be honest about.** The AI hype on X brings me anxiety sometimes. I see people building all kinds of amazing stuff every single day, shipping new tools, launching products, creating businesses overnight. And it’s a little bit intimidating how fast everyone seems to be moving. There are moments where I think “am I falling behind? Should I be doing more?” But I’m actively trying to focus on my own progress instead of comparing myself to others. Comparison really is the thief of joy, especially on social media where everyone only shows their highlights. I have my own pace, my own goals, and my own journey. That has to be enough.

Also, I really need to pick up the deep life habits again. If you read my past issues, you know I used to be really strict about avoiding Reddit and YouTube. Well, I slipped. These platforms are garbage for my brain. I always tell myself “just one video” or “just a quick scroll” and then 45 minutes have passed and I feel worse than before. X has some value with all the AI discussion happening there, but it’s also a massive distraction. I keep tabbing away from my work to check notifications. Not good. I need to get back to being disciplined about this, because the difference in my focus and productivity is night and day.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### **🎯 Goals for Next Week**

The main goal is to make serious progress on the FocusKit Watch app and get it to the TestFlight crowd. I’m really excited about this update because it’s not just the Watch integration, it will also bring a lot of performance improvements to the iPhone app. The refactoring I’m doing now to support the Watch is making the whole codebase cleaner and faster. Sometimes doing the hard work upfront pays off in unexpected ways.

That’s it for this week. Thanks for reading, and I’ll see you in the next one!