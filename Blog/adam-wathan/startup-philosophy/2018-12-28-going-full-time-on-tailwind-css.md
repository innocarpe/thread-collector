---
source: blog
creator: adam-wathan
url: https://adamwathan.me/going-full-time-on-tailwind-css
title: Going Full-Time on Tailwind CSS
published_at: 2018-12-28
collected_at: 2026-04-15
author: ""
lang: en
categories: ["startup-philosophy", "monetization", "case-study"]
extras:
  word_count: 1473
  adapter: rss
---

Late into Halloween night in 2017, we released the very first version of [Tailwind CSS](https://tailwindcss.com) — a utility-first CSS framework for rapidly developing custom user interfaces.

Since then:

- We've published [30 releases](https://github.com/tailwindcss/tailwindcss/releases)

- [77 people](https://github.com/tailwindcss/tailwindcss/graphs/contributors) have contributed to the codebase

- The [GitHub repository](https://github.com/tailwindcss/tailwindcss) has been starred over 8,000 times

- Over 1,100 people joined the Tailwind CSS [Slack community](https://join.slack.com/t/tailwindcss/shared_invite/enQtNDQ1MDYyNDA0NzA3LTAzOGEzYTRmMjE2OWUwMGViMGM2NGM5OWVmN2UzZjlmNzQ0ZTA2NGUwODYyOWMzNzM0M2MzMmE1NGYyNjk5NTI)

- Over 10,000 people started following [@tailwindcss](https://twitter.com/tailwindcss) on Twitter

- The framework has been installed almost 700,000 times via [npm](https://www.npmjs.com/package/tailwindcss)

What started as just a bunch of boilerplate I was copying and pasting between new projects has grown into a serious tool that has been adopted by some of my favorite companies, including [Algolia](https://www.algolia.com/doc/) who generously power the Tailwind documentation search.

 [이미지: Screenshot of Algolia documentation site]
 

_Algolia's [new documentation site](https://www.algolia.com/doc/), built with Tailwind CSS._

Last summer I was having a difficult time figuring out what I really wanted to be working on for the long haul.

For the past few years I've been pretty successfuly creating books and courses for other developers, but every individual project felt really short-term — just something to work on for a couple of months, leaving me to _(hopefully)_ come up with a new idea to work on when it was finished.

Not only that, but every project felt sort of disconnected and isolated: what could a video course on TDD and a CSS framework possibly have in common?

Eventually though, after re-reading [Anything You Want](https://sivers.org/a) by Derek Sivers for the _nth_ time, I realized there actually _was_ a common thread between everything I spend my time on:

_I like to help people build awesome software, and have more fun doing it._

The more I've heard from people using Tailwind CSS, the more I've realized it has the potential to be the highest impact project I've ever worked on in terms of fulfilling that goal.

**So starting in 2019, I'm going to be working full-time on Tailwind CSS.**

Here are some of the things I'm going to be working on.

## Getting to version 1.0

Tailwind has been out in the wild for over a year now, so the rough edges have become a bit more obvious and the vision for the project has continued to become more clear.

The first month or so of 2019 is going to be dedicated to polishing what we have with v0.7.3 and releasing a proper v1.0.0.

Overall I don't expect a ton of things to change, but the areas I'm paying the most attention to include:

- Consistency in both class and configuration naming

- Improving default configuration scales (the `max-width` scale could be better for example)

- Making any breaking changes that might be necessary to support planned future features

As I've always done my best to do [in the past](https://github.com/tailwindcss/tailwindcss/releases/tag/v0.7.0), the upgrade path will be as simple, clear, and painless as possible. You might need to change a couple of class names in your markup, but even with changes like that I'm planning to provide official plugins to provide backwards compatibility so you can upgrade progressively if needed.

There will be a v1.0.0 release in February for sure.

## Expanding the documentation

People always tell me our documentation is awesome but there are still a [ton](https://tailwindcss.com/docs/background-position) [of](https://tailwindcss.com/docs/background-repeat) [pages](https://tailwindcss.com/docs/height) with "Work in Progress!" banners I need to finish.

Fully finishing the API documentation will be the first thing I work on after tagging v1.0.

After that, I'm planning to add more tutorial-style documentation (like our page on [Extracting Components](https://tailwindcss.com/docs/extracting-components)), a lot more [component examples](https://tailwindcss.com/docs/examples/alerts), and a dedicated knowledge base area where I can publish articles that answer common questions that don't fit into the structure of the regular documentation.

Some of the areas I'm planning to expand the documentation include:

- More instructions for integrating Tailwind with different frameworks and build tools _(setting up Tailwind with vue-cli, nuxt.js, create-react-app, next.js, Ember, Rails, Phoenix, etc.)_

- Explaining browser support

- Explaining our Preflight styles

- Best practices for adding your own base styles

- Building themeable interfaces with Tailwind

- Sharing a Tailwind config between projects

...and a bunch more.

## Video Tutorials

Once 1.0 is out and the documentation feels solid, I'm going to be working on an official video course called "Designing with Tailwind CSS".

It will of course cover getting set up with Tailwind and explaining the features and workflow, but the bulk of it is going to focus on actually building great looking interfaces with Tailwind.

By working through a bunch of different layout and component examples, you'll learn the intricacies of CSS positioning, how to effectively use flexbox, best practices for responsive design, and a ton more.

**It will be completely free**, and I'm hoping to have it ready around April or May.

## Growing the community

Up until now we've used the [tailwindcss/discuss](https://github.com/tailwindcss/discuss/issues) repository as a makeshift discussion forum and even though it works okay, I'd like to launch a proper [Discourse](https://www.discourse.org/) forum in the new year.

I'm planning to spend a few hours every week making sure everyone's questions are answered, and hopefully my own activity in the forums will help foster a bigger and more active community where questions and answers don't disappear like they do in Slack.

I'm also planning to move our Slack community over to Discord after the success other communities like [Statamic](https://statamic.com/blog/goodbye-slack-hello-discord) and [EmberJS](https://twitter.com/tomdale/status/1075803157404508168) have had with it so we'll still have a great place for real-time chat.

## Showcasing awesome Tailwind CSS projects

Right now there are a few community-driven projects like [awesome-tailwindcss](https://github.com/aniftyco/awesome-tailwindcss), [Built with Tailwind](https://builtwithtailwind.com/), and [TailwindComponents](https://tailwindcomponents.com/) that do a great job curating beautiful Tailwind sites and third-party plugins, but I think putting together something official would go a long way towards increasing adoption.

So I'm planning to add a new section to the website that links out to third-party plugins and tools built by the community, as well as a gallery that showcases websites that are built with Tailwind.

## New features and tools

Of course I'll be continuing to develop new features for future Tailwind releases, initially focusing on some highly requested additions like:

- CSS Grid

- Transitions and animations

- Making utility variants like "hover" work with "@apply"

I've also got some ideas for additional tooling I'd like to build, like:

- A style guide generator powered by your Tailwind config file

- A playground/sandbox for creating JSFiddle/CodePen-style demos but with access to all of Tailwind's features

- A tool for building color palettes

I don't have a timeline in mind for any of that stuff, but they are ideas I'm tossing around nonetheless.

## Themes and UI kits

Out of the box Tailwind is perfect for people with a good sense for design and a solid background in CSS, but there's a huge group of people out there who _want_ to use Tailwind but would benefit from a more opinionated starting point.

Over the spring and summer I'm going to be working with [Steve Schoger](https://twitter.com/steveschoger) to put together some official themes and UI kits that will help even more people get started with Tailwind by providing predesigned HTML-based components and layouts that look great out of the box but are easy to customize.

## Sustainability

Right now I'm fortunate enough to be able to work on Tailwind full-time for a while without worrying about paying my bills, but of course that can't last forever.

Here are some of the ideas I have for making this work over the long haul:

- 

**Continue running my book/course business**

My existing products continue to sell pretty well even when I'm focused on other things, but inevitably I'll have to put some work into that business to make sure it continues to fund my time on Tailwind.

I'm planning to release an updated version of my [Test-Driven Laravel](https://course.testdrivenlaravel.com) course in 2020, as well as an updated version of [Advanced Vue Component Design](https://adamwathan.me/advanced-vue-component-design/) when Vue 3.0 is released.

- 

**Corporate sponsorship**

Much like Evan has done with [Vue.js](https://www.patreon.com/evanyou) and Taylor has done with [Laravel](https://www.patreon.com/taylorotwell), I think there is potential to fund a lot of Tailwind development through corporate sponsorship, especially once v1.0 is out and if I can continue to grow the user base.

I'm not going to explore this seriously any time soon, but it might be something to consider later in the year once my other efforts start to pay off.

- 

**Premium products**

Things like the themes and UI kits are great candidates for paid products, much like Bootstrap does with their [official theme store](https://themes.getbootstrap.com/).

This is something I'll definitely be thinking about once we get deeper into that project.

Overall I'm pretty optimistic about making this all work, but only time will tell for sure.

Either way, I'm going to give it a shot for all of 2019 and see what I can do. It'll be an exciting year for sure.