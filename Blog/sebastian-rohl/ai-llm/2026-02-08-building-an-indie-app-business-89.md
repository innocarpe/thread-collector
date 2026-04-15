---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-89
title: "Building An Indie App Business #89"
published_at: 2026-02-08
collected_at: 2026-04-15
author: ""
lang: en
categories: ["ai-llm", "dev-tools", "productivity"]
extras:
  word_count: 1417
  adapter: rss
---

Welcome back to another article about my life as an independent app developer. We’re living in crazy times as developers when you look at the speed of changes caused by AI, but I am really positive about all the changes and I am super excited to increase my business output with all the new tools that are available. Let’s see what happened this week.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### **📊 Business Development**

February is always a weird month for my business. We’re coming from the crazy highs of January and now we’re facing two things at the same time: First, we see a massive spike in renewal revenue because so many new people decided to improve their life with [HabitKit](https://habitkit.app) at the start of January and all those monthly subscriptions are now renewing. Second, we also see a massive spike in churn, because a lot of people didn’t follow through with their plans to change their life and stopped using the app again. Which means they are cancelling their subscriptions. New subscribers coming in, old subscribers leaving. The result? Stagnating (or even declining) MRR.

But honestly, this is totally fine for me. It’s happening every single year and by now I know that growing MRR will be back in March or April. For the first two years of my business, this kind of flatline was really hard for me to deal with. I would check the numbers every morning and feel a little sting every time. But now I’ve been through this cycle enough times that I can just relax and trust the process. Experience is a beautiful thing.

[FocusKit](https://tryfocuskit.com)’s growth is also stagnating a little bit. Right now, we are at $113 MRR and we made $748 in total revenue for the past 28 days. These numbers are super low in comparison to HabitKit, but you know what they say: “comparison is the thief of joy.” So I have to imagine I never had the HabitKit experience and enjoy the numbers as if FocusKit was my first and only app. When you look at it like that, ~$750 in revenue for the past 28 days is actually awesome and I am really happy with that. A year ago, FocusKit didn’t even exist. Now it’s making real money. Still, I am excited to make it grow even more and I will do everything I can to make it the best Pomodoro / Focus Timer app out there.

#### **🛠️ FocusKit Development**

On Monday I released the biggest update for FocusKit yet! I already told you about all the cool new features in previous newsletters so you probably already know that it brings support for custom routines. Users can now build their own routines from scratch, manage multiple of them, give them names, adjust the individual durations, and configure the long-break logic exactly how they want it. This makes FocusKit so much more flexible and customizable. I use this feature all the time myself, so I am pretty sure that other people will love it as well. Nothing beats using your own product and thinking “yeah, this is actually good.”

But I didn’t stop there. I already have the next smaller update in development and it’s ready for testing. This one fixes two pain points that users have been telling me about for a while:

- 

**Auto-advance to Next Session:** Some users thought it was weird that you have to explicitly tap a button to move to the next session when the previous one is over. I originally implemented it that way because I thought some people prefer to fill in the session notes AFTER a session finishes, so staying on the completed session and allowing the user to make changes made sense to me. Turns out, not everyone works like that. Some people just want the next session to start immediately without any extra taps. Fair enough. So I made this configurable in the settings. Now there is an “Auto-advance to Next Session” toggle and everyone can choose what works best for them.

- 

**Daily Routine Reset:** This was the other big pain point that many users kept telling me about: The routine progress doesn’t automatically restart at the start of a new day. When you think about it, this makes total sense. Nobody wants to open the app in the morning and start with a break session because that’s where they left off yesterday. I have to be honest, I hadn’t thought this through properly when I developed the first version of the app. And the funny thing is, once so many people kept nagging me about this, I realized that it actually annoyed me too. I just never noticed it because I was so focused on building other features. So I made this configurable as well, with “Yes, please refresh every day” as the new default.

Can’t wait to release this! Should be out next week. These are the kind of updates that don’t sound exciting on paper, but they make the daily experience of using the app so much better. And happy users stick around longer, which is great for retention and ultimately for the business.

#### **🤖 OpenClaw Updates**

If you’re following me on X or read my last newsletter issue, you probably know that I am pretty excited about OpenClaw and agentic AI in general. I already saw so many positive effects on my development speed that I am super stoked about having a personal assistant for my app business. I have to admit that I couldn’t find that much time this week to expand my workflows with it, but I have some huge plans. Especially once Sonnet 5 drops. Can’t wait to see what that model can do.

The most interesting use case I’m working on right now: Support Email Automation. Here’s the thing, the first 30 minutes of my work day are usually eaten up by answering support emails. I get so many questions about how to cancel the subscription or how to archive a habit or when feature X will drop. And the answers are usually pretty similar every time. Copy, paste, adjust a name, send. It’s not hard work, but it’s repetitive and it eats into my productive morning hours. So there is definitely room for automation here.

Here is the plan, and I think it’s going to be really cool:

**Step 1: Fix the email situation.** Right now, everything is pointing to my private Gmail address. Yes, I know... not very professional. We need to create a proper support email address for my indie app business and update every single place where I link to it. App Store descriptions, in-app support buttons, website footer, everywhere. This alone is going to be a bit of a project, but it’s long overdue anyway.

**Step 2: Let OpenClaw handle the drafts.** Once the new email is set up, I want to give Eric, that’s my OpenClaw bot, access to it and let him DRAFT (not send!) replies to the incoming emails. This is really important to me: the bot should never be able to send emails on his own. I want to stay in the loop and have the final say on everything that goes out. The idea is that when I open my inbox in the morning, there are already draft replies waiting for me. I just go through them, make a quick change here and there if needed, and hit send. That could turn my 30-minute email session into a 5-minute one.

**Step 3: Make OpenClaw actually good at this.** For the drafts to be useful, Eric needs to understand my apps and match my tone. So we need to feed him all my existing email templates and build some kind of wiki for my apps that describes every screen, every feature, every common question. The more context he has, the better his drafts will be. I want someone to read his response and think “yeah, that sounds exactly like Sebastian would write.”

I’m really excited about this one. Still need to figure out some of the technical details, but I’m sure Eric will help me out with that too. That’s the beauty of having an AI assistant, you can literally ask it to help you set itself up. We’re living in the future.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.