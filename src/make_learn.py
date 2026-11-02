"""Write the Learn pages (hub, five lessons, resources, storybook reader) into src/pages/."""
import html, json, pathlib

SRC = pathlib.Path(__file__).parent / 'pages'
E = html.escape

LESSONS = [
    {
        'slug': 'learn-climate', 'art': 'learn-climate', 'n': 1, 'mins': 5, 'short': 'Climate change basics',
        'title': 'Why is our planet getting warmer?',
        'lead': 'Climate change explained with a blanket, a sunny day and a few simple ideas.',
        'sections': [
            ('Weather or climate?', ['Weather is what the sky is doing today: sunny, cloudy, rainy or windy. Climate is the usual weather of a place over many years, usually 30 years or more.', 'One hot day is weather. Hotter years, again and again, are a change in climate.']),
            ('Earth’s warm blanket', ['Earth is wrapped in a thin layer of air. Some gases in that air, such as carbon dioxide, work like a blanket: they keep some of the sun’s heat in.', 'That is a good thing. Without it, Earth would be far too cold for people, plants and animals.']),
            ('Why the blanket is getting thicker', ['When people burn coal, oil and gas for cars, factories and electricity, they add more carbon dioxide to the air. Cutting down forests adds more too, because trees soak it up.', 'A thicker blanket traps more heat, so Earth warms. It is now more than 1°C warmer than about 150 years ago. That sounds small, but for a whole planet it is a lot.']),
            ('What it means in Kenya', ['A warmer planet changes the rains. Some places get longer dry spells, which are hard for farmers and herders. Others get heavier rain and floods. Very hot days come more often too.']),
            ('The good news', ['We know what causes climate change, so we know how to slow it. Kenya already makes most of its electricity from clean sources, like geothermal steam from under the Rift Valley, water and wind.', 'Planting trees, saving energy and walking or cycling all help.']),
        ],
        'words': [('Weather', 'What the sky is doing today.'), ('Climate', 'The usual weather of a place over many years.'), ('Carbon dioxide', 'A gas in the air. Burning coal, oil and gas makes lots of it.'), ('Greenhouse effect', 'The way some gases keep heat in, like a blanket.'), ('Fossil fuels', 'Coal, oil and gas, formed from plants and animals that lived long ago.')],
        'facts': [('Where does most of Kenya’s electricity come from?', 'Clean sources: geothermal steam from deep underground, plus water, wind and sunshine.'), ('Is a little warming a big deal?', 'Yes. More than 1°C sounds small, but for a whole planet it changes rain, heat and seasons.'), ('Do trees help?', 'Yes. Trees take in carbon dioxide from the air as they grow.')],
        'try': ('Weather diary', 'For one week, draw the weather every morning: sun, clouds, rain or wind. At the end, ask an older relative what the weather was like when they were your age.'),
        'quiz': [
            ('What is climate?', [('What the sky is doing right now', False), ('The usual weather of a place over many years', True), ('A kind of cloud', False)], 'Weather is today. Climate is the pattern over many years.'),
            ('Which gas works like a blanket around Earth?', [('Oxygen', False), ('Carbon dioxide', True), ('Steam from a kettle', False)], 'Carbon dioxide and other greenhouse gases keep heat in.'),
            ('What makes the blanket thicker?', [('Burning coal, oil and gas', True), ('Planting trees', False), ('Riding a bicycle', False)], 'Burning fossil fuels adds carbon dioxide. Trees and bicycles help!'),
        ],
        'book': True,
    },
    {
        'slug': 'learn-biodiversity', 'art': 'learn-biodiversity', 'n': 2, 'mins': 5, 'short': 'Biodiversity',
        'title': 'The web of life.',
        'lead': 'Biodiversity means all the different living things on Earth. Here is why every one of them matters.',
        'sections': [
            ('What is biodiversity?', ['“Bio” means life and “diversity” means many different kinds. Biodiversity is all the plants, animals, insects, fungi and tiny microbes on Earth, and the places where they live.']),
            ('Everything is connected', ['Living things depend on each other, like threads in a web. Bees carry pollen from flower to flower, so plants can make fruits and seeds, like mangoes and avocados.', 'Birds spread those seeds, and new trees grow. Pull one thread, and others are affected.']),
            ('Kenya is full of life', ['Kenya has savannahs with giraffes and lions, Kakamega Forest (a tropical rainforest in western Kenya), Lake Nakuru with its flamingos, and coral reefs at Watamu on the coast.']),
            ('What harms it, and how we help', ['Cutting down forests, plastic and rubbish, pollution and climate change all harm wildlife.', 'We help by planting indigenous trees, growing flowers for bees and keeping rubbish out of nature. Kenya plans to grow 15 billion trees by 2032.']),
        ],
        'words': [('Biodiversity', 'All the different kinds of life on Earth.'), ('Habitat', 'The home where a plant or animal lives.'), ('Pollinator', 'An animal, like a bee or butterfly, that carries pollen between flowers.'), ('Indigenous tree', 'A tree that grows naturally in Kenya.'), ('Ecosystem', 'Living things and their surroundings, working together.')],
        'facts': [('Why do bees matter for lunch?', 'Bees and other pollinators help many fruits grow, like mangoes and avocados.'), ('How many trees does Kenya plan to grow?', '15 billion by 2032. Every school tree counts!'), ('Where are Kenya’s coral reefs?', 'Along the coast, like the reefs at Watamu, home to bright fish and sea turtles.')],
        'try': ('Nature hunt', 'In 10 minutes, how many different plants, insects and birds can you spot around your school? Draw your three favourites.'),
        'quiz': [
            ('What does biodiversity mean?', [('Only wild animals', False), ('All the different kinds of life on Earth', True), ('Big forests only', False)], 'Biodiversity is every kind of living thing, big and tiny.'),
            ('What do bees do for plants?', [('They eat the leaves', False), ('They carry pollen so plants can make fruits and seeds', True), ('They water them', False)], 'Pollination is how many flowers become fruit.'),
            ('Which helps biodiversity?', [('Planting indigenous trees', True), ('Burning rubbish', False), ('Throwing plastic in rivers', False)], 'Indigenous trees give local animals food and homes.'),
        ],
    },
    {
        'slug': 'learn-justice', 'art': 'learn-justice', 'n': 3, 'mins': 4, 'short': 'Climate justice',
        'title': 'Is climate change fair?',
        'lead': 'Climate justice is about fairness: who caused the problem, who is hurt most, and who gets a say.',
        'sections': [
            ('Not everyone caused it equally', ['Countries that burned the most coal, oil and gas for many years caused most of climate change. Africa produces only about 4 out of every 100 parts of the world’s greenhouse gases.']),
            ('Not everyone is hurt equally either', ['Many communities in Africa face droughts and floods, even though they did little to cause them. Families who farm, keep animals or live near rivers often feel it first.']),
            ('Children have the most at stake', ['Children did the least to cause climate change, but they will live with it the longest. Yet they are rarely asked what they think when big decisions are made.']),
            ('What climate justice asks for', ['Those who caused more do more to cut pollution and to help others get ready. People most at risk are protected first. And everyone, including children, gets a say.']),
        ],
        'quote': ('Children aren’t just victims of climate change. We’re problem solvers.', 'Alana Chelangat, founder of Dunia Endelevu'),
        'words': [('Justice (haki)', 'Fairness. In Kiswahili, haki also means rights.'), ('Emissions', 'Gases released into the air, like smoke from burning fuel.'), ('Climate finance', 'Money that helps countries cut pollution and get ready for climate change.'), ('Vulnerable', 'More likely to be harmed.')],
        'facts': [('How much of the world’s greenhouse gases come from Africa?', 'About 4 out of every 100 parts.'), ('Who did the least to cause climate change?', 'Children, yet they will live with it the longest.'), ('What is the Kiswahili word for justice?', 'Haki. It also means rights and fairness.')],
        'try': ('Fairness talk', 'Imagine your class shares one water tank, and one class uses most of the water. What would be fair? Now talk about how that is like our planet.'),
        'quiz': [
            ('Climate justice is mostly about…', [('Fairness', True), ('Weather forecasts', False), ('Football', False)], 'It asks who caused the problem, who is hurt, and who decides.'),
            ('About how much of the world’s greenhouse gases does Africa produce?', [('Half', False), ('About 4 out of every 100 parts', True), ('Most of it', False)], 'Africa produces very little, yet many communities are hit hard.'),
            ('What should children have in climate decisions?', [('Nothing', False), ('A say', True), ('Only homework', False)], 'Children will live with these decisions the longest.'),
        ],
    },
    {
        'slug': 'learn-rights', 'art': 'learn-rights', 'n': 4, 'mins': 4, 'short': 'Environmental rights',
        'title': 'Your right to a healthy environment.',
        'lead': 'Clean air, clean water and a safe place to live are not just nice to have. In Kenya, they are your right.',
        'sections': [
            ('What are rights?', ['Rights are things every person should have and be protected to have, like education, health and safety. Children have rights too.']),
            ('Kenya’s Constitution', ['Article 42 of Kenya’s Constitution (2010) says every person has the right to a clean and healthy environment. That includes you.']),
            ('Around the world', ['In 2022, the United Nations agreed that a clean, healthy and sustainable environment is a human right. In 2023, a United Nations committee on children’s rights said governments must protect children from harm to the environment, including climate change.', 'Children also have the right to be heard on things that affect them.']),
            ('Rights come with responsibilities', ['Kenya’s Constitution also says every person has a duty to help protect and look after the environment.', 'If the environment near you is harmed, tell a trusted adult. Adults can report it to the county government or to NEMA, Kenya’s environment authority.']),
        ],
        'words': [('Right', 'Something every person should have and be protected to have.'), ('Responsibility', 'Something you should do to help others and the planet.'), ('Constitution', 'The most important set of rules for a country.'), ('NEMA', 'The National Environment Management Authority, which looks after Kenya’s environment.')],
        'facts': [('Which part of Kenya’s Constitution protects your environment?', 'Article 42: the right to a clean and healthy environment.'), ('When did the United Nations call a healthy environment a human right?', 'In 2022.'), ('Can children speak up about the environment?', 'Yes. Children have the right to be heard on things that affect them.')],
        'try': ('Rights detective', 'With your teacher, find one place near your school that is not clean or healthy. Together, write a polite letter suggesting how to fix it.'),
        'quiz': [
            ('Article 42 of Kenya’s Constitution gives every person the right to…', [('A clean and healthy environment', True), ('Free sweets', False), ('A new phone', False)], 'Article 42 protects the environment you live in.'),
            ('Rights come with…', [('Responsibilities', True), ('Nothing at all', False), ('Only homework', False)], 'Every person has a duty to help protect the environment.'),
            ('You see dangerous rubbish near your school. What do you do first?', [('Ignore it', False), ('Tell a trusted adult', True), ('Clean it up alone', False)], 'Adults can make it safe and report it.'),
        ],
    },
    {
        'slug': 'learn-action', 'art': 'learn-action', 'n': 5, 'mins': 5, 'short': 'Climate action',
        'title': 'What can we do?',
        'lead': 'Climate action means slowing climate change, and getting ready for the changes already here.',
        'sections': [
            ('Two kinds of action', ['Some actions cut the pollution that warms the planet: saving energy, using clean energy and planting trees.', 'Others help us get ready for changes: saving rainwater for dry times, planting shade trees and warning people early about very hot days or heavy rain.']),
            ('At home', ['Switch off lights and devices nobody is using. Turn off the tap while you brush your teeth. Reuse and repair things instead of throwing them away.']),
            ('At school', ['Grow a tree nursery. Alana, our founder, co-founded a school tree nursery with more than 20,000 trees. Compost food scraps, collect rainwater, and start an environment club or a daily weather board.']),
            ('Use your voice', ['Write a story, speak at assembly or ask a question on a podcast. Dunia Endelevu helps children do all three, for free.']),
            ('The world is acting too', ['In 2015, almost every country agreed to work together to slow global warming. This is called the Paris Agreement. Kenya banned plastic carrier bags in 2017.']),
        ],
        'words': [('Mitigation', 'Cutting the pollution that causes climate change.'), ('Adaptation', 'Getting ready for the changes climate change brings.'), ('Renewable energy', 'Energy that does not run out, like sun, wind, water and geothermal.'), ('Compost', 'Food scraps that rot down into rich soil.')],
        'facts': [('When did Kenya ban plastic carrier bags?', 'In 2017.'), ('How many trees grow in the school nursery Alana co-founded?', 'More than 20,000.'), ('What is the Paris Agreement?', 'In 2015, almost every country agreed to work together to slow global warming.')],
        'try': ('Class climate pledge', 'Each pupil chooses one action for a month. Track it on a class chart and celebrate together at the end.'),
        'quiz': [
            ('Collecting rainwater for the dry season is an example of…', [('Getting ready for changes', True), ('Making pollution', False), ('Weather', False)], 'Saving water helps families and schools cope with dry spells.'),
            ('Which action saves energy?', [('Switching off lights nobody is using', True), ('Leaving the TV on all day', False), ('Opening the fridge again and again', False)], 'Every light switched off saves energy.'),
            ('In 2015, almost every country agreed to…', [('Work together to slow global warming', True), ('Stop all rain', False), ('Ban bicycles', False)], 'That agreement is called the Paris Agreement.'),
        ],
    },
]

ORDER = [l['slug'] for l in LESSONS] + ['learn-resources']
TITLES = {l['slug']: l['short'] for l in LESSONS}
TITLES['learn-resources'] = 'Learn more'

BOOK_PAGES = 10
BOOK_TEXT = json.load(open(pathlib.Path(__file__).parent / 'book_text.json'))


def lesson_page(L):
    i = ORDER.index(L['slug'])
    nxt = ORDER[i + 1]
    out = ['<main id="main">', '']
    out.append(f'''  <section class="wrap lesson-hero" aria-labelledby="lesson-title">
    <div class="lesson-hero__copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="learn.html">Learn</a><span aria-hidden="true">›</span><span aria-current="page">{E(L['short'])}</span></nav>
      <span class="tag tag--start">Lesson {L['n']} · {L['mins']} min read</span>
      <h1 id="lesson-title" class="h1 split">{E(L['title'])}</h1>
      <p class="lead">{E(L['lead'])}</p>
    </div>
    <figure class="lesson-hero__art art-scene">{{{{art:{L['art']}}}}}</figure>
  </section>
''')
    secs = []
    for h, paras in L['sections']:
        ps = ''.join(f'<p>{E(p)}</p>' for p in paras)
        secs.append(f'        <section class="lesson__sec reveal"><h2 class="h3">{E(h)}</h2>{ps}</section>')
    quote = ''
    if L.get('quote'):
        q, who = L['quote']
        quote = f'\n        <blockquote class="quote reveal"><p>“{E(q)}”</p><footer>{E(who)}</footer></blockquote>'
    words = ''.join(f'<div><dt>{E(w)}</dt><dd>{E(d)}</dd></div>' for w, d in L['words'])
    book = ''
    if L.get('book'):
        book = '''
        <a class="side-book" href="story-baraka.html">
          <picture><source type="image/webp" srcset="assets/books/baraka/cover.webp"><img src="assets/books/baraka/cover.jpg" alt="" width="800" height="1236" loading="lazy"></picture>
          <span><span class="card3__num">Storybook</span><strong>Baraka and the Warm Blanket</strong><span class="more">Read the book <span class="arrow">{{arrow}}</span></span></span>
        </a>'''
    out.append(f'''  <div class="wrap lesson">
    <article class="lesson__body">
{chr(10).join(secs)}{quote}
    </article>
    <aside class="lesson__side">
      <div class="words">
        <h2 class="label">Words to know</h2>
        <dl>{words}</dl>
      </div>{book}
    </aside>
  </div>
''')
    facts = ''.join(f'''
      <button class="fact" type="button" aria-pressed="false"><span class="fact__front"><span class="fact__kicker">Did you know?</span><strong>{E(q)}</strong><span class="fact__hint">Tap to find out</span></span><span class="fact__back">{E(a)}</span></button>''' for q, a in L['facts'])
    out.append(f'''  <section class="wrap section" aria-labelledby="facts-title">
    <div class="center-head"><span class="tag">Did you know?</span><h2 id="facts-title" class="h2 h2--sm">Three quick facts.</h2></div>
    <div class="facts">{facts}
    </div>
  </section>
''')
    t_title, t_body = L['try']
    qs = []
    for qi, (q, opts, why) in enumerate(L['quiz'], start=1):
        buttons = ''.join(f'<button class="opt" type="button"{" data-correct" if ok else ""}>{E(o)}</button>' for o, ok in opts)
        qs.append(f'''
        <div class="q"><p class="q__text"><span class="q__n">{qi}</span>{E(q)}</p><div class="q__opts">{buttons}</div><p class="q__why" hidden>{E(why)}</p></div>''')
    out.append(f'''  <section class="wrap section" aria-label="Activity and quiz">
    <div class="lesson-do">
      <div class="try reveal">
        <span class="tag tag--start">Try this</span>
        <h2 class="h2 h2--sm">{E(t_title)}</h2>
        <p class="lead">{E(t_body)}</p>
      </div>
      <div class="quiz reveal" data-quiz>
        <h2 class="h3">Quick quiz</h2>{''.join(qs)}
        <p class="quiz__score" aria-live="polite" hidden></p>
        <button class="btn btn--ghost btn--sm quiz__again" type="button" hidden>Try again</button>
      </div>
    </div>
  </section>
''')
    out.append(f'''  <nav class="wrap section lesson-next" aria-label="Next lesson">
    <a class="next-card" href="{nxt}.html"><span class="label">Next{' lesson' if nxt != 'learn-resources' else ''}</span><strong>{E(TITLES[nxt])}</strong><span class="circle-btn" aria-hidden="true">{{{{arrow}}}}</span></a>
  </nav>

</main>
''')
    return '\n'.join(out)


def hub_page():
    cards = []
    for L in LESSONS:
        cards.append(f'''      <a class="topic reveal" href="{L['slug']}.html">
        <div class="topic__art art-scene">{{{{art:{L['art']}}}}}</div>
        <div class="topic__body"><span class="card3__num">Lesson {L['n']}{' · Start here' if L['n'] == 1 else ''}</span><h3 class="h3">{E(L['short'])}</h3><p>{E(L['lead'])}</p><span class="track__go">{L['mins']} min read <span class="arrow">{{{{arrow}}}}</span></span></div>
      </a>''')
    cards.append('''      <a class="topic topic--sun reveal" href="learn-resources.html">
        <div class="topic__art art-scene">{{art:learn-resources}}</div>
        <div class="topic__body"><span class="card3__num">For everyone</span><h3 class="h3">Learn more</h3><p>Books, podcasts, games and real science for curious children, parents and teachers.</p><span class="track__go">Explore <span class="arrow">{{arrow}}</span></span></div>
      </a>''')
    return f'''<main id="main">

  <section class="wrap page-hero" aria-labelledby="learn-title">
    <div class="panel">
      <span class="chip">Learn</span>
      <h1 id="learn-title" class="h1 split">Big climate ideas, made simple.</h1>
      <p class="lead">Short lessons, storybooks and quizzes for curious children, parents and teachers. Free to use at home and in class.</p>
    </div>
  </section>

  <section class="wrap section" aria-labelledby="book-title" style="padding-top: clamp(48px, 6vw, 80px)">
    <div class="book-feature reveal">
      <a class="book-feature__cover" href="story-baraka.html" aria-label="Read Baraka and the Warm Blanket">
        <picture><source type="image/webp" srcset="assets/books/baraka/cover.webp"><img src="assets/books/baraka/cover.jpg" alt="Cover of Baraka and the Warm Blanket: a boy with glasses and a sketchbook, his grandmother and a green chameleon on a farm" width="1600" height="1236"></picture>
      </a>
      <div class="book-feature__copy stack stack--lg">
        <span class="tag tag--start">New storybook · Ages 6–10</span>
        <h2 id="book-title" class="h2">Baraka and the Warm Blanket</h2>
        <p class="lead">A boy, his grandmother and a chameleon who turns orange when he’s too hot explain why our planet is warming.</p>
        <div class="btn-row">
          <a class="btn btn--sun" href="story-baraka.html">Read the book {{{{arrow}}}}</a>
          <a class="btn btn--ghost" href="assets/books/baraka/baraka-and-the-warm-blanket.pdf" download>Download PDF (2 MB)</a>
        </div>
        <p class="fine">Story by Dunia Endelevu. Illustrated with AI (Gemini).</p>
      </div>
    </div>
  </section>

  <section class="wrap section" aria-labelledby="lessons-title">
    <div class="center-head">
      <span class="tag">Lessons</span>
      <h2 id="lessons-title" class="h2">Five lessons, one at a time.</h2>
      <p class="lead">Each lesson has a story, three quick facts, an activity and a quiz.</p>
    </div>
    <div class="topics">
{chr(10).join(cards)}
    </div>
  </section>

  <section class="wrap section" aria-labelledby="listen-title">
    <div class="panel panel--dark listen reveal">
      <div class="stack stack--lg">
        <span class="chip">Listen</span>
        <h2 id="listen-title" class="h2 h2--sm">Learn by listening.</h2>
        <p class="lead">Climate Gumzo is our podcast, where young hosts ask the questions children really have.</p>
        <div class="btn-row"><a class="btn btn--sun" href="{{{{spotify}}}}" target="_blank" rel="noopener">Listen on Spotify {{{{arrow}}}}</a></div>
      </div>
      <div class="listen__art art-scene" aria-hidden="true">{{{{duo:mic}}}}</div>
    </div>
  </section>

  <section class="wrap section" aria-labelledby="teach-title">
    <div class="panel panel--sun cta reveal">
      <div class="stack stack--lg">
        <h2 id="teach-title" class="h2">Teaching with these lessons?</h2>
        <p class="lead">Use them freely in class. We can also bring a Dunia Endelevu session to your school.</p>
        <div class="btn-row"><a class="btn btn--ink" href="contact.html?topic=school#enquiry">Book a school session {{{{arrow}}}}</a></div>
      </div>
      <div class="cta__deco" aria-hidden="true">{{{{mark_white}}}}</div>
    </div>
  </section>

</main>
'''


RESOURCES = [
    ('Our storybook', 'Baraka and the Warm Blanket', 'Read our first storybook online, or download it to print.', 'story-baraka.html', False),
    ('Our podcast', 'Climate Gumzo', 'Young hosts and climate experts chat about big ideas in simple words.', '{{spotify}}', True),
    ('A book by our founder', 'Alana’s Magical Adventure at Mazingira Park', 'The first book in Alana Chelangat’s Climate Action Adventure Series.', 'https://samogera.github.io/alanachelangat/writing.html', True),
    ('Games and explainers', 'NASA Climate Kids', 'Games, videos and simple articles about weather, climate, energy and nature.', 'https://climatekids.nasa.gov/', True),
    ('Real science for schools', 'The GLOBE Program', 'Students collect real environmental data, like air and soil temperature, and share it with scientists.', 'https://www.globe.gov/', True),
    ('Today’s weather', 'Kenya Meteorological Department', 'Official weather forecasts and warnings for every county in Kenya.', 'https://meteo.go.ke/', True),
    ('Today’s air', 'AirQo', 'Air quality readings from monitors in African cities, including Nairobi.', 'https://airqo.org/', True),
    ('Children’s rights', 'UNICEF: children’s right to a healthy environment', 'How the United Nations asked governments to protect children from environmental harm and climate change.', 'https://www.unicef.org/press-releases/un-committee-rights-child-calls-states-take-action-first-guidance-childrens-rights', True),
]


def resources_page():
    cards = []
    for i, (kind, title, desc, url, ext) in enumerate(RESOURCES):
        attrs = ' target="_blank" rel="noopener"' if ext else ''
        sun = ' tile--sun' if i in (0, 3) else ''
        cards.append(f'      <a class="tile{sun} reveal" href="{url}"{attrs}><span class="card3__num">{E(kind)}</span><h3 class="h3">{E(title)}</h3><p>{E(desc)}</p><span class="track__go">{"Visit" if ext else "Read"} <span class="arrow">{{{{arrow}}}}</span></span></a>')
    return f'''<main id="main">

  <section class="wrap lesson-hero" aria-labelledby="res-title">
    <div class="lesson-hero__copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="learn.html">Learn</a><span aria-hidden="true">›</span><span aria-current="page">Learn more</span></nav>
      <span class="tag tag--start">Educational resources</span>
      <h1 id="res-title" class="h1 split">Learn more.</h1>
      <p class="lead">Books, podcasts, games and real science for curious children, parents and teachers. Explore them with a grown-up.</p>
    </div>
    <figure class="lesson-hero__art art-scene">{{{{art:learn-resources}}}}</figure>
  </section>

  <section class="wrap section" aria-label="Resources" style="padding-top: clamp(40px, 5vw, 64px)">
    <div class="grid-2">
{chr(10).join(cards)}
    </div>
    <p class="fine" style="margin-top: 18px">Links to other websites open in a new tab. Dunia Endelevu is not responsible for their content.</p>
  </section>

  <section class="wrap section" aria-labelledby="teach-title">
    <div class="panel panel--sun cta reveal">
      <div class="stack stack--lg">
        <h2 id="teach-title" class="h2">Back to the lessons.</h2>
        <div class="btn-row"><a class="btn btn--ink" href="learn.html">All lessons {{{{arrow}}}}</a></div>
      </div>
      <div class="cta__deco" aria-hidden="true">{{{{mark_white}}}}</div>
    </div>
  </section>

</main>
'''


def book_page():
    pages = []
    for i in range(1, BOOK_PAGES + 1):
        text = BOOK_TEXT[str(i)]
        alt = 'Cover: Baraka and the Warm Blanket, by Dunia Endelevu.' if i == 1 else f'Page {i}. {text}'
        load = '' if i <= 2 else ' loading="lazy"'
        pages.append(f'        <figure class="reader__page" data-page="{i}"><picture><source type="image/webp" srcset="assets/books/baraka/page-{i:02d}.webp"><img src="assets/books/baraka/page-{i:02d}.jpg" alt="{E(alt)}" width="1600" height="1236"{load}></picture></figure>')
    text_items = ''.join(f'<li>{E(BOOK_TEXT[str(i)])}</li>' for i in range(2, BOOK_PAGES + 1))
    return f'''<main id="main">

  <section class="wrap book-head" aria-labelledby="book-title">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="learn.html">Learn</a><span aria-hidden="true">›</span><span aria-current="page">Storybook</span></nav>
    <h1 id="book-title" class="h1">Baraka and the Warm Blanket</h1>
    <p class="lead">A Dunia Endelevu storybook about climate change, for ages 6 to 10.</p>
  </section>

  <section class="wrap reader-wrap" aria-label="Storybook reader">
    <div class="reader" data-reader>
      <div class="reader__pages">
{chr(10).join(pages)}
      </div>
      <div class="reader__bar">
        <button class="reader__btn" type="button" data-prev aria-label="Previous page">{{{{arrow}}}}</button>
        <span class="reader__count" aria-live="polite"><span data-count>1</span> of {BOOK_PAGES}</span>
        <button class="reader__btn reader__btn--next" type="button" data-next aria-label="Next page">{{{{arrow}}}}</button>
      </div>
    </div>
    <div class="book-actions">
      <a class="btn btn--sun" href="assets/books/baraka/baraka-and-the-warm-blanket.pdf" download>Download PDF (2 MB) {{{{arrow}}}}</a>
      <a class="btn btn--ghost" href="learn-climate.html">Do the lesson</a>
    </div>
    <p class="fine book-credit">Story by Dunia Endelevu. Illustrated with AI (Gemini). Free to read, print and share for learning.</p>
    <details class="book-text">
      <summary>Read the story as text</summary>
      <ol>{text_items}</ol>
    </details>
  </section>

</main>
'''


for L in LESSONS:
    (SRC / f"{L['slug']}.html").write_text(lesson_page(L))
(SRC / 'learn.html').write_text(hub_page())
(SRC / 'learn-resources.html').write_text(resources_page())
(SRC / 'story-baraka.html').write_text(book_page())
print('wrote', len(LESSONS) + 3, 'pages')
