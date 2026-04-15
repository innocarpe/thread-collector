---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-91
title: "Building An Indie App Business #91"
published_at: 2026-02-22
collected_at: 2026-04-15
author: ""
lang: en
categories: ["dev-tools", "web-app", "productivity"]
extras:
  word_count: 1084
  adapter: rss
---

Welcome back to another issue of my weekly indie log! This was one of those weeks where I just put my head down and shipped. Multiple projects moved forward at the same time, I ran into some tough technical challenges, and I spent some time improving my development workflow. Let’s get into it.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### **🛠️ Development Corner**

A lot happened this week on the development side, so let me break it down project by project.
[이미지: Image]

**FocusKit Watch Integration is almost ready for beta.** If you’ve been following along, you know I’ve been working on bringing FocusKit to the Apple Watch. This week I made some really solid progress on it. Users will be able to start, stop, reset, and skip sessions directly from their wrist, see their Routine progress, and even get a history of the past couple of days. I’m really happy with how it’s coming together.

That said, building for watchOS is not easy. Apple created this beautiful ecosystem and then they just... don’t give you the APIs you need. Some things that feel like they should be straightforward are either not possible or require really creative workarounds. I had a nice evening vibe coding session earlier this week where things finally clicked, and after that we moved fast. But getting there was a struggle. Lots of obstacles and failed approaches, even with AI assistance. Some things like canvas operations and sidebar layouts are just tough no matter how you approach them.

One thing I noticed while testing the newest version: some workflows and animations started to lag. I iterated pretty fast while preparing the phone app for integration with the Watch, and now I need to go back and debug performance. This is honestly one of my biggest weaknesses as a developer. After a while of building features quickly, animations start to feel janky and I need to sit down and actually think about best practices and optimization. It’s not the most exciting work, but it has to be done.

I also added a couple of Complications for the Watch faces and I had a lot of fun while building them out. First time I felt like Xcode did something right in terms of developer experience.

**My secret MacOS side project is getting closer to a release-ready version.** I’ve been putting a lot of time into polishing and design tweaking on this macOS app project. If you remember from last week, I finally got it to beta after dragging it around for over 2 years. This week the focus was on making the whole experience feel right. Getting closer every week.

**HabitKit landing page in the background.** Here’s something I’ve been doing that I really enjoy: while my main focus was on FocusKit development, I’ve been vibe coding on a new landing page for HabitKit on the side. It’s one of those projects you can pick up for 30 minutes when you need a break from your main task. Different context, different tech stack, but still productive. I like working this way because it keeps things fresh without losing momentum on the important stuff.

**Quick thought on Apple’s recent design direction: iOS 26 Liquid Glass.** I’ve said it before and I’ll say it again: this is one of the best design decisions Apple has ever made. Every time I look at it, I’m impressed. It just looks right. Especially the look and feel of the Apple Music app with the latest iOS beta is awesome.

#### **💡 Indie Insights**

**The AI speed paradox.** New AI models are allowing me to iterate on my ideas faster than ever. I can go from concept to working prototype in a fraction of the time it used to take. AI should theoretically make you work less, right? In practice, I’ve never worked as much as in the past few weeks. The speed at which you can build things doesn’t give you a breathing break. There’s always the next feature, the next improvement, the next project you could start right now. It’s a weird paradox. The tool that should free up your time actually makes you want to spend more time building because the results come so fast. I’m trying to be more intentional about this, but it’s hard when every new model makes you 10% faster.

**Cursor Skills and Rules.** One thing I heavily neglected over the past months: setting up proper Skills and Rules for my projects in Cursor. I knew they existed, I knew they were useful, but I never took the time to really experiment with them. This week Cursor added a marketplace that makes it super easy to import battle-tested skills from other developers. I spent some time exploring it and I’m honestly impressed. It’s one of those things where you wonder why you didn’t do this earlier. Having good rules and skills set up for your codebase makes the AI output so much better. If you’re using Cursor and haven’t looked into this yet, I really recommend checking it out.
[이미지: Image]

**Productivity app adventures.** I’ve been trying out Craft as my new productivity and journaling app. I really tried to like Obsidian for a while, but it just feels too scrappy for me. The tasks plugin doesn’t feel smooth enough, and the whole experience is more “powerful tool” than “enjoyable app”. Craft on the other hand is just beautiful. It feels good to open it, it feels good to write in it. Sometimes the tool you use matters just as much as what you do with it.

#### **🎯 Goals for Next Week**

Next week will be all about HabitKit. I need to upgrade the Flutter version and do some maintenance work that I’ve been pushing off for a while. It’s not glamorous work, but it’s necessary. The goal is to get HabitKit into a development-ready state where I can vibe code on it regularly and ship updates more frequently again. It’s been on the back burner for too long while I was focused on FocusKit and the macOS projects, and it deserves some attention. Once the maintenance is done, I can start making progress on some important features in the coming months.

That’s it for this week. Thanks for reading, and I’ll see you in the next one!

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.