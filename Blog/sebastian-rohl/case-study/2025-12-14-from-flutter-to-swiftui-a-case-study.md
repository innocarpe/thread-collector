---
source: blog
creator: sebastian-rohl
url: https://sebastianroehl.substack.com/p/from-flutter-to-swiftui-a-case-study
title: From Flutter to SwiftUI - A Case Study
published_at: 2025-12-14
collected_at: 2026-04-15
author: ""
lang: en
categories: ["case-study", "web-app", "dev-tools"]
extras:
  word_count: 1955
  adapter: rss
---

When I decided to start my own business, I had only business ideas that were perfectly suited for the mobile space. I wanted to build habit trackers, workout trackers, stuff like that. The problem was that on my first real software engineering job after university I only dealt with web technologies like ASP.NET, Angular, and Azure. So I didn’t have much experience with mobile development at all.

Back at university, I was really into watching Udemy courses. One course that particularly stood out was “The Complete Flutter Development Bootcamp with Dart” by Angela Yu. It guided me through building several demo applications with Flutter and I really enjoyed it.

Coming from Angular and building SPAs on the web, Flutter instantly felt like home. The declarative approach to building UIs and the reactive state management were super similar to what I already knew. So when I decided to build my apps, I opted for Flutter. It felt like a no-brainer to have one codebase and deploy it to multiple platforms.

Since then I have built three different apps with Flutter and one in particular got really popular and was a huge success for me: HabitKit. But after a while cracks started to show, and for my new app FocusKit I decided to try SwiftUI and go all-in on the Apple ecosystem. In this article I try to explain my pain points with Flutter and what brought me to SwiftUI.

**Disclaimer:** I don’t want to blame any technology, everything has its ups and downs. I am sure most of my issues with one technology could be solved. I am just describing my experiences as an indie developer with limited time, resources and skills. Experiences may heavily differ for enterprise development teams!

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.

#### **The Flutter Honeymoon Phase**

The first 12 months of my indie app journey were a breeze, at least from a technical point of view. I built my first two apps and HabitKit got popular pretty quickly.

I was really fast developing new things and shipped so many feature updates for my apps. I was able to reuse a lot of code for different projects, which was great. The UIs of my apps were super different though and I was only able to make my second app, HabitKit, look really good in my eyes. The first one was more of a learning project.

The best part was that I was able to ship all my apps to iOS and Android at the same time. HabitKit made decent revenue on Android as well, despite the well-known fact that users on iOS are much more willing to pay for apps than Android users. At one point, the revenue share across platforms for my app business was 50-50. That’s pretty amazing if you think about it.

I also really liked the vibrant ecosystem of packages and services. Adding Firebase libraries or picking a cool state management solution was super easy and it felt like everybody was having fun with Flutter. My app HabitKit uses over 50 different external packages, which shows how rich the ecosystem is. You can find a Flutter package for almost everything (but watch out, always think about long-term maintainability)!

#### **The Cracks Start To Show**

Performance problems started to show after HabitKit got more successful. I faced the famous “Flutter Shader Compilation Jank” and even the introduction of Flutter’s new rendering engine Impeller didn’t feel like it fixed all issues. I was constantly trying to optimize my code and the calculations that each component made. I needed to be super thoughtful about how and where I updated the state. Even today, the animations still jank on certain devices when a bottom modal sheet in HabitKit gets opened or when the user has a huge amount of habits. It’s frustrating because I never found a proper solution for this.

Then there is the native code problem. With Flutter you’re able to build the core app UIs with one codebase and deploy it to multiple platforms. This sounds great in theory, but it quickly falls apart when your users want native capabilities. Home Screen widgets, Lock Screen widgets, or Shortcuts can only be implemented with native code. This forces you to maintain two additional mini-codebases and learn Swift and Kotlin and all the native APIs as well. On the iOS side of things, developing the home screen widgets for HabitKit was actually entertaining and cool, I liked it. The Android part was a huge pain to me and I always cringe in horror whenever I have to touch that code again.

Another thing that hit me was what I call the “backend problem”. Once your app gets popular and you started with a local-only database that just lives on the user’s device, people will start asking for sync. They want to use the app on multiple devices and have their data sync across them. When you’re using Flutter you’re forced to build a backend or use third-party services like Firebase or PowerSync (which also produces hard-to-determine costs that can be scary for indie app developers). When you’re using SwiftUI and focus on the Apple ecosystem, you can just enable iCloud sync for your database and you’re done. It’s so much simpler. Adding a cross-device data synchronization retroactively is super hard and a huge barrier!

The revenue split between iOS and Android also shifted over time. I did a lot of price experimenting, but never found a good combination of products and prices that could match the performance I was able to have on iOS. Nowadays the revenue split between iOS and Android is 75-25 (and the gap is growing and growing). Don’t get me wrong, 25% of my revenue is still a lot of money, but after having introduced native features like home screen widgets the “one-codebase-multiple-platforms-for-free” argument doesn’t really work anymore. I had to maintain three codebases anyway.

On top of that there were some really weird disputes with the Google review team. They threatened to remove my app from Google Play because I was linking to my newsletter in the settings. This led to some additional frustration on my end about supporting Android at all.

#### **An Honest Comparison**

Let me compare both frameworks directly. I’ve been using both for a while now and have some thoughts on the differences.

**Development Tooling:** Here Flutter has a real and huge advantage. Being able to use VSCode as your official development environment was the best decision the Flutter team could have made. Being tied to Xcode for SwiftUI is a huge turn-off and I sadly have to say that Xcode is the absolute worst IDE I ever had to work with. It’s slow, not very customizable, and the error messages are confusing. Luckily, I was able to find a weird solution that allows me to code in Cursor and only run the app in Xcode, but this doesn’t feel right and is still a disadvantage compared to Flutter.

Hot-reload on Flutter is also the best thing ever and it’s a bummer that Swift doesn’t support this. Before someone says it: using solutions like “Inject” feels more like a weird hack and doesn’t come close to the official Flutter experience. As someone coming from web development, not having hot-reload just sounds dumb in 2025. The SwiftUI Previews are super slow and never clicked for me. I always end up just running the app instead.

**Native Systems Integration:** This is where SwiftUI really shines. Shortcuts, Live Activities, Native Alarms, Dynamic Island, Lock Screen and Home Screen Widgets —> everything is easier when you’re 100% on SwiftUI. You don’t need any bridge layers, no platform channels and no weird hacks. It just works. If you want to support many native-only features in your apps, do yourself a favor and pick SwiftUI instead of Flutter.

**UI Design:** With iOS 26 Apple made a huge leap in terms of user interface design. I might be biased, but in my opinion the Liquid Glass design is the best thing that ever happened to the Apple ecosystem. I love every part of it and really wanted to add it to my app HabitKit. But because the official “Cupertino” widget library for Flutter was and still is heavily lacking, there is no way to achieve this look in a Flutter app in the near future. If you need a cross-platform solution but still want the Liquid Glass look, you’re probably better off with React Native at this point.

**Learning Curve:** If you’re coming from Flutter, SwiftUI is pretty easy to learn. Both are declarative and feel similar conceptually. So there wasn’t a huge barrier of entry for me. The real pain is actually learning the ecosystem, the native APIs and how to deal with the terrible documentation. In terms of learning resources and documentation, Flutter has the lead by far. The Apple stuff is sparse and often outdated. The most valuable resources are WWDC videos which is pretty weird to be honest. I don’t want to watch a 45 minute video when I’m just trying to understand how an API works.

**Long Term Maintainability:** SwiftUI will always be a first-class citizen on Apple platforms. There is no threat of Apple killing the framework. I know there were some rumors about Google not being 100% behind Flutter anymore and this is pretty scary for an indie app developer. You don’t want to invest years into a technology that might be abandoned. With SwiftUI I feel more secure about the future of my apps.

#### **Conclusion**

So, should you switch from Flutter to SwiftUI? It really depends on your situation.

If you’re just starting out and want to build apps for both iOS and Android with one codebase, Flutter is still a great choice. The developer experience is really good, you can move fast, and you can reach both platforms from day one. Just be aware that once you want to add native features like widgets, you’ll have to write platform-specific code anyway.

If most of your users are on iOS, if you want to use all the cool native features that Apple provides, and if you’re okay with only supporting Apple devices, then SwiftUI is probably the better choice. The integration with the Apple ecosystem is just so much smoother and you don’t have to deal with maintaining multiple codebases.

For me personally, the switch was worth it. FocusKit is built entirely in SwiftUI and the development experience has been great, despite the terrible tooling. I can use all the native features without any workarounds and I don’t have to worry about Android-specific bugs anymore. The Liquid Glass design looks amazing on FocusKit and I couldn’t have achieved this with Flutter.

I still maintain HabitKit in Flutter and I’m not planning to rewrite it. That would be a huge undertaking and the app works fine as it is. But for all my future projects, I’ll probably stick with SwiftUI, although I can’t guarantee it! Right now, the peace of mind of being fully native is worth a lot to me though.

At the end of the day, both are good technologies. Pick the one that fits your needs and your business goals. And don’t be afraid to switch if your situation changes. I did it and I don’t regret it. When it comes to React Native, I can’t give you advice on that because I never worked with it.

PS: This will be the last newsletter issue before my huge “Year In Review 2025” article on Dec 31st!

Thanks for reading Building A Profitable App Business! Subscribe for free to receive new posts and support my work.