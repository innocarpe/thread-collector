---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-84
title: "Building An Indie App Business #84"
published_at: 2025-12-07
collected_at: 2026-04-15
author: ""
lang: en
categories: ["startup-philosophy", "case-study", "monetization"]
extras:
  word_count: 997
  adapter: rss
---

Welcome back to another issue of my weekly indie log. One week ago I released my new app FocusKit and so far I’m pretty happy with how things are going. It’s been a busy but exciting week!

**[Short intermission: FocusKit is featured on ProductHunt today. It would mean the world to me if you could give it an upvote there! Thanks so much for all the support.](https://www.producthunt.com/products/focuskit?launch=focuskit)**

Let me tell you everything I’ve done since the release.

#### Bugfixes and New Features

Here’s something I learned from launching HabitKit: you should always be prepared for bugs. No matter how much you test, users will find issues you never thought about. So a couple of days before the actual release, I already started working on the first update. This way I could immediately respond to any feedback without scrambling around.

I released FocusKit 1.0.1 on Monday, just two days after launch. I wanted to show early users that I’m actively working on the app and listening to their feedback. I am always looking for improvements I can make to the app and this is super important in the early stages in my opinion.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

The update includes a changelog modal so users can see what’s new when they open the app after an update. I also made the “Adjust Timer” buttons automatically show up when a session is over, a few people mentioned they sometimes want to add or subtract a few minutes after finishing, and this makes it much easier. And I added left-right arrows on the “Change Metrics” buttons for better navigation.

On the bugfix side, I fixed an issue where sessions were sometimes misplaced in the Timeline tab. This was actually a bit tricky to track down because it only happened in specific edge cases. I also made sure sound options now apply to “Reset” actions as well (they didn’t before, which was an oversight on my part), and fixed an issue where the Insights category filter wasn’t able to take full height on some devices.

Shortly after I was done with 1.0.1, I started working on FocusKit 1.1.0. I think it has enough important features to justify bumping the version number to 1.1 instead of just another patch release.

The biggest addition is the ability to set a default category. This was actually one of the most requested features during beta testing, people don’t want to select a category every single time they start a session. Now you can just pick your most-used category as the default and it will be pre-selected.

I also made it possible to open the “Category Management” view directly from the session timer. Before, you had to go to settings first, which was annoying if you wanted to quickly add a new category. And I added filtering options to the Timeline view, so you can now filter sessions by category or by kind (focus session, break, etc.). This makes it much easier to see patterns in your productivity.

On the technical side, I did some database optimizations that should make the app feel snappier, especially if you have a lot of recorded sessions. And I fixed the accuracy of the Live Activity timer texts, there was a small drift happening over longer sessions that was bugging me.

#### The Numbers

If you came for the numbers, here are some launch statistics so far:

- 

Total Revenue: $446

- 

MRR: $18

- 

Downloads: 794

- 

Ratings/Reviews: 26 - 4.8 stars

I’m honestly pretty happy with these numbers for a week-one launch. Obviously I’m hoping they continue to grow, but you never really know what will happen. The App Store, especially ranking for certain keywords, can be unpredictable and could potentially take many months/years.

You can also check out the most recent revenue metrics on [tryfocuskit.com/open](https://tryfocuskit.com/open/)where I’ve embedded the verified RevenueCat statistics. I’m a big fan of building in public, so everything is transparent there.
[이미지: Image]

#### Ad Campaigns

This week I also started experimenting with paid advertising to get some first eyeballs on the app.

First, I started a Reddit ad campaign targeting multiple productivity-oriented subreddits like r/GetDisciplined and r/GetStudying. These seem like the perfect audience for a focus timer app! So far I’ve spent 50€, got around 16k impressions and 92 clicks. The click-through rate is not amazing, but it’s not terrible either (at least I guess so).

The annoying part is that I can’t figure out exactly how many downloads it generated. App Store Connect doesn’t make it easy to track attribution from specific ad campaigns. If anyone has tips on this, let me know! For now, the general goal is just to get some eyes on the product. I’m not expecting the Reddit campaign to be profitable. I set a daily budget of 10€, so it’s not going to break the bank either way.

I also started an Apple Search Ads campaign targeting the keyword “Pomodoro Timer”. This one is more expensive per click, but also more targeted. I’ve spent 75€ so far and it generated 550 impressions, 60 taps and 35 installs. That’s a cost per install of around 2.14€, which I think is pretty reasonable for a first experiment. The conversion from tap to install is also really good at almost 60%, which tells me the App Store page is doing its job.

I’ll keep running both campaigns for a while and see how the numbers develop. Maybe I’ll do a deeper analysis in a future post once I have more data.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### What’s Next

For the coming week, I want to focus on getting FocusKit 1.1.0 through App Review and out to users. I’m also thinking about reaching out to some productivity YouTubers and bloggers for potential reviews. We’ll see how that goes.

Until next week!