---
source: blog
creator: adam-wathan
url: https://adamwathan.me/2019/10/17/persistent-layout-patterns-in-nextjs
title: Persistent Layout Patterns in Next.js
published_at: 2019-10-17
collected_at: 2026-04-15
author: ""
lang: en
categories: ["web-app"]
extras:
  word_count: 1679
  adapter: rss
---

[Adam Wathan](/)
 
 [Articles](/articles)
 [Talks](/talks)
 [Screencasts](/screencasts)
 [Podcast](/podcast)
 [Courses](/courses)
 [Projects](/projects)
 [Journal](/journal)
 
 
 
 
 
 
 
 
 
 
 
 
 [Articles](/articles)
 [Talks](/talks)
 [Screencasts](/screencasts)
 [Podcast](/podcast)
 [Courses](/courses)
 [Projects](/projects)
 [Journal](/journal)
 
 
 
 
 
 October 17, 2019

# Persistent Layout Patterns in Next.js

 

When single-page applications were really getting popular in the early Backbone/Ember/Angular days, one of the biggest selling points was that you could navigate around your site without re-rendering the entire document from scratch every time the URL changed.

This meant you could do things like preserve the scroll position in part of the UI that didn't change (like a sidebar for example) without the complexity of measuring it and trying to restore it on the next page load like you'd have to do in a traditional server-driven application.

Because this benefit was so heavily advertised, I was very surprised to find out that in many modern single-page application frameworks like Next.js and Gatsby, **the default experience is re-rendering the entire UI every time you click a link** — throwing away that nice feeling of a persistent UI we worked so hard to achieve a decade ago!

Next.js is such a wonderfully productive development experience and produces such incredibly fast websites that I just refused to believe it had to be this way.

So I spent a few weeks researching, asking questions, and experimenting, and came up with these four patterns for persistent layouts in Next.js applications.

## The default experience

Check out this little demo app I've put together:

It's got two main sections:

- A home screen, which is just a single page.

- An account settings section, which contains a horizontally scrollable list of tabs that you can click to visit different subsections.

In this demo, the page components are constructed in the simplest, most naive way possible, where the pages themselves use the layout components they need as their own root element:

```
// /pages/account-settings/basic-information.js
import AccountSettingsLayout from '../../components/AccountSettingsLayout'

const AccountSettingsBasicInformation = () => (
  <AccountSettingsLayout>
    <div>{/* ... */}</div>
  </AccountSettingsLayout>
)

export default AccountSettingsBasicInformation

```

The problem with this approach is most obvious when you visit one of the account settings pages, scroll the list of tabs all the way to the right, and click the "Security" tab.

Notice how the tab bar jumps all the way back to the left?

That's because using this approach, the component at the top of the component tree is always the page component itself, even if the first node in each page component is the same layout component.

Because the page component changes, **React throws out all of its children and re-renders them from scratch**, meaning each page renders a brand new copy of the `SiteLayout` or `AccountSettingsLayout`, even if the previous page had already rendered that component in the same place in the DOM.

The end result is a single-page application that _feels_ like a server-driven application UI. Yuck!

## Option 1: Use a single shared layout in a custom `<App>` component

One way to add a persistent layout component to your site is to create a [custom App component](https://nextjs.org/docs#custom-app), and always render your site layout above the current page component in the component tree.

```
// /pages/_app_.js
import React from 'react'
import App from 'next/app'
import SiteLayout from './components/SiteLayout'

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props
    return (
      <SiteLayout>
        <Component {...pageProps}></Component>
      </SiteLayout>
    )
  }
}

export default MyApp

```

Here's what that looks like when applied to the demo app from earlier:

You can confirm that the `SiteLayout` component is not re-rendered by typing something into the search field, then navigating to another page.

Because the `SiteLayout` component is re-used across page transitions, whatever you type in the search field is preserved — progress!

**But we still have the tab bar scroll position problem to deal with.**

That's because using this approach, _we can only provide a single layout component_ and that component _must be shared across all pages_.

That means the wrapper component we add here has to be the lowest common denominator between all pages on the site, and our homepage doesn't use the extra UI from the `AccountSettingsLayout` so we still have to render that component as the first node in each account settings page:

```
// /pages/account-settings/basic-information.js
import AccountSettingsLayout from '../../components/AccountSettingsLayout'

const AccountSettingsBasicInformation = () => (
  <AccountSettingsLayout>
    <div>{/* ... */}</div>
  </AccountSettingsLayout>
)

export default AccountSettingsBasicInformation

```

So while this approach might work if you really only need one layout and it's used for every single page on your site, it falls apart very quickly for even the most basic of projects.

## Option 2: Render a different layout in `<App>` based on the current URL

If your needs are only slightly more complex than what's possible with a single shared layout, you might be able to get away with rendering a different tree based on the current URL.

By inspecting `router.pathname`, you can figure out which "section" of your site you're currently in, and render the corresponding layout tree:

```
// /pages/_app_.js
import React from 'react'
import App from 'next/app'
import SiteLayout from '../components/SiteLayout'
import AccountSettingsLayout from '../components/AccountSettingsLayout'

class MyApp extends App {
  render() {
    const { Component, pageProps, router } = this.props

    if (router.pathname.startsWith('/account-settings/')) {
      return (
        <SiteLayout>
          <AccountSettingsLayout>
            <Component {...pageProps}></Component>
          </AccountSettingsLayout>
        </SiteLayout>
      )
    }

    return (
      <SiteLayout>
        <Component {...pageProps}></Component>
      </SiteLayout>
    )
  }
}

export default MyApp

```

As long as you make sure you always render the entire layout tree directly in `_app.js` (don't use `SiteLayout` from within `AccountSettingsLayout` for example), this works perfectly:

Even the tabs work this way!

The downside of this approach is that your `App` component is going to be constantly churning as you add new sections to your site, and quickly grow out of control if you aren't careful about looking for opportunities to extract the route matching logic.

It also couples your layouts to your URLs, and if you ever needed to deviate (maybe `/account-settings/delete` uses a totally different layout), you need to add more and more hyper-specific conditional logic.

So while this can work well for smaller sites, for larger sites you'll want something more declarative and flexible.

## Option 3: Add a static `layout` property to your page components

One way to avoid your `App` component growing in complexity over time is to move the responsibility of defining the page layout to the page component instead of the `App` component.

You can do this by attaching a static property like `layout` (the name can be whatever you want) to your page components and reading that from inside your `App` component:

```
// /pages/account-settings/basic-information.js
import AccountSettingsLayout from '../../components/AccountSettingsLayout'

const AccountSettingsBasicInformation = () => <div>{/* ... */}</div>

AccountSettingsBasicInformation.layout = AccountSettingsLayout

export default AccountSettingsBasicInformation

```

```
// /pages/_app_.js
import React from 'react'
import App from 'next/app'

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props
    const Layout = Component.layout || (children => <>{children}</>)

    return (
      <Layout>
        <Component {...pageProps}></Component>
      </Layout>
    )
  }
}

export default MyApp

```

Here's what that looks like in action:

This is almost perfect, but there's one issue:

_The search field state is not preserved when navigating from the home page to an account settings page, or vice versa._

That's because in this example, the `AccountSettingsLayout` uses the `SiteLayout` internally, which means the actual top level layout component is switching from `SiteLayout` to `AccountSettingsLayout`, and the original `SiteLayout` is destroyed and replaced with a new instance created inside of `AccountSettingsLayout`.

If that sort of limitation isn't a problem for your site, this can be a great option. If it is, thankfully there's one more pattern we can try.

## Option 4: Add a `getLayout` function to your page components

If we use a static _function_ instead of a simple property, we can return a complex layout _tree_ instead of a single component:

```
// /pages/account-settings/basic-information.js
import SiteLayout from '../../components/SiteLayout'
import AccountSettingsLayout from '../../components/AccountSettingsLayout'

const AccountSettingsBasicInformation = () => <div>{/* ... */}</div>

AccountSettingsBasicInformation.getLayout = page => (
  <SiteLayout>
    <AccountSettingsLayout>{page}</AccountSettingsLayout>
  </SiteLayout>
)

export default AccountSettingsBasicInformation

```

Then in our custom `App` component, we can invoke that function passing in the current page to get back the entire tree:

```
// /pages/_app.js
import React from 'react'
import App from 'next/app'

class MyApp extends App {
  render() {
    const { Component, pageProps, router } = this.props

    const getLayout = Component.getLayout || (page => page)

    return getLayout(<Component {...pageProps}></Component>)
  }
}

export default MyApp

```

_(I've used the name `getLayout` in this example but it can be whatever you want — this isn't a framework feature or anything.)_

This puts each page component in charge of its entire layout, and allows an arbitrary degree of UI persistence:

### Bonus: Add a `getLayout` function to your layout components

Using this approach can mean some repetitive code in page components that use the same layout tree, and can force you to update many files if you ever need to change that tree.

One approach I've been experimenting with to avoid this duplication is to add a `getLayout` function to each layout component as well, so page components can delegate to the layout in order to fetch the complete layout tree.

```
// /components/SiteLayout.js
const SiteLayout = ({ children }) => <div>{/* ... */}</div>

export const getLayout = page => <SiteLayout>{page}</SiteLayout>

export default SiteLayout

```

```
// /components/AccountSettingsLayout.js
import { getLayout as getSiteLayout } from './SiteLayout'

const AccountSettingsLayout = ({ children }) => <div>{/* ... */}</div>

export const getLayout = page =>
  getSiteLayout(<AccountSettingsLayout>{page}</AccountSettingsLayout>)

export default AccountSettingsLayout

```

Now each page component simply imports `getLayout` from the layout it needs, and re-exports it as a static property on the page itself:

```
// /pages/account-settings/basic-information.js
import SiteLayout from '../../components/SiteLayout'
import { getLayout } from '../../components/AccountSettingsLayout'

const AccountSettingsBasicInformation = () => <div>{/* ... */}</div>

AccountSettingsBasicInformation.getLayout = getLayout

export default AccountSettingsBasicInformation

```

Here's what this looks like applied to the entire demo:

Eventually I'd love to see persistent layouts get more love as a first-class feature in Next.js, but for now hopefully these patterns will let you recreate that classic SPA user experience without having to give up all of the wonderful things Next has to offer.

If you have any questions or ideas, I'm [@adamwathan](https://twitter.com/adamwathan) on Twitter!