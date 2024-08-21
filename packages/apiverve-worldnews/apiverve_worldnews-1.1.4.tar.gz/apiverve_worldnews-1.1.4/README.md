World News API
============

News API is a simple tool for scraping news data. It returns the news title, description, and more.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [World News API](https://apiverve.com/marketplace/api/news)

---

## Installation
	pip install apiverve-worldnews

---

## Configuration

Before using the news API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The World News API documentation is found here: [https://docs.apiverve.com/api/news](https://docs.apiverve.com/api/news).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_worldnews.apiClient import NewsAPIClient

# Initialize the client with your APIVerve API key
api = NewsAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = { "category": "technology" }
```

###### Simple Request

```
# Make a request to the API
result = api.execute(query)

# Print the result
print(result)
```

###### Example Response

```
{
  "status": "ok",
  "error": null,
  "data": {
    "date": "2024-08-14",
    "category": "technology",
    "articleCount": 60,
    "articles": [
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "Microsoft Issues Patches for 90 Flaws, Including 10 Critical Zero-Day Exploits",
        "pubDate": "Wed, 14 Aug 2024 11:18:00 +0530",
        "description": "Microsoft on Tuesday shipped fixes to address a total of 90 security flaws, including 10 zero-days, of which six have come under active exploitation in the wild. Of the 90 bugs, seven are rated Critical, 79 are rated Important, and one is rated Moderate in severity. This is also in addition to 36 vulnerabilities that the tech giant resolved in its Edge browser since last month. The Patch Tuesday",
        "link": "https://thehackernews.com/2024/08/microsoft-issues-patches-for-90-flaws.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "Critical Flaw in Ivanti Virtual Traffic Manager Could Allow Rogue Admin Access",
        "pubDate": "Wed, 14 Aug 2024 10:48:00 +0530",
        "description": "Ivanti has rolled out security updates for a critical flaw in Virtual Traffic Manager (vTM) that could be exploited to achieve an authentication bypass and create rogue administrative users. The vulnerability, tracked as CVE-2024-7593, has a CVSS score of 9.8 out of a maximum of 10.0. \"Incorrect implementation of an authentication algorithm in Ivanti vTM other than versions 22.2R1 or 22.7R2",
        "link": "https://thehackernews.com/2024/08/critical-flaw-in-ivanti-virtual-traffic.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "China-Backed Earth Baku Expands Cyber Attacks to Europe, Middle East, and Africa",
        "pubDate": "Wed, 14 Aug 2024 10:31:00 +0530",
        "description": "The China-backed threat actor known as Earth Baku has diversified its targeting footprint beyond the Indo-Pacific region to include Europe, the Middle East, and Africa starting in late 2022. Newly targeted countries as part of the activity include Italy, Germany, the U.A.E., and Qatar, with suspected attacks also detected in Georgia and Romania. Governments, media and communications, telecoms,",
        "link": "https://thehackernews.com/2024/08/china-backed-earth-baku-expands-cyber.html"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " Google's new Pixel Screenshots takes an active (and safe) approach to organizing your digital life ",
        "pubDate": "Wed, 14 Aug 2024 04:30:00 +0000",
        "description": "Exclusive to the Pixel 9 series, the new app can automatically save screengrabs complete with URLs inside entries.",
        "link": "https://www.techradar.com/computing/software/googles-new-pixel-screenshots-takes-an-active-and-safe-approach-to-organizing-your-digital-life"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "Buying the Google Pixel 9 Pro from these retailers gets you a free gift card (up to $350)",
        "pubDate": "Wed, 14 Aug 2024 03:49:00 +0000",
        "description": "The new Google Pixel 9 series is available for preorders, and early-bird shoppers can receive a free gift card worth hundreds.",
        "link": "https://www.zdnet.com/article/buying-the-google-pixel-9-pro-from-these-retailers-gets-you-a-free-gift-card-up-to-350/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " Google is making Gemini AI part of everything you do with your smartphone – here's how ",
        "pubDate": "Wed, 14 Aug 2024 02:00:34 +0000",
        "description": "Google embeds Gemini AI throughout mobile devices.",
        "link": "https://www.techradar.com/computing/artificial-intelligence/google-is-making-gemini-ai-part-of-everything-you-do-with-your-smartphone-and-heres-5-ways-itll-do-that"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "Google's new Pixel Screenshots may be the feature that finally converts me to use AI",
        "pubDate": "Wed, 14 Aug 2024 00:52:00 +0000",
        "description": "It won't turn my boring office background into a field of flowers, but being able to parse through hundreds of screenshots with a few clicks feels like a major win.",
        "link": "https://www.zdnet.com/article/googles-new-pixel-screenshots-may-be-the-feature-that-finally-converts-me-to-use-ai/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Valve confirms it'll support the ROG Ally with its Steam Deck operating system",
        "pubDate": "2024-08-14T00:15:10Z",
        "description": "Valve once imagined that every PC maker could have their own \"Steam Machine,\" a PC game console running the company's Linux-based SteamOS. It took a decade for that dream to evolve into the company's own internally developed Steam Deck gaming handheld, but the original dream isn't dead.  The company's long said it plans to let other companies use SteamOS, too — and that means explicitly supporting the rival Asus ROG Ally gaming handheld, Valve designer Lawrence Yang now confirms to The Verge. A few days ago, some spotted an intriguing line in Valve's latest SteamOS release notes: “Added support for extra ROG Ally keys.” We didn't know Valve was supporting any ROG Ally keys at all, let alone extras!  Maybe Valve was just supporting those... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219469/valve-steamos-asus-rog-ally-steady-progress-dual-boot"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "U.S. Considers Breaking Up Google to Address Search Monopoly",
        "pubDate": "Tue, 13 Aug 2024 23:45:38 +0000",
        "description": "The Justice Department and state attorneys general are discussing various scenarios to remedy Google’s dominance in online search, including a breakup of the company.",
        "link": "https://www.nytimes.com/2024/08/13/technology/google-monopoly-antitrust-justice-department.html"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "Google Pixel 9's new AI photo-editing features can fix just about any poorly-captured image",
        "pubDate": "Tue, 13 Aug 2024 23:29:00 +0000",
        "description": "From improved zooming to AI-powered group photos, here are the Pixel 9's greatest hits.",
        "link": "https://www.zdnet.com/article/google-pixel-9s-new-ai-photo-editing-features-can-fix-just-about-any-poorly-captured-image/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " Quordle today – hints and answers for Wednesday, August 14 (game #933) ",
        "pubDate": "Tue, 13 Aug 2024 23:02:00 +0000",
        "description": "Looking for Quordle clues? We can help. Plus get the answers to Quordle today and past solutions.",
        "link": "https://www.techradar.com/computing/websites-apps/quordle-today-answers-clues-14-august-2024"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " NYT Strands today — hints, answers and spangram for Wednesday, August 14 (game #164) ",
        "pubDate": "Tue, 13 Aug 2024 23:02:00 +0000",
        "description": "Looking for NYT Strands answers and hints? Here's all you need to know to solve today's game, including the spangram.",
        "link": "https://www.techradar.com/computing/websites-apps/nyt-strands-today-answers-hints-14-august-2024"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "6 AI features Google thinks will sell you on its latest Pixel phones (including the Fold)",
        "pubDate": "Tue, 13 Aug 2024 22:45:00 +0000",
        "description": "New tools including Call Summary and Pixel Screenshots take the Pixel 9 series' AI capabilities to the next level.",
        "link": "https://www.zdnet.com/article/6-ai-features-google-thinks-will-sell-you-on-its-latest-pixel-phones-including-the-fold/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "ChatGPT Advanced Voice Mode First Impressions: Fun, and Just a Bit Creepy",
        "pubDate": "Tue, 13 Aug 2024 22:39:34 +0000",
        "description": "The new voice feature from OpenAI for ChatGPT is often entertaining and will even do a Trump impression. It likely rolls out to all paid users this fall.",
        "link": "https://www.wired.com/story/chatgpt-advanced-voice-mode-first-impressions/"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "I went hands-on with every Google Pixel 9 model, and this is the one you should buy",
        "pubDate": "Tue, 13 Aug 2024 22:38:00 +0000",
        "description": "The new Google Pixel 9 series has slimmer, flatter designs, improved camera hardware, and AI features that you may actually want to use.",
        "link": "https://www.zdnet.com/article/i-went-hands-on-with-every-google-pixel-9-model-and-this-is-the-one-you-should-buy/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "Report: DoJ may want to break up Google",
        "pubDate": "Tue, 13 Aug 2024 22:24:29 +0000",
        "description": "In an unexpected move, Bloomberg reports, the Justice Department may be considering busting Google up.",
        "link": "https://www.zdnet.com/article/report-doj-may-want-to-break-up-google/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "I went hands-on with Google's $1,799 Pixel 9 Pro Fold, and I'm ready to switch from Samsung",
        "pubDate": "Tue, 13 Aug 2024 22:12:00 +0000",
        "description": "The successor to one of last year's best foldable phones is lighter, brighter, still expensive, and full of potential.",
        "link": "https://www.zdnet.com/article/i-went-hands-on-with-googles-1799-pixel-9-pro-fold-and-im-ready-to-switch-from-samsung/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Every time Google dinged Apple during its Pixel 9 launch event",
        "pubDate": "2024-08-13T21:55:53Z",
        "description": "Photo by Chris Welch / The Verge          In between the reveal of new Pixel phones and AI features at its event today, Google snuck in a few burns targeted at Apple. Some were subtle — others far from it. While it’s not uncommon for companies like Google to draw comparisons to competitors during big events like this, Google seemed to sprinkle references to Apple all throughout its showcase. Maybe that’s because Google has become especially competitive in the AI industry, which Apple has only just barely begun to dip into. Here are all the moments of comparison that we caught during the event. Gemini is going “far beyond English speakers” Image: Google       Gemini is available globally in 45 different languages.    When introducing Gemini, Sameer Samat, the... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219764/google-dinged-apple-pixel-9-launch-event"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Elections Officials Battle a Deluge of Disinformation",
        "pubDate": "Tue, 13 Aug 2024 21:50:39 +0000",
        "description": "County clerks and secretaries of state are overwhelmed this year, as they stare down a “perpetual moving target” of new conspiracy theories, political pressure and threats.",
        "link": "https://www.nytimes.com/2024/08/12/business/media/2024-election-disinformation.html"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Florida sued over its ban on lab-grown meat",
        "pubDate": "2024-08-13T21:41:10Z",
        "description": "Photo by Carolyn Fong for The Washington Post via Getty Images          Upside Foods, a cultivated meat firm, sued Florida over its ban on lab-grown meat, arguing that the state’s legislation prohibiting the sale of cultivated meat is unconstitutional.  Florida Governor Ron DeSantis signed the ban into law in May, describing the legislation as a way of “fighting back against the global elite’s plan to force the world to eat meat grown in a petri dish or bugs to achieve their authoritarian goals.” In a lawsuit filed in federal court on Monday, Upside Foods and the Institute of Justice, a nonprofit public interest law firm, allege that Florida’s lab-grown meat ban is about protecting the state’s cattle industry — and that the law is unconstitutional. The complaint claims SB 1084 violates the Supremacy and... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219779/florida-lab-grown-meat-lawsuit-upside-foods"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Artists’ lawsuit against Stability AI and Midjourney gets more punch",
        "pubDate": "2024-08-13T21:35:28Z",
        "description": "Illustration by Cath Virginia / The Verge | Photos from Getty Images          A lawsuit that several artists filed against Stability AI, Midjourney, and other AI-related companies can proceed with some claims dismissed, a judge ruled yesterday. Many artists allege that popular generative AI services violated copyright law by training on a dataset that included their works and, in some cases, that users of these services can directly reproduce copies of the work. Last year, Judge William Orrick allowed a direct copyright infringement complaint against Stability, operator of the popular Stable Diffusion AI image generator. But he dismissed a variety of other claims and asked the artists’ attorneys to amend them with more detail.  In this more recent ruling, the revised arguments convinced the judge to approve an... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219520/stability-midjourney-artist-lawsuit-copyright-trademark-claims-approved"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "In 1997, the BBC asked Jeff Bezos when internet shopping would take off",
        "pubDate": "2024-08-13T21:16:35Z",
        "description": "Jeff Bezos appearing in a 27-year-old report by the BBC on internet shopping. | Screenshot: YouTube          Earlier this year, Amazon reported $143.3 billion in revenue for the first quarter of 2024. But 27 years ago, the BBC wondered when predictions that the internet revolutionizing shopping would come true, speaking to local bakers, booksellers, and even Jeff Bezos to find out. The Money Programme report, which originally aired in November of 1997, was recently added to the BBC Archive YouTube Channel. In it, reporter Nils Blythe takes a simulated journey on the information superhighway — complete with wonderfully dated ‘90s-era blue screen effects and graphics — and speaks to retailers who had varying levels of success with online commerce at the time.   Those included a small bakery in the UK that was enjoying several thousands of dollars... Continue reading…",
        "link": "https://www.theverge.com/24219730/jeff-bezos-amazon-bbc-archive-shopping"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "How Google’s new Pixel 9 phones differ from one another (and don’t)",
        "pubDate": "2024-08-13T21:00:00Z",
        "description": "The base Pixel 9 is one of four new models, starting at $799. | Image: Google          At its most recent Made by Google event, the monopolistic search giant announced four new phones: the Pixel 9, Pixel 9 Pro, Pixel 9 Pro XL, and Pixel 9 Pro Fold. This is more phones than Google has ever sold at once — especially when you throw in the midrange Pixel 8A from May — making the decision on which to get somewhat confusing.   So, we thought it might be helpful to explain the key differences and similarities between the four new models and succinctly lay out all the finer specs for you to peruse. Hopefully, this will help you choose between the new Pixels, which are set to launch in waves on August 22nd and September 4th. The biggest differences between Pixel 9 phones: price and size What immediately separates most of the Pixel 9... Continue reading…",
        "link": "https://www.theverge.com/24216079/google-pixel-9-pro-xl-fold-comparison-specs-price-features"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "Google Pixel 9 Pro Fold vs. OnePlus Open: Which one should you buy?",
        "pubDate": "Tue, 13 Aug 2024 20:48:00 +0000",
        "description": "Google just unveiled its newest foldable smartphone, but it faces stiff competition from the OnePlus Open. Let's break down the pros and cons of both.",
        "link": "https://www.zdnet.com/article/google-pixel-9-pro-fold-vs-oneplus-open-which-one-should-you-buy/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Paramount is shutting down its TV studio as part of a new wave of layoffs",
        "pubDate": "2024-08-13T20:45:19Z",
        "description": "Image: Paramount          Ahead of its upcoming merger with Skydance Media, Paramount is winding down its TV production studio as part of a larger restructuring effort that will put 15 percent of its current workforce out of jobs. In a memo sent to employees today and obtained by The Hollywood Reporter, Paramount TV head Nicole Clemens and Paramount co-CEO George Cheeks announced that Paramount Global is shuttering the studio. Clemens, who joined Paramount in 2018 following former exec Amy Powell’s sudden exit, is also set to leave the company, and all of Paramount’s currently airing TV series and projects still in development will transition to CBS Studios. In the memo, Clemens and Cheeks insisted that while Paramount TV is coming to an end, “our ethos will live... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219776/paramount-tv-studios-shut-down-cbs-layoffs"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Google Unveils Pixel 9 Phones to Beat Apple’s iPhone",
        "pubDate": "Tue, 13 Aug 2024 20:41:24 +0000",
        "description": "The internet giant unveiled the next generation of Pixel phones, headphones and watches to stand out in a hardware market that has mostly ignored it.",
        "link": "https://www.nytimes.com/2024/08/13/technology/google-pixel-9.html"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "Lost in translation: AI chatbots still too English-language centric, Stanford study finds",
        "pubDate": "Tue, 13 Aug 2024 20:40:32 +0000",
        "description": "Human preferences and experiences are not universal, and AI chatbots need to reflect that.",
        "link": "https://www.zdnet.com/article/lost-in-translation-ai-chatbots-still-too-english-language-centric-stanford-study-finds/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "Latest news",
        "title": "The best AI for coding in 2024 (and what not to use)",
        "pubDate": "Tue, 13 Aug 2024 20:34:00 +0000",
        "description": "I've been subjecting AI chatbots to a set of real-world programming tests. Which chatbots handled the challenge and which crawled home in shame? Read on.",
        "link": "https://www.zdnet.com/article/the-best-ai-for-coding/#ftag=RSSbaffb68"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Texas judge who owns Tesla stock recuses himself from X’s advertiser lawsuit",
        "pubDate": "2024-08-13T20:18:15Z",
        "description": "Illustration by Laura Normand / The Verge          A Texas judge who was assigned two cases involving Elon Musk’s X platform has recused himself from one of them, shortly after a report that he owns stock in Tesla.  US District Court Judge Reed O’Connor was assigned to X’s recent antitrust lawsuit against advertisers over their boycott of the service, as well as a separate case against Media Matters, which the company sued for a report showing that X displayed ads from major brands next to pro-Nazi content. On Tuesday, O’Connor filed a notice to the court clerk recusing himself from the antitrust lawsuit. He still appears to be assigned to the Media Matters case as of Tuesday afternoon. The recusal came just a few days after NPR reported on O’Connor’s Tesla stock holdings, which, a... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219740/texas-judge-reed-oconnor-tesla-stock-x-antitrust-lawsuit"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Google’s finally rolling out the Zoom Enhance camera trick it announced last year",
        "pubDate": "2024-08-13T20:14:37Z",
        "description": "Photo by Allison Johnson / The Verge          Apparently, turning the cliched “enhance!” meme into reality wasn’t as easy as Google might have initially expected. Today, the company confirmed in a blog post that Zoom Enhance is finally rolling out to the Pixel 8 Pro and will also be present on the Pixel 9 Pro, 9 Pro XL, and 9 Pro Fold at launch.  Google announced the AI-powered Zoom Enhance during last year’s Made by Google event, but we’ve made it all the way to a new generation of phones, and only now is the software feature ready for release. “When you pinch in, Zoom Enhance can intelligently sharpen and enhance the details of your images, so you can get closer than ever, even when you forget to zoom” is how Google’s hardware chief, Rick Osterloh, explained the feature last... Continue reading…",
        "link": "https://www.theverge.com/2024/8/13/24219750/google-zoom-enhance-pixel-8-9-pro-feature"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "UAW Files Federal Labor Charges Against Donald Trump and Elon Musk, Alleging They Tried to ‘Threaten and Intimidate Workers’",
        "pubDate": "Tue, 13 Aug 2024 20:12:07 +0000",
        "description": "During their conversation on X Spaces, Trump seemed to praise Musk for firing striking workers. Those remarks may violate labor law.",
        "link": "https://www.wired.com/story/uaw-donald-trump-elon-musk-labor-charges/"
      },
      {
        "category": "technology",
        "website": "The Verge -  All Posts",
        "title": "Here’s how the new Pixel Watch 3 stacks up against Google’s last-gen model",
        "pubDate": "2024-08-13T20:00:00Z",
        "description": "Google’s latest wearable is both bigger and brighter than its predecessors. | Image: Google          Now that Google has officially announced the Pixel Watch 3 after a deluge of leaks and rumors, Android users have even more wearables to choose from. Google’s latest smartwatch will arrive on September 10th and start at $349.99, with the last-gen Pixel Watch 2 hanging around for $249.99. Sadly, Google has dropped the original model from its lineup, though you can still buy it on sale from third-party retailers.   With almost identical names and similar domed displays, it can be confusing to distinguish which watch is which — never mind which to buy. Yet, they’re more different than they appear, with each wearable offering more features and capabilities than its predecessor. The new Pixel Watch 3 offers several advanced running features,... Continue reading…",
        "link": "https://www.theverge.com/24218577/google-pixel-watch-3-vs-2-comparison-specs-price"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "Kamala Harris' Rally Crowds Aren't AI-Generated. Here's How You Can Tell",
        "pubDate": "Tue, 13 Aug 2024 19:36:45 +0000",
        "description": "Conspiracy theories have shot up around images of surging crowds for Harris-Walz campaign events. But all it takes is a little research to prove the photos are real.",
        "link": "https://www.wired.com/story/kamala-harris-rally-crowds-ai-trump-conspiracy/"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "The 42 Best Shows on Hulu Right Now (August 2024)",
        "pubDate": "Tue, 13 Aug 2024 19:00:00 +0000",
        "description": "The Bear, Futurama, and Solar Opposites just a few of the shows you should be watching on Hulu this month.",
        "link": "https://www.wired.com/story/best-tv-shows-hulu-this-week/"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "Thousands of People Are Playing the Mysterious Game ‘Deadlock’ Right Now",
        "pubDate": "Tue, 13 Aug 2024 18:30:55 +0000",
        "description": "No official details exist yet for Deadlock, the rumored 6v6 team shooter from Valve. That hasn’t stopped people from playing it on Steam.",
        "link": "https://www.wired.com/story/valve-deadlock-secret-game-thousands-playing/"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " Google Gemini Live is the first AI that almost encourages you to be rude ",
        "pubDate": "Tue, 13 Aug 2024 18:16:34 +0000",
        "description": "Google launches Gemini Live AI assistant that users can interrupt and converse with like a human.",
        "link": "https://www.techradar.com/computing/artificial-intelligence/google-gemini-live-is-the-first-ai-that-almost-encourages-you-to-be-rude"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Musk’s Trump Talk on X: After Glitchy Start, a Two-Hour Ramble",
        "pubDate": "Tue, 13 Aug 2024 17:43:21 +0000",
        "description": "Problems in the livestream renewed questions about X’s ability to handle big events, but it also showed how the platform can still grab attention.",
        "link": "https://www.nytimes.com/2024/08/13/technology/elon-musk-x-donald-trump.html"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " Windows 11 art lovers, take note: Paint 3D’s days are numbered – so make sure you download it from the Microsoft Store while you still can ",
        "pubDate": "Tue, 13 Aug 2024 17:01:41 +0000",
        "description": "Microsoft is canning Paint 3D when November 2024 rolls around, so download the app while it’s still available!",
        "link": "https://www.techradar.com/computing/windows/windows-11-art-lovers-take-note-paint-3ds-days-are-numbered-so-make-sure-you-download-it-from-the-microsoft-store-while-you-still-can"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "Google’s New Pixel Watch 3 Can Detect a Loss of Pulse",
        "pubDate": "Tue, 13 Aug 2024 17:00:00 +0000",
        "description": "The company’s wearables technicians talk about pioneering new health advances, along with the challenges they’ve faced and the successes they’ve earned after a decade of Wear OS.",
        "link": "https://www.wired.com/story/google-new-pixel-watch-3-can-detect-a-loss-of-pulse/"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "For Google’s Pixel Camera Team, It’s All About the Memories",
        "pubDate": "Tue, 13 Aug 2024 17:00:00 +0000",
        "description": "In exclusive interviews, Google’s Pixel imaging team explains how its new camera tech can capture a photo that’s more realistic and natural—and how its new AI tools can reimagine an entire scene.",
        "link": "https://www.wired.com/story/google-pixel-9-real-tone-pixel-camera-interview/"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "Google Pixel 9, Pixel 9 Pro Fold, Pixel Watch 3, Pixel Buds Pro 2: Specs, Features, Release Date",
        "pubDate": "Tue, 13 Aug 2024 17:00:00 +0000",
        "description": "The Pixel 9 series now features four phones, including the Pixel 9 Pro Fold, alongside the Pixel Watch 3 and Pixel Buds Pro 2.",
        "link": "https://www.wired.com/story/made-by-google-pixel-9-phones-pixel-watch-3-pixel-buds-pro-2/"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "The Google Pixel 9’s AI Camera Features Let You Reshape Reality",
        "pubDate": "Tue, 13 Aug 2024 17:00:00 +0000",
        "description": "Add Me, Reimagine, Autoframe, and Zoom Enhance—these camera features allow you to alter your photos with zero technical know-how.",
        "link": "https://www.wired.com/story/all-the-new-generative-ai-camera-features-in-google-pixel-9-phones/"
      },
      {
        "category": "technology",
        "website": "Wired",
        "title": "Lawsuit Attacks Florida’s Lab-Grown Meat Ban as Unconstitutional",
        "pubDate": "Tue, 13 Aug 2024 16:47:31 +0000",
        "description": "Upside Foods, a leading cultivated-meat company, argues that the ban violates the US Constitution in several ways.",
        "link": "https://www.wired.com/story/upside-foods-institute-of-justice-cultivated-lab-grown-meat-lawsuit-florida-ron-desantis/"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " The first macOS Sequoia beta with Apple Intelligence just landed, but only a select few can try it out ",
        "pubDate": "Tue, 13 Aug 2024 16:00:32 +0000",
        "description": "Apple drops macOS Sequoia 15.1 beta 2, which finally brings long-awaited AI features.",
        "link": "https://www.techradar.com/computing/mac-os/the-first-macos-sequoia-beta-with-apple-intelligence-just-landed-but-only-a-select-few-can-try-it-out"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "GhostWrite: New T-Head CPU Bugs Expose Devices to Unrestricted Attacks",
        "pubDate": "Tue, 13 Aug 2024 19:32:00 +0530",
        "description": "A team of researchers from the CISPA Helmholtz Center for Information Security in Germany has disclosed an architectural bug impacting Chinese chip company T-Head's XuanTie C910 and C920 RISC-V CPUs that could allow attackers to gain unrestricted access to susceptible devices. The vulnerability has been codenamed GhostWrite. It has been described as a direct CPU bug embedded in the hardware, as",
        "link": "https://thehackernews.com/2024/08/ghostwrite-new-t-head-cpu-bugs-expose.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "Researchers Uncover Vulnerabilities in AI-Powered Azure Health Bot Service",
        "pubDate": "Tue, 13 Aug 2024 18:30:00 +0530",
        "description": "Cybersecurity researchers have discovered two security flaws in Microsoft's Azure Health Bot Service that, if exploited, could permit a malicious actor to achieve lateral movement within customer environments and access sensitive patient data. The critical issues, now patched by Microsoft, could have allowed access to cross-tenant resources within the service, Tenable said in a new report shared",
        "link": "https://thehackernews.com/2024/08/researchers-uncover-vulnerabilities-in_0471960302.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "Why Hardsec Matters: From Protecting Critical Services to Enhancing Resilience",
        "pubDate": "Tue, 13 Aug 2024 16:26:00 +0530",
        "description": "Traditionally, the focus has been on defending against digital threats such as malware, ransomware, and phishing attacks by detecting them and responding. However, as cyber threats become more sophisticated. There is a growing recognition of the importance of measures that stop new attacks before they are recognized. With high-value assets, it’s not good enough to have the protection, it’s",
        "link": "https://thehackernews.com/2024/08/why-hardsec-matters-from-protecting.html"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " New version of Nvidia RTX 4070 graphics card spotted with slower VRAM – here’s why that might just be a good thing ",
        "pubDate": "Tue, 13 Aug 2024 10:44:54 +0000",
        "description": "Leak shows a tamer version of Nvidia’s RTX 4070 GPU could be on shelves soon – dare we hope that it’s cheaper?",
        "link": "https://www.techradar.com/computing/gpu/new-version-of-nvidia-rtx-4070-graphics-card-spotted-with-slower-vram-heres-why-that-might-just-be-a-good-thing"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " Apple Maps could be plotting a big update to help it compete with Google Maps' Street View ",
        "pubDate": "Tue, 13 Aug 2024 10:24:33 +0000",
        "description": "Expect Look Around to be looking around more places and more countries in the not-too-distant future.",
        "link": "https://www.techradar.com/computing/websites-apps/apple-maps-could-be-plotting-a-big-update-to-help-it-compete-with-google-maps-street-view"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "FBI Shuts Down Dispossessor Ransomware Group's Servers Across U.S., U.K., and Germany",
        "pubDate": "Tue, 13 Aug 2024 14:34:00 +0530",
        "description": "The U.S. Federal Bureau of Investigation (FBI) on Monday announced the disruption of online infrastructure associated with a nascent ransomware group called Radar/Dispossessor. The effort saw the dismantling of three U.S. servers, three United Kingdom servers, 18 German servers, eight U.S.-based criminal domains, and one German-based criminal domain. Dispossessor is said to be led by individual(",
        "link": "https://thehackernews.com/2024/08/fbi-shuts-down-dispossessor-ransomware.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "Ukraine Warns of New Phishing Campaign Targeting Government Computers",
        "pubDate": "Tue, 13 Aug 2024 10:42:00 +0530",
        "description": "The Computer Emergency Response Team of Ukraine (CERT-UA) has warned of a new phishing campaign that masquerades as the Security Service of Ukraine to distribute malware capable of remote desktop access. The agency is tracking the activity under the name UAC-0198. More than 100 computers are estimated to have been infected since July 2024, including those related to government bodies in the",
        "link": "https://thehackernews.com/2024/08/ukraine-warns-of-new-phishing-campaign.html"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Tether Co-Founder Faces the Unraveling of a Crypto Dream",
        "pubDate": "Tue, 13 Aug 2024 04:01:30 +0000",
        "description": "Brock Pierce arrived in Puerto Rico seven years ago, promising to use crypto magic to revitalize the local economy. Now he’s mired in legal disputes and fighting with his business partners.",
        "link": "https://www.nytimes.com/2024/08/13/technology/brock-pierce-crypto-puerto-rico.html"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Fact-Checking Trump’s Talk With Elon Musk on X",
        "pubDate": "Tue, 13 Aug 2024 04:00:31 +0000",
        "description": "Fact-checking Donald Trump’s claims about immigration, Vice President Kamala Harris, President Biden and more.",
        "link": "https://www.nytimes.com/2024/08/12/us/politics/trump-musk-x-fact-check.html"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "X Spaces With Trump and Musk Is Off to a Glitchy Start",
        "pubDate": "Tue, 13 Aug 2024 00:37:00 +0000",
        "description": "The audio livestream of a conversation between Elon Musk and the former president ran late as users scrambled to try to access the site.",
        "link": "https://www.nytimes.com/2024/08/12/technology/trump-musk-x-spaces-interview.html"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Trump Returns to X in Victory for Elon Musk",
        "pubDate": "Mon, 12 Aug 2024 20:09:24 +0000",
        "description": "The former president posted a campaign video ahead of a scheduled interview on the platform with Mr. Musk, who reinstated Mr. Trump’s account shortly after buying the site in 2022.",
        "link": "https://www.nytimes.com/2024/08/12/technology/donald-trump-elon-musk-x.html"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Elon Musk Is Using X to Push His Views, and Donald Trump",
        "pubDate": "Mon, 12 Aug 2024 19:46:00 +0000",
        "description": "Mr. Musk has become a vocal supporter of Mr. Trump. It wasn’t always that way.",
        "link": "https://www.nytimes.com/2024/08/12/technology/elon-musk-political-views.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "How Phishing Attacks Adapt Quickly to Capitalize on Current Events",
        "pubDate": "Mon, 12 Aug 2024 16:50:00 +0530",
        "description": "In 2023, no fewer than 94 percent of businesses were impacted by phishing attacks, a 40 percent increase compared to the previous year, according to research from Egress. What's behind the surge in phishing? One popular answer is AI – particularly generative AI, which has made it trivially easier for threat actors to craft content that they can use in phishing campaigns, like malicious emails",
        "link": "https://thehackernews.com/2024/08/how-phishing-attacks-adapt-quickly-to.html"
      },
      {
        "category": "technology",
        "website": "The Hacker News",
        "title": "Researchers Uncover Vulnerabilities in Solarman and Deye Solar Systems",
        "pubDate": "Mon, 12 Aug 2024 16:00:00 +0530",
        "description": "Cybersecurity researchers have identified a number of security shortcomings in photovoltaic system management platforms operated by Chinese companies Solarman and Deye that could enable malicious actors to cause disruption and power blackouts. \"If exploited, these vulnerabilities could allow an attacker to control inverter settings that could take parts of the grid down, potentially causing",
        "link": "https://thehackernews.com/2024/08/researchers-uncover-vulnerabilities-in.html"
      },
      {
        "category": "technology",
        "website": "NYT > Technology",
        "title": "Brands Love Influencers (Until Politics Get Involved)",
        "pubDate": "Mon, 12 Aug 2024 09:02:46 +0000",
        "description": "Marketing firms are using artificial intelligence to help analyze influencers and predict whether they will opine about the election.",
        "link": "https://www.nytimes.com/2024/08/12/business/media/influencers-politics-ai-analysis.html"
      },
      {
        "category": "technology",
        "website": " TechRadar - All the latest technology news ",
        "title": " NYT Wordle today — answer and hints for game #1152, Wednesday, August 14 ",
        "pubDate": "Tue, 14 Feb 2023 09:56:57 +0000",
        "description": "Looking for Wordle hints? We can help. Plus get the answers to Wordle today and yesterday.",
        "link": "https://www.techradar.com/news/wordle-today"
      }
    ]
  },
  "code": 200
}
```

---

## Customer Support

Need any assistance? [Get in touch with Customer Support](https://apiverve.com/contact).

---

## Updates
Stay up to date by following [@apiverveHQ](https://twitter.com/apiverveHQ) on Twitter.

---

## Legal

All usage of the APIVerve website, API, and services is subject to the [APIVerve Terms of Service](https://apiverve.com/terms) and all legal documents and agreements.

---

## License
Licensed under the The MIT License (MIT)

Copyright (&copy;) 2024 APIVerve, and Evlar LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.