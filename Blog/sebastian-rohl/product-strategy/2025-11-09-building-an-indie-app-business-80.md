---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/building-an-indie-app-business-80
title: "Building An Indie App Business #80"
published_at: 2025-11-09
collected_at: 2026-04-15
author: ""
lang: en
categories: ["product-strategy", "web-app", "startup-philosophy"]
extras:
  word_count: 1148
  adapter: rss
---

Sorry that I didn’t release an issue last week. I was on vacation and just couldn’t find the time to put something together, even though I wanted to. But now I’m back, much more focused, and I managed to make a lot of progress on my new Pomodoro timer app. I’m really trying hard to get everything ready for my planned launch on November 30th. Having a short break was nice, but it also made me extra motivated to push forward with the app this week.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

Quick side note: At the end of last week, [I had the chance to do an interview on IndieHackers.com](https://www.indiehackers.com/post/tech/building-a-mobile-app-portfolio-to-15k-mo-5jpsSF0k2OZKIntPYgTT), which was a really cool experience for me. If you are interested, feel free to check it out, I share a lot about my journey so far and give some insights into how I managed to launch my own mobile app business. I talk about the ups and downs, the challenges I faced, and what helped me to finally make it work. I hope it can be helpful or inspiring for someone else who is trying to achieve the same!

Back to the Pomodoro app, here is everything I achieved since the last newsletter issue:

I finalized the Insights Screen for version 1.0.0 of the app. This was a big one for me because I really wanted to give users a way to see their progress and understand their habits better. Users will be able to scroll through their complete session history and see all the statistics that matter to them. For example, they can check how many sessions they completed in total, or how much time they actually spent in Focus sessions versus Break sessions. It’s really helpful to see these numbers because sometimes you think you worked a lot, but the data tells a different story.

I also added a bar chart that visualizes all these metrics in different time periods. You can switch between week, month, year, or all-time view to see how your productivity changed over time. This makes it super easy to spot trends and see if you’re improving or not. Another thing I implemented was the category distribution chart. This one shows you how much time you spent in each category, or how many sessions you completed per category. It displays both the percentage and the absolute values.

The last feature on the Insights screen is the “Streak” card. This one is probably my favorite because it adds a bit of gamification to the whole thing. It shows your current streak, which means how many days in a row you started at least one focus session. It also displays how much time you already focused each day of the current week, so you can see your progress at a glance. But the coolest part is that you can set a weekly goal for yourself, and the card will show a progress bar that fills up as you get closer to your goal. I think this will help people stay motivated and keep coming back to the app.

I finalized the integration with the new AlarmKit APIs. Since my app will only be available for iOS 26 and above, I had the chance to use this new feature from Apple, which was really cool. Now when your session is over, you get a big alarm screen that looks almost exactly like the native iOS alarms. It reminds you that you’re done with your work session or that you need to get back to it after a break. The whole experience feels really native and polished. I also added a live activity that shows up on the lock screen and the Dynamic Island, which looks really nice. This is definitely a killer feature in my opinion, and I think users will love it.

I also put some effort into finalizing my database structure. I wanted to make it future-proof, so I added a system that can migrate to new versions automatically. SwiftData makes this super easy actually, which I’m really happy about. But the best part is that I managed to get the automatic cross-device sync working. Now I can see and manage all my focus sessions on my iPad as well, and everything stays in sync automatically. This is super convenient when you’re working on different devices throughout the day.

When I was testing the app, I seeded around 12,000 focus sessions for the past two years to see how it would perform with a lot of data. I noticed that there was a certain lag when pressing buttons, especially on the Insights tab where all the statistics are calculated. This was a problem because I want the app to feel snappy and responsive. So I invested some time to find the bottlenecks in my code and optimized everything. The app is much more performant now, even with thousands of sessions in the database.

I finished the Onboarding view this week. I tried to keep it as simple as possible, because this approach already worked really great with HabitKit. I think most people are really annoyed by long onboarding flows with unnecessary questionnaires or complex explanations. So I only have one screen that explains the purpose of the app in a simple way. Then the user taps on “Continue” and bam, they go straight into the app. The rest should be self-explanatory, and I think this is how it should be. Less is more when it comes to onboarding.

I also integrated purchases and subscriptions with RevenueCat. It was super easy to set everything up this time around. Creating offerings, product packages, and integrating it with App Store Connect is really straightforward when you’ve already done it once before. But I also noticed that RevenueCat made great improvements to their documentation. It gets easier and easier for new developers to get started, and I really like that they’re putting effort into making the developer experience better.

Of course, whenever I had only time for small tasks, I squashed a lot of bugs and made minor improvements to the UX. These small things add up over time and make the app feel more polished overall.

Do I still have a huge backlog? Yes! Am I really intimidated by it when thinking about my deadline of when I wanted to release the app? Yes! But I am super focused and motivated to bring this app THIS month in the App Store and will do my best to make it happen. Using the app itself to stay focused while working help tremendously as well.

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

Again, still have a hug amount of work to do, but let’s see how next week will turn out!