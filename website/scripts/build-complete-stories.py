import json, os, re

EXTRACTED_FILE = 'scripts/extracted_content.json' if os.path.exists('scripts/extracted_content.json') else 'website/scripts/extracted_content.json'
STORIES_DIR = 'src/content/stories' if os.path.exists('src/content/stories') else 'website/src/content/stories'

os.makedirs(STORIES_DIR, exist_ok=True)

with open(EXTRACTED_FILE, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

def clean_text(t, title=""):
    if not t:
        return ""
    # Normalize common broken quote artifacts and encoding issues
    t = t.replace('\ufffd', "'").replace('â€™', "'").replace('â€œ', '"').replace('â€ ', '"')
    t = t.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    # Split paragraphs by double newline
    paras = [p.strip() for p in re.split(r'\n{2,}', t) if p.strip()]
    
    # If the first paragraph repeats the title or author byline, remove it
    if paras and title:
        norm_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
        norm_p0 = re.sub(r'[^a-zA-Z0-9]', '', paras[0].lower())
        if norm_title and (norm_p0 in norm_title or norm_title in norm_p0) and len(norm_p0) > 5:
            paras = paras[1:]
        elif norm_p0 in ['bydhanushree', 'bymithraa', 'byaradhana', 'dhanushree', 'mithraa', 'aradhana', 'by aradhana', 'by dhanushree', 'by mithraa']:
            paras = paras[1:]

    merged_paras = []
    for p in paras:
        if merged_paras and re.search(r'[,;:\-–—\(\'\"“a-z]$', merged_paras[-1]) and not p.startswith('#') and not p.startswith('- ') and not re.match(r'^\d+[\.\)]', p):
            merged_paras[-1] = merged_paras[-1] + ' ' + p
        else:
            merged_paras.append(p)

    # Clean double spaces in each paragraph
    cleaned_paras = [re.sub(r'[ \t]+', ' ', p).strip() for p in merged_paras if p.strip()]
    return '\n\n'.join(cleaned_paras)

stories_specs = [
    # 1. Blog Aradhana
    {
        "slug": "never-ending-reincarnations-artist",
        "title": "The Never-Ending Reincarnations of an Artist",
        "section": "lifestyle",
        "format": "blog",
        "author": "Aradhana",
        "authorRole": "Essayist & Cultural Critic",
        "subtitle": "How continuous reinvention, vulnerability, and experimentation shape the creative journey across an artist's lifetime.",
        "excerpt": "A personal essay on the cycles of creative renewal, creative doubts, and the ongoing labor of artistic reinvention.",
        "heroImage": {
            "src": "/media/photos/blog-aradhana-artist-reincarnations.jpg",
            "alt": "Artist workspace with oil paintings, canvases, and palettes in sunlit studio",
            "caption": "An artist's contemplative studio atelier reflecting continuous reinvention and creative craft.",
            "credit": "Fine Art Photography"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Blog']['docs'].get('Aradhana.docx', ''))
    },

    # 2. Blog Dhanushree
    {
        "slug": "finding-marakkave-ninaikiren",
        "title": "Finding 'Marakkave Ninaikiren': A Journey Through Pain, Resilience, and Human Emotion",
        "section": "lifestyle",
        "format": "blog",
        "author": "Dhanushree",
        "authorRole": "Literary Critic & Essayist",
        "subtitle": "A reflective reading of wartime trauma, displacement, and feminine survival in Tamil literature.",
        "excerpt": "An essay on 'Marakkave Ninaikiren', exploring how literature preserves the visceral memories of war and personal resilience.",
        "heroImage": {
            "src": "/media/photos/blog-dhanushree-marakkave.jpg",
            "alt": "Book cover of Marakkave Ninaikiren",
            "caption": "Cover edition of 'Marakkave Ninaikiren', chronicling war, resilience, and personal testimony.",
            "credit": "Literary Archive"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Blog']['docs'].get('Dhanushree.pdf', ''))
    },

    # 3. Blog Mithraa
    {
        "slug": "is-it-a-privilege",
        "title": "Is It a Privilege?",
        "section": "lifestyle",
        "format": "blog",
        "author": "Mithraa",
        "authorRole": "Student Essayist",
        "subtitle": "Interrogating unexamined social capital, generational comfort, and everyday advantages in contemporary youth culture.",
        "excerpt": "A candid essay examining how privilege operates unnoticed until contrasted with systemic inequality.",
        "heroImage": {
            "src": "/media/photos/blog-mithraa-privilege.jpeg",
            "alt": "Reflective visual on socioeconomic perspective and privilege",
            "caption": "Reflections on social mobility, structural advantages, and perspective.",
            "credit": "Society & Culture Desk"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Blog']['docs'].get('Mithraa.pdf', ''))
    },

    # 4. Lifestyle Aradhana
    {
        "slug": "dalit-vegan-food-culture",
        "title": "A Dalit Vegan in a Country Where Food's Never Just Food",
        "section": "lifestyle",
        "format": "article",
        "author": "Aradhana",
        "authorRole": "Food & Culture Correspondent",
        "subtitle": "Navigating dietary politics, caste identity, and culinary heritage in urban contemporary India.",
        "excerpt": "An inquiry into how food choices intersect with caste history, family traditions, and ethical eating in modern India.",
        "heroImage": {
            "src": "/media/photos/lifestyle-aradhana-dalit-vegan.jpg",
            "alt": "Traditional culinary spices, lentils, and cookware",
            "caption": "Regional cooking vessels and plant-based culinary traditions in southern India.",
            "credit": "Culinary Documentation"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Lifestyle-Entertainment']['docs'].get('Aradhana.docx', ''))
    },

    # 5. Lifestyle Dhanushree
    {
        "slug": "striking-the-balance-pa-ranjith",
        "title": "Striking the Balance: Why Pa. Ranjith’s ‘Natchathiram Nagargiradhu’ Redefined Romantic Cinema",
        "section": "lifestyle",
        "format": "article",
        "author": "Dhanushree",
        "authorRole": "Cinema & Arts Critic",
        "subtitle": "A critical examination of caste, theatrical form, and radical love in Tamil contemporary film.",
        "excerpt": "How Pa. Ranjith dismantled conventional cinematic romance by placing caste politics and progressive theater at its emotional core.",
        "heroImage": {
            "src": "/media/photos/lifestyle-dhanushree-natchathiram.jpg",
            "alt": "Promotional artwork from Pa. Ranjith's Natchathiram Nagargiradhu",
            "caption": "Pa. Ranjith's 'Natchathiram Nagargiradhu' blends theatrical performance with radical discussions on love and caste.",
            "credit": "Cinema Archive"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Lifestyle-Entertainment']['docs'].get('Dhanushree.pdf', ''))
    },

    # 6. Lifestyle Mithraa
    {
        "slug": "male-loneliness-epidemic",
        "title": "Is There Really a 'Male Loneliness Epidemic'?",
        "section": "lifestyle",
        "format": "article",
        "author": "Mithraa",
        "authorRole": "Society & Culture Reporter",
        "subtitle": "Dissecting social media discourse, emotional isolation, and the structural realities of young men's relationships.",
        "excerpt": "Investigating whether modern male loneliness is an unprecedented sociological crisis or a reflection of changing social patterns.",
        "heroImage": {
            "src": "/media/photos/lifestyle-mithraa-male-loneliness.jpeg",
            "alt": "Young adult sitting outdoors in thought",
            "caption": "Urban isolation and relational disconnection among contemporary youth.",
            "credit": "Society & Culture Desk"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Lifestyle-Entertainment']['docs'].get('Mithraa.pdf', ''))
    },

    # 7. National Aradhana
    {
        "slug": "el-nino-india-climate-vulnerability",
        "title": "El Niño Highlights India's Growing Climate Vulnerability",
        "section": "national",
        "format": "article",
        "author": "Aradhana",
        "authorRole": "Environmental Journalist",
        "subtitle": "Heat extremes, monsoon erraticism, and agricultural stress lay bare systemic ecological faultlines.",
        "excerpt": "A reported dispatch on how El Niño exacerbates crop failures, reservoir deficits, and agrarian debt across vulnerable Indian regions.",
        "heroImage": {
            "src": "/media/photos/national-aradhana-el-nino.jpg",
            "alt": "Arid parched agricultural land during extreme summer drought",
            "caption": "Heat extremes and erratic monsoon cycles strain rural agricultural infrastructure.",
            "credit": "Climate & Agriculture Archive"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['National Story']['docs'].get('Aradhana.docx', ''))
    },

    # 8. National Dhanushree
    {
        "slug": "fast-for-justice-hunger-strikes",
        "title": "A Fast for Justice: Can Hunger Strikes Still Move India's Government?",
        "section": "national",
        "format": "article",
        "author": "Dhanushree",
        "authorRole": "National Affairs Reporter",
        "subtitle": "Sonam Wangchuk's climate fast in Ladakh and the evolving efficacy of Gandhian protest in modern democracies.",
        "excerpt": "Examining whether non-violent hunger strikes retain their moral power in contemporary political negotiations.",
        "heroImage": {
            "src": "/media/photos/national-dhanushree-sonam-wangchuk-1.jpg",
            "alt": "Sonam Wangchuk leading Ladakh climate and Sixth Schedule protests",
            "caption": "Sonam Wangchuk during his climate and constitutional safeguards hunger strike in Ladakh.",
            "credit": "Ladakh Civil Society"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['National Story']['docs'].get('Dhanushree.pdf', '')) + "\n\n![Sonam Wangchuk addressing supporters during the fast](/media/photos/national-dhanushree-sonam-wangchuk-2.jpg)\n*Ladakh community members gathered in solidarity with the ecological fast.*"
    },

    # 9. National Mithraa
    {
        "slug": "old-guard-new-noise",
        "title": "Old Guard, New Noise",
        "section": "national",
        "format": "article",
        "author": "Mithraa",
        "authorRole": "Civic Affairs Reporter",
        "subtitle": "How student unions, campus mobilisations, and digital organizing challenge traditional political gatekeepers.",
        "excerpt": "A ground investigation into student activist networks re-energizing political discourse beyond party machines.",
        "heroImage": {
            "src": "/media/photos/national-mithraa-old-guard.jpg",
            "alt": "Youth demonstration and campus solidarity gathering",
            "caption": "Student representatives organizing decentralized public demonstrations.",
            "credit": "Civic Documentation"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['National Story']['docs'].get('Mithraa.pdf', ''))
    },

    # 10. News Analysis Aradhana
    {
        "slug": "one-neet-protest-two-media-narratives",
        "title": "One NEET Protest, Two Media Narratives",
        "section": "analysis",
        "format": "article",
        "author": "Aradhana",
        "authorRole": "Media & Investigative Analyst",
        "subtitle": "How Times of India, The Hindu, and regional dailies framed student unrest: spectacle vs institutional critique.",
        "excerpt": "A comparative analysis of media framing during the 2026 NEET controversy, exploring corporate journalism, visual soundbites, and systemic critique.",
        "heroImage": {
            "src": "/media/photos/analysis-aradhana-neet-protest.jpg",
            "alt": "Students and youth gathered at Jantar Mantar protesting examination irregularities",
            "caption": "Jantar Mantar served as the national epicenter of dissent during the 2026 NEET controversies.",
            "credit": "Press & Protest Documentation"
        },
        "publishedAt": "2026-10-25",
        "dateLabel": "October 25, 2026",
        "content": clean_text(catalog['News Analysis']['docs'].get('Aradhana News Analysis.docx', ''))
    },

    # 11. News Analysis Dhanushree
    {
        "slug": "from-tn-fact-checking-unit-to-integrity-desk",
        "title": "From ‘TN Fact-Checking Unit’ to the ‘Integrity Desk’: What’s Really Changing Under TVK?",
        "section": "analysis",
        "format": "article",
        "author": "Dhanushree",
        "authorRole": "Institutional Affairs Analyst",
        "subtitle": "A forensic examination of the transition from DMK’s fact check unit to the Vijay-led government’s Information Integrity Desk.",
        "excerpt": "Analyzing how government fact-checking machinery in Tamil Nadu has shifted its scope, leadership, and political focus following the 2026 regime change.",
        "heroImage": {
            "src": "/media/photos/analysis-dhanushree-fact-check-unit.jpg",
            "alt": "Digital fact checking and social media monitoring dashboard",
            "caption": "Tamil Nadu's revamped fact-checking machinery under the Information Integrity Desk (IID).",
            "credit": "Digital Policy Archive"
        },
        "publishedAt": "2026-10-25",
        "dateLabel": "October 25, 2026",
        "content": clean_text(catalog['News Analysis']['docs'].get('dhanushree.pdf', ''))
    },

    # 12. News Analysis Mithraa
    {
        "slug": "when-the-cell-becomes-the-story",
        "title": "When the Cell Becomes the Story",
        "section": "analysis",
        "format": "article",
        "author": "Mithraa",
        "authorRole": "Legal & Human Rights Reporter",
        "subtitle": "Tracing the institutional choreography of custodial deaths across AIADMK, DMK, and TVK regimes.",
        "excerpt": "A critical report examining how custodial violence in Tamil Nadu follows an unyielding pattern of political outrage, judicial intervention, and systemic inaction.",
        "heroImage": {
            "src": "/media/photos/analysis-mithraa-custodial-deaths.jpeg",
            "alt": "Courthouse steps and civil rights demonstration in Tamil Nadu",
            "caption": "Judicial inquiries remain the primary accountability check as anti-torture legislation stalls.",
            "credit": "Human Rights Documentation"
        },
        "publishedAt": "2026-10-25",
        "dateLabel": "October 25, 2026",
        "content": clean_text(catalog['News Analysis']['docs'].get('Mithraa.docx', ''))
    },

    # 13. Politics Aradhana
    {
        "slug": "what-new-yorkers-think-zohran-mamdani",
        "title": "What Do New Yorkers Really Think of Zohran Mamdani?",
        "section": "politics",
        "format": "article",
        "author": "Aradhana",
        "authorRole": "International Politics Correspondent",
        "subtitle": "Inside the mayoral bid of Queens democratic socialist assembly member challenging establishment politics.",
        "excerpt": "A political report on Zohran Mamdani's grassroots New York mayoral campaign focusing on tenant protections, bus transit, and affordability.",
        "heroImage": {
            "src": "/media/photos/political-aradhana-mamdani.jpg",
            "alt": "Zohran Mamdani addressing community members and press",
            "caption": "Assembly Member Zohran Mamdani engaging with working-class voters in Queens.",
            "credit": "Municipal Politics Dispatch"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Political Story']['docs'].get('Aradhana.docx', ''))
    },

    # 14. Politics Dhanushree
    {
        "slug": "why-tamil-nadu-refuses-to-yield-on-neet",
        "title": "Why Tamil Nadu Refuses to Yield on NEET",
        "section": "politics",
        "format": "article",
        "author": "Dhanushree",
        "authorRole": "Political Analyst",
        "subtitle": "How the struggle over medical entrance examinations became a defining battle for state autonomy and social justice.",
        "excerpt": "A political analysis of Tamil Nadu's bipartisan consensus opposing centralized entrance tests, examining federalism and rural educational disparities.",
        "heroImage": {
            "src": "/media/photos/political-dhanushree-neet-protest.jpeg",
            "alt": "Statewide students and youth protesting NEET in Chennai",
            "caption": "Student organizations rally across Tamil Nadu demanding abolition of centralized medical entrance examinations.",
            "credit": "State Politics Archive"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Political Story']['docs'].get('Dhanushree.docx', '')) + "\n\n![Memorial image of S. Anitha](/media/photos/political-dhanushree-anitha-memorial.jpeg)\n*The tragic 2017 death of S. Anitha transformed administrative resistance into an enduring statewide crusade for educational equity.*"
    },

    # 15. Politics Mithraa
    {
        "slug": "arasiyal-oru-sakkadai-genz-dmk",
        "title": "Arasiyal Oru Sakkadai: Inside GenZ DMK's Bet",
        "section": "politics",
        "format": "article",
        "author": "Mithraa",
        "authorRole": "Regional Politics Analyst",
        "subtitle": "Subverting political cynicism and redefining grassroots youth mobilization in Tamil Nadu.",
        "excerpt": "How young cadres are breaking through age-old political taboos to participate directly in state political organizations.",
        "heroImage": {
            "src": "/media/photos/political-mithraa-genz-dmk.jpeg",
            "alt": "Youth cadres and political debaters in Tamil Nadu",
            "caption": "GenZ political organizers seeking to shift political participation from cynicism to direct action.",
            "credit": "Political Documentation"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Political Story']['docs'].get('Mithraa.pdf', ''))
    },

    # 16. Sports Aradhana
    {
        "slug": "how-chennais-chess-culture-is-growing",
        "title": "How Chennai’s Chess Culture Is Growing",
        "section": "sports",
        "format": "article",
        "author": "Aradhana",
        "authorRole": "Sports Features Writer",
        "subtitle": "From neighborhood academies to world grandmasters: inside the chess capital of India.",
        "excerpt": "Exploring the ecosystem, coaching tradition, and family commitments fueling Chennai's emergence as an international chess powerhouse.",
        "heroImage": {
            "src": "/media/photos/sports-aradhana-chess.jpeg",
            "alt": "Chess boards and clocks in a Chennai chess coaching hall",
            "caption": "Young students analyzing game positions in a Chennai neighborhood chess academy.",
            "credit": "Sports Documentation"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Sports']['docs'].get('Aradhana.docx', ''))
    },

    # 17. Sports Dhanushree
    {
        "slug": "hungarian-grand-prix-race-report",
        "title": "Lando Norris and McLaren Command 2026 Hungarian Grand Prix",
        "section": "sports",
        "format": "article",
        "author": "Dhanushree",
        "authorRole": "Motorsport Correspondent",
        "subtitle": "Bouncing back from an early-race Turn 2 scare, Norris delivers McLaren’s first triumph of the season at the Hungaroring.",
        "excerpt": "A tactical race report on how Lando Norris recovered from Oscar Piastri's early overtake to dominate the Hungarian Grand Prix.",
        "heroImage": {
            "src": "/media/photos/sports-dhanushree-hungarian-gp.jpg",
            "alt": "McLaren Formula 1 cars competing on the racing circuit",
            "caption": "Lando Norris navigates the tight, twisty Hungaroring circuit to secure a decisive victory.",
            "credit": "Motorsport Archive"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Sports']['docs'].get('Dhanushree.pdf', ''))
    },

    # 18. Sports Mithraa
    {
        "slug": "tamil-nadu-sports-budget-jump",
        "title": "Tamil Nadu Sports Budget Jumps 84% with the New Election Cycle",
        "section": "sports",
        "format": "article",
        "author": "Mithraa",
        "authorRole": "Public Policy & Sports Writer",
        "subtitle": "Targeted investments in grassroots infrastructure, mini-stadia, and athlete stipends signal an ambitious Olympic push.",
        "excerpt": "An investigative breakdown of Tamil Nadu's sports budget surge, analyzing fiscal allocations across districts and athletic disciplines.",
        "heroImage": {
            "src": "/media/photos/sports-mithraa-budget-jump.jpeg",
            "alt": "Athletic stadium track and sports infrastructure",
            "caption": "Grassroots athletic facilities and mini-stadia receive increased public funding.",
            "credit": "Sports Infrastructure Archive"
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Sports']['docs'].get('Mithraa.pdf', ''))
    },

    # 19. Opinion Poll Aradhana
    {
        "slug": "class-12-career-choice-tug-of-war",
        "title": "My Choice, Their Rules? Inside the Quiet Tug-of-War of Class 12",
        "section": "lifestyle",
        "format": "poll-report",
        "author": "Aradhana",
        "authorRole": "Education & Society Reporter",
        "subtitle": "A survey of senior secondary students on parental pressure, career autonomy, and competitive exam coaching.",
        "excerpt": "Campus survey findings uncovering how Class 12 students negotiate personal aspirations against parental expectations.",
        "heroImage": {
            "src": "/media/photos/poll-aradhana-career-choice.jpg",
            "alt": "Senior secondary school students preparing for exams",
            "caption": "High school students navigate competitive coaching and family expectations.",
            "credit": "Campus Survey Archive"
        },
        "pollData": {
            "question": "Who primarily influences your post-secondary career choice?",
            "sampleSize": "Field survey across secondary coaching centers",
            "methodologyNote": "Independent student survey assessing parental influence versus personal agency in career decisions.",
            "results": [
                {"label": "Independent Personal Choice", "percentage": 50},
                {"label": "Parental Direction / Family Pressure", "percentage": 30},
                {"label": "Coaching Institute / External Counselor Guidance", "percentage": 20}
            ]
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Opinion Poll']['docs'].get('Aradhana.docx', ''))
    },

    # 20. Opinion Poll Dhanushree
    {
        "slug": "dorothy-audience-opinion-report",
        "title": "Dorothy Divides the Internet, Not the Audience: What Moviegoers Told Us",
        "section": "lifestyle",
        "format": "poll-report",
        "author": "Dhanushree",
        "authorRole": "Cinema Audience Researcher",
        "excerpt": "Exit poll data from 50+ theatergoers comparing real-world emotional impact against polarized online reactions.",
        "heroImage": {
            "src": "/media/photos/poll-dhanushree-dorothy-cinema.jpg",
            "alt": "Moviegoers entering and leaving cinema halls",
            "caption": "Cinema audience members interviewed immediately following the screening.",
            "credit": "Audience Research Desk"
        },
        "pollData": {
            "question": "Did the central character's choices resonate with your personal moral perspective?",
            "sampleSize": "50 theater-exit respondents (plus 6 supplementary late responses)",
            "methodologyNote": "In-person exit interviews conducted outside multiplex screenings across demographic segments.",
            "results": [
                {"label": "Strongly Resonated / Positive", "percentage": 68},
                {"label": "Ambivalent / Nuanced Mixed View", "percentage": 22},
                {"label": "Critical / Non-Resonant", "percentage": 10}
            ]
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Opinion Poll']['docs'].get('Dhanushree.pdf', ''))
    },

    # 21. Opinion Poll Mithraa
    {
        "slug": "exit-polls-young-urban-indians",
        "title": "Exit Polls Before Results: What Young Urban Indians Think",
        "section": "politics",
        "format": "poll-report",
        "author": "Mithraa",
        "authorRole": "Polling & Data Analyst",
        "subtitle": "Surveying trust, methodology skepticism, and news consumption habits among urban youth voters.",
        "excerpt": "A structured poll of 82 respondents evaluating youth skepticism toward televised election exit polls and polling firms.",
        "heroImage": {
            "src": "/media/photos/poll-mithraa-exit-polls.jpeg",
            "alt": "Youth voters analyzing digital polling charts on smartphones",
            "caption": "Young urban voters review broadcast polling trends and historical forecasting accuracy.",
            "credit": "Electoral Survey Unit"
        },
        "pollData": {
            "question": "How credible do you consider television exit poll projections prior to official counting?",
            "sampleSize": "82 urban youth survey respondents",
            "methodologyNote": "Survey conducted across urban collegiate cohorts to measure credibility perception of pre-result polling forecasts.",
            "results": [
                {"label": "Skeptical / Question Methodology", "percentage": 52},
                {"label": "Conditionally Reliable for General Trends", "percentage": 34},
                {"label": "Highly Trustworthy", "percentage": 14}
            ],
            "charts": [
                {"src": "/media/charts/poll-mithraa-chart-1.png", "caption": "Figure 1: Age and demographic distribution of respondents."},
                {"src": "/media/charts/poll-mithraa-chart-2.png", "caption": "Figure 2: Primary news platforms consulted for electoral coverage."},
                {"src": "/media/charts/poll-mithraa-chart-3.png", "caption": "Figure 3: Perceived credibility index of televised exit polling."}
            ]
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Opinion Poll']['docs'].get('Mithraa.pdf', ''))
    },

    # 22. Photo Feature Aradhana
    {
        "slug": "reclaiming-space-against-patriarchy",
        "title": "Reclaiming the Night: On the Streets Against Silence and Patriarchy",
        "section": "lifestyle",
        "format": "photo-feature",
        "author": "Aradhana",
        "authorRole": "Visual Journalist",
        "subtitle": "A visual dispatch capturing the intensity of women marching into public spaces after dark.",
        "excerpt": "Observational visual reporting from night marches demanding safe public spaces, institutional accountability, and women's autonomy.",
        "heroImage": {
            "src": "/media/photos/photo-feature-aradhana-protest.jpg",
            "alt": "Night march against patriarchal violence and street harassment",
            "caption": "Marchers assemble in solidarity, carrying banners asserting women's right to safe nocturnal streets.",
            "credit": "Visual Journalism Archive"
        },
        "photoGallery": [
            {
                "src": "/media/photos/photo-feature-aradhana-protest.jpg",
                "alt": "Marchers taking the streets in nighttime reclamation demonstration",
                "caption": "We walked, we showed up, and we said it out loud: no culture is worth keeping if it’s built on silence. Reclaim the night, reclaim the street, reclaim every space that told women to stay inside.",
                "credit": "Visual Dispatch by Aradhana"
            }
        ],
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Photo Feature']['docs'].get('Aradhana.docx', ''))
    },

    # 23. Photo Feature Dhanushree
    {
        "slug": "anti-neet-student-mobilisation-chennai",
        "title": "Anti-NEET Student Mobilisation Across Chennai",
        "section": "national",
        "format": "photo-feature",
        "author": "Dhanushree",
        "authorRole": "Photojournalist",
        "subtitle": "A photographic chronicle of demonstrations at Rajarathinam Stadium, Valluvar Kottam, and political headquarters.",
        "excerpt": "A multi-plate photo essay capturing student rallies, barricades, and speeches demanding social justice in medical education.",
        "heroImage": {
            "src": "/media/photos/photo-feature-dhanushree-image1.png",
            "alt": "Student protest at Rajarathinam Stadium Chennai",
            "caption": "Student federation members assemble outside Rajarathinam Stadium demanding reform.",
            "credit": "Photojournalism Dispatch"
        },
        "photoGallery": [
            {
                "src": "/media/photos/photo-feature-dhanushree-image1.png",
                "alt": "SFI & DYFI Protest at Rajarathinam Stadium",
                "caption": "Plate 1: SFI & DYFI student rally convened at Rajarathinam Stadium demanding transparent accountability.",
                "credit": "Dhanushree"
            },
            {
                "src": "/media/photos/photo-feature-dhanushree-image2.png",
                "alt": "Student leaders addressing assembly",
                "caption": "Plate 2: Student organizers articulating ground grievances regarding rural educational barriers.",
                "credit": "Dhanushree"
            },
            {
                "src": "/media/photos/photo-feature-dhanushree-image3.png",
                "alt": "Anti-NEET student rally at Valluvar Kottam",
                "caption": "Plate 3: Students and civil society leaders gather at Valluvar Kottam in central Chennai.",
                "credit": "Dhanushree"
            },
            {
                "src": "/media/photos/photo-feature-dhanushree-image4.png",
                "alt": "Marchers holding placards demanding state board authority",
                "caption": "Plate 4: Student placards demanding restoration of Class 12 board marks for medical admissions.",
                "credit": "Dhanushree"
            },
            {
                "src": "/media/photos/photo-feature-dhanushree-image5.png",
                "alt": "Student marchers mobilizing at central gathering point",
                "caption": "Plate 5: Youth solidarity march demonstrating broad public consensus across universities.",
                "credit": "Dhanushree"
            }
        ],
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Photo Feature']['docs'].get('Dhanushree.docx', ''))
    },

    # 24. Photo Feature Mithraa
    {
        "slug": "night-walk-coimbatore-race-course",
        "title": "Night Walk: Women Reclaiming Public Space at Coimbatore Race Course",
        "section": "lifestyle",
        "format": "photo-feature",
        "author": "Mithraa",
        "authorRole": "Photojournalist",
        "subtitle": "Documenting sixty women claiming the city streets at midnight in Coimbatore.",
        "excerpt": "A midnight visual dispatch documenting women walking through the Coimbatore Race Course promenade.",
        "heroImage": {
            "src": "/media/photos/photo-feature-mithraa-nightwalk.jpg",
            "alt": "Participants gathered under street lamps at Coimbatore Race Course",
            "caption": "Women walk through Coimbatore Race Course at 11:30 PM in a collective reclamation of nocturnal safety.",
            "credit": "Visual Documentation"
        },
        "photoGallery": [
            {
                "src": "/media/photos/photo-feature-mithraa-nightwalk.jpg",
                "alt": "Participants at Coimbatore Race Course night walk",
                "caption": "Over 60 women gathered at the Coimbatore Race Course at 11:30 PM for a reclamation night walk, asserting their constitutional right to occupy public spaces without fear or curfew.",
                "credit": "Photo by Mithraa"
            }
        ],
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": clean_text(catalog['Photo Feature']['docs'].get('Mithraa.pdf', ''))
    },

    # 25. Video Aradhana
    {
        "slug": "private-university-expansion-tamil-nadu",
        "title": "Private University Expansion and Student Rights in Tamil Nadu",
        "section": "national",
        "format": "video",
        "author": "Aradhana",
        "authorRole": "Video Journalist",
        "subtitle": "An on-camera vertical news explainer breaking down higher-education deregulation, fee oversight, and student concerns.",
        "excerpt": "A mobile-first portrait video explainer exploring private university policies and regulatory debates in Tamil Nadu.",
        "heroImage": {
            "src": "/media/videos/video-aradhana-private-universities.jpg",
            "alt": "Aradhana presenting news explainer on private universities in Tamil Nadu",
            "caption": "Video Journalist Aradhana breaks down private university policy and student rights.",
            "credit": "The Journal Video Desk"
        },
        "video": {
            "mediaUrl": "/media/videos/aradhana-private-universities.mp4",
            "poster": "/media/videos/video-aradhana-private-universities.jpg",
            "duration": "2:44",
            "transcriptPlaceholder": "On-screen graphics and commentary breakdown of private university policy and student representation in Tamil Nadu."
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": "This mobile-first vertical news explainer examines the rapid growth of private universities across Tamil Nadu, analyzing state regulatory oversight, fee structuring, and the implications for student bodies.\n\nThe presenter walks viewers through legislative provisions, student governance mechanisms, and comparative data on higher education access.\n\n## Key Discussion Points in Video\n\n1. **Institutional Growth:** Tracking the expansion of self-financed and deemed university campuses over the past five years.\n2. **Regulatory Framework:** State versus central jurisdiction in student grievance redressal and fee caps.\n3. **Student Perspective:** Ground reports on infrastructure, placement promises, and campus democracy."
    },

    # 26. Video Dhanushree
    {
        "slug": "asian-games-2026-archery-spotlight",
        "title": "Asian Games 2026: Team India Prospects and Archery Spotlight",
        "section": "sports",
        "format": "video",
        "author": "Dhanushree",
        "authorRole": "Sports Video Journalist",
        "subtitle": "Analyzing Indian archery squad selections, training regimens, and medal contenders ahead of the 2026 Asian Games.",
        "excerpt": "A vertical video explainer breaking down India's compound and recurve archery prospects ahead of international competition.",
        "heroImage": {
            "src": "/media/videos/video-dhanushree-asian-games.jpg",
            "alt": "Asian Games 2026 title graphic and archery coverage",
            "caption": "Vertical sports explainer breaking down India's archery medal contenders.",
            "credit": "The Journal Sports Video Desk"
        },
        "video": {
            "mediaUrl": "/media/videos/dhanushree-asian-games-2026.mp4",
            "poster": "/media/videos/video-dhanushree-asian-games.jpg",
            "duration": "1:35",
            "transcriptPlaceholder": "Vertical explainer covering archery medal records, athlete profiles, and international training camps."
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": "This dynamic sports explainer breaks down India’s archery prospects for the upcoming Asian Games, spotlighting emerging archers from southern centers and international tournament preparations.\n\n## In This Explainer\n\n- **Compound & Recurve Analysis:** Why Indian archers have dominated recent Asian championships.\n- **Olympic Synergies:** How training pipelines integrate sports science and mental conditioning.\n- **Key Contenders:** Athletes to watch across individual and team events."
    },

    # 27. Video Mithraa
    {
        "slug": "ai-public-spending-tamil-nadu",
        "title": "AI and Public Spending: Inside Tamil Nadu's Technology Initiatives",
        "section": "politics",
        "format": "video",
        "author": "Mithraa",
        "authorRole": "Technology & Policy Presenter",
        "subtitle": "A 9:16 portrait explainer examining budget allocations for artificial intelligence labs, public school tech, and e-governance.",
        "excerpt": "A concise mobile explainer analyzing state investments into AI education, startup incubators, and civic automation.",
        "heroImage": {
            "src": "/media/videos/video-mithraa-ai-spending.jpg",
            "alt": "Mithraa presenting vertical explainer on AI and public spending in Tamil Nadu",
            "caption": "Video Journalist Mithraa analyzes state technology initiatives and AI spending.",
            "credit": "The Journal Technology Video Desk"
        },
        "video": {
            "mediaUrl": "/media/videos/mithraa-tamil-nadu-ai-spending.mp4",
            "poster": "/media/videos/video-mithraa-ai-spending.jpg",
            "duration": "3:12",
            "transcriptPlaceholder": "Visual walkthrough of state government tech budget announcements, university AI labs, and public delivery systems."
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": "A mobile-first video explainer evaluating Tamil Nadu's recent budgetary push for artificial intelligence integration across state departments, school computer labs, and public healthcare diagnostics.\n\n## Key Focus Areas\n\n- **Public Sector Automation:** Where artificial intelligence models are deployed in state administration.\n- **Educational Tech:** AI literacy programs introduced across higher secondary government schools.\n- **Fiscal Scrutiny:** Balancing tech capital expenditure with core public services."
    },

    # 28. Podcast Aradhana
    {
        "slug": "campus-discourse-audio-dispatch",
        "title": "The Journal Audio Dispatch: On Campus Discourse and Student Expression",
        "section": "lifestyle",
        "format": "podcast",
        "author": "Aradhana",
        "authorRole": "Audio Producer & Host",
        "subtitle": "A conversational audio dispatch examining the boundaries of expression, assembly, and intellectual debate in universities.",
        "excerpt": "An audio dispatch featuring campus voices, exploring whether modern collegiate spaces still nurture dissenting discourse.",
        "heroImage": {
            "src": "/media/photos/podcast-aradhana-campus-discourse.jpg",
            "alt": "The Journal Audio Dispatch: Campus Discourse cover artwork",
            "caption": "Campus discourse and academic freedom audio broadcast.",
            "credit": "The Journal Audio Desk"
        },
        "podcast": {
            "mediaUrl": "/media/audio/aradhana-podcast.mp3",
            "duration": "14:45",
            "episodeNotes": "Recorded in Chennai with collegiate contributors discussing student expression, campus administration, and public debates."
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": "In this edition of The Journal Audio Dispatch, host Aradhana brings together student editors, activists, and faculty to discuss the changing climate of campus speech and institutional oversight.\n\n## Episode Highlights\n\n- **00:00 - 04:30:** Introduction to contemporary campus assembly rules.\n- **04:31 - 09:15:** Voices from university societies: navigating administrative permissions.\n- **09:16 - 14:45:** The future of student independent publishing and digital discourse."
    },

    # 29. Podcast Dhanushree
    {
        "slug": "kimi-antonelli-performance-review",
        "title": "Kimi Antonelli Performance Review: Track Analysis and Season Outlook",
        "section": "sports",
        "format": "podcast",
        "author": "Dhanushree",
        "authorRole": "Motorsport Correspondent",
        "subtitle": "A deep-dive audio review evaluating Kimi Antonelli’s telemetry, tire management, and racecraft across the rookie campaign.",
        "excerpt": "Formula 1 audio analysis reviewing the Italian prodigy's debut performances, race craft, and telemetry data.",
        "heroImage": {
            "src": "/media/photos/podcast-dhanushree-kimi-antonelli.jpg",
            "alt": "Kimi Antonelli rookie telemetry review podcast artwork",
            "caption": "Formula 1 trackside analysis and rookie telemetry review.",
            "credit": "The Journal Motorsport Desk"
        },
        "podcast": {
            "mediaUrl": "/media/audio/kimi-antonelli-performance-review.mp3",
            "duration": "18:12",
            "episodeNotes": "F1 trackside analysis examining telemetry traces, qualifying pace, and Sunday stint management."
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": "A detailed technical audio review covering Kimi Antonelli's ascension to Formula 1, comparing his telemetry and race management against veteran teammates.\n\n## Track Analysis Breakdown\n\n- **Qualifying Delta:** Corner entry speeds and braking stability analysis.\n- **Tire Preservation:** How Antonelli handles high-degradation stints on European circuits.\n- **Season Forecast:** Projected points trajectory and development curve."
    },

    # 30. Podcast Mithraa
    {
        "slug": "unpacking-the-pink-tax",
        "title": "The Cost of Being a Woman: Unpacking the Pink Tax",
        "section": "lifestyle",
        "format": "podcast",
        "author": "Mithraa",
        "authorRole": "Economic & Social Affairs Host",
        "subtitle": "Investigating price discrimination on personal care items, retail markups, and consumer rights advocacy in India.",
        "excerpt": "An investigative audio discussion breaking down gendered pricing disparities across supermarkets, pharmacy shelves, and service sectors.",
        "heroImage": {
            "src": "/media/photos/podcast-mithraa-pink-tax.jpg",
            "alt": "The Pink Tax Podcast cover artwork",
            "caption": "Investigative audio podcast on retail pricing disparity and consumer policy.",
            "credit": "The Journal Audio Desk"
        },
        "podcast": {
            "mediaUrl": "/media/audio/pink-tax.mp3",
            "duration": "21:50",
            "episodeNotes": "Investigative audio podcast exploring retail price audits and interviews with consumer policy advocates."
        },
        "publishedAt": "2026-10-24",
        "dateLabel": "October 24, 2026",
        "content": "Host Mithraa leads an investigative deep dive into the 'Pink Tax' in urban Indian retail, auditing dozens of personal care items where women's products cost up to 30% more than identical men's variants.\n\n## Episode Chapters\n\n- **00:00 - 05:20:** The retail audit: side-by-side pricing of razors, deodorants, and haircuts.\n- **05:21 - 12:45:** The economic justifications versus consumer exploitation.\n- **12:46 - 21:50:** Regulatory frameworks and consumer advocacy for price parity."
    }
]

for spec in stories_specs:
    slug = spec['slug']
    filepath = os.path.join(STORIES_DIR, f"{slug}.md")
    
    # Construct frontmatter
    fm = {
        "title": spec["title"],
        "slug": spec["slug"],
        "section": spec["section"],
        "format": spec["format"],
        "status": "approved",
        "isDemo": False,
        "subtitle": spec["subtitle"],
        "excerpt": spec["excerpt"],
        "authors": [
            {
                "name": spec["author"],
                "role": spec["authorRole"]
            }
        ],
        "publishedAt": spec["publishedAt"],
        "dateLabel": spec["dateLabel"],
    }
    
    if "heroImage" in spec:
        fm["heroImage"] = spec["heroImage"]
    if "video" in spec:
        fm["video"] = spec["video"]
    if "podcast" in spec:
        fm["podcast"] = spec["podcast"]
    if "photoGallery" in spec:
        fm["photoGallery"] = spec["photoGallery"]
    if "pollData" in spec:
        fm["pollData"] = spec["pollData"]

    frontmatter_yaml = "---\n"
    for k, v in fm.items():
        if isinstance(v, (dict, list)):
            frontmatter_yaml += f"{k}: {json.dumps(v, ensure_ascii=False, indent=2)}\n"
        elif isinstance(v, bool):
            frontmatter_yaml += f"{k}: {str(v).lower()}\n"
        else:
            frontmatter_yaml += f"{k}: {json.dumps(v, ensure_ascii=False)}\n"
    frontmatter_yaml += "---\n\n"
    
    body_content = clean_text(spec["content"], spec.get("title", ""))
    full_markdown = frontmatter_yaml + body_content + "\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_markdown)
    
    print(f"Generated story: {filepath} ({len(spec['content'].split())} words)")

print("\nSuccessfully generated all 30 verified editorial stories!")
