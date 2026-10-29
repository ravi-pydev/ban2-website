"""Text content for the site. Edit the wording here; templates only handle layout."""

SITE_NAME = 'Ban2Plans'

# Enquiries open WhatsApp to this number (country code + number, digits only).
WHATSAPP_NUMBER = '919412833444'

PROFILE = {
    'name': 'Shashi Darshan',
    'title': 'Assistant Sales Manager',
    'tagline': 'Hospitality sales & event management',
    'summary': (
        'Ability to work under pressure, time management and being target '
        'focused are some of the key qualities I have. I believe in smart '
        'working and want to keep learning to enhance my knowledge and '
        'polish my skills.'
    ),
    'email': 'shashidarshan.999@gmail.com',
    'location': 'Rohtak, India',
    'service_area': 'Delhi NCR & across India',
    'dob': '08 May 1999',
}

# ---------------------------------------------------------------------------
# Home page (business)
# ---------------------------------------------------------------------------

HERO = {
    'heading': 'Events that run on time, on budget and on brand.',
    'text': (
        'From boardroom meetings to large conferences, I plan, negotiate and '
        'deliver corporate and social events with the eye of a hotel insider — '
        'so you can focus on your guests while every detail is handled.'
    ),
    'image': 'banquet-hall.jpg',
}

STATS = [
    {'value': '4+', 'label': 'Years in hospitality'},
    {'value': '50+', 'label': 'MNC events executed'},
    {'value': '5', 'label': 'Events handled in a day'},
    {'value': '2', 'label': 'Associate awards'},
]

INTRO = {
    'heading': 'A hotel insider on your side of the table',
    'paragraphs': [
        'I have spent my career inside luxury hotels — first coordinating events '
        'at Le Méridien Gurgaon, then selling venues and building corporate '
        'accounts at Welcomhotel by ITC Hotels. I know how hotels price, plan '
        'and run events, and where the hidden costs and common mistakes are.',
        'That experience means I can find the right venue faster, negotiate '
        'fairer terms, and coordinate every department — banquets, kitchen, AV, '
        'front office — so your event feels effortless for you and your guests.',
    ],
    'image': 'conference-hall.jpg',
}

SERVICES = [
    {'icon': 'mic', 'title': 'Corporate Events & Conferences', 'image': 'conference.jpg',
     'text': 'Annual meets, conferences, town halls and product launches — planned '
             'end to end, from agenda and seating to AV and catering.'},
    {'icon': 'globe', 'title': 'MICE Planning', 'image': 'seminar.jpg',
     'text': 'Meetings, incentives, conferences and exhibitions for corporate, '
             'government and travel trade groups of any size.'},
    {'icon': 'building', 'title': 'Venue Sourcing & Negotiation', 'image': 'banquet-hall.jpg',
     'text': 'Shortlisting the right hotel or banquet, comparing proposals and '
             'negotiating rates, inclusions and contract terms for you.'},
    {'icon': 'glass', 'title': 'Gala Dinners & Award Nights', 'image': 'dinner-setup.jpg',
     'text': 'Theme, décor, menu, stage and run-of-show for dinners and '
             'recognition evenings your team will remember.'},
    {'icon': 'sun', 'title': 'Offsites & Retreats', 'image': 'resort.jpg',
     'text': 'Leadership offsites and team retreats with room blocks, '
             'activities and transfers organised in one plan.'},
    {'icon': 'heart', 'title': 'Social Celebrations', 'image': 'celebration.jpg',
     'text': 'Birthdays, anniversaries and family functions with the same '
             'attention to detail as a corporate event.'},
]

SESSIONS = [
    {'title': 'Corporate conferences', 'image': 'conference.jpg',
     'text': 'Multi-session conferences for MNC clients with stage, AV and breakout planning.'},
    {'title': 'Gala dinners', 'image': 'dinner-setup.jpg',
     'text': 'Seated dinners with custom menus, table layouts and décor.'},
    {'title': 'Workshops & trainings', 'image': 'workshop.jpg',
     'text': 'Interactive sessions with the right room set-up and refreshments.'},
    {'title': 'Seminars & keynotes', 'image': 'seminar.jpg',
     'text': 'Theatre-style sessions with registration, stage and speaker support.'},
    {'title': 'Team offsites', 'image': 'retreat.jpg',
     'text': 'Retreats combining work sessions, leisure and accommodation.'},
    {'title': 'Launches & celebrations', 'image': 'stage.jpg',
     'text': 'High-energy launches and parties with entertainment and stage cues.'},
]

WHY_ME = [
    {'icon': 'key', 'title': 'Hotel insider knowledge',
     'text': 'I have sold and run events from the hotel side, so I know what to ask for.'},
    {'icon': 'rupee', 'title': 'Better rates & terms',
     'text': 'Proposals, quotations and contract negotiation are my everyday work.'},
    {'icon': 'clock', 'title': 'Calm under pressure',
     'text': 'Used to handling up to five events in a single day without missing a detail.'},
    {'icon': 'award', 'title': 'Award-winning service',
     'text': 'Recognised as Associate of the Month and Associate of the Quarter.'},
]

PROCESS = [
    {'title': 'Consultation', 'text': 'We talk through your goals, guest count, dates and budget.'},
    {'title': 'Proposal', 'text': 'You get venue options, a plan and a transparent cost estimate.'},
    {'title': 'Negotiation', 'text': 'I secure rates, inclusions and contract terms on your behalf.'},
    {'title': 'Execution', 'text': 'On the day I coordinate every team so the event runs to plan.'},
    {'title': 'Follow-up', 'text': 'Final bills are checked and feedback reviewed for next time.'},
]

CLIENT_TYPES = [
    'Multinational corporates', 'Government bodies', 'Travel trade partners',
    'MICE agencies', 'Startups & SMEs', 'Families & private hosts',
]

# Replace these with real feedback before going live. While 'sample' is True
# the card shows a "Sample" badge so it is never mistaken for a real review.
TESTIMONIALS = [
    {'quote': 'Add a short quote from a happy client here — what the event was and '
              'what they valued most about working with Shashi.',
     'name': 'Client name', 'role': 'Designation, Company', 'sample': True},
    {'quote': 'Add a second testimonial here, ideally from a corporate or MICE '
              'client, mentioning the size or type of event.',
     'name': 'Client name', 'role': 'Designation, Company', 'sample': True},
    {'quote': 'Add a third testimonial here, for example from a social event or '
              'offsite, to show the range of events handled.',
     'name': 'Client name', 'role': 'Designation, Company', 'sample': True},
]

FAQS = [
    {'q': 'What size of events do you handle?',
     'a': 'Anything from a 10-person board meeting to large conferences and gala '
          'dinners. The planning approach scales with the guest count.'},
    {'q': 'Which cities do you work in?',
     'a': 'Mainly Delhi NCR, and I can coordinate events with hotels across India.'},
    {'q': 'How early should I get in touch?',
     'a': 'Four to eight weeks ahead is ideal for corporate events, and earlier for '
          'peak wedding and conference season. Shorter timelines are possible.'},
    {'q': 'Do you only work with one hotel brand?',
     'a': 'Tell me your requirements and I will recommend the venue options that fit '
          'them best.'},
]

# ---------------------------------------------------------------------------
# About page (resume)
# ---------------------------------------------------------------------------

EXPERIENCE = [
    {
        'role': 'Assistant Sales Manager',
        'company': 'Welcomhotel by ITC Hotels',
        'location': 'Delhi',
        'period': 'Apr 2026 – Present',
        'points': [
            'Identify and develop new corporate, government, travel trade, and MICE accounts',
            'Prepare proposals, contracts, quotations, and negotiate commercial terms',
            'Conduct daily sales calls, client meetings, and hotel presentations',
            'Follow up on enquiries and convert leads into confirmed business',
            'Coordinate with internal departments for seamless event planning '
            'and guest service delivery',
            'Monitor competitor activities, market trends, and pricing strategies',
        ],
    },
    {
        'role': 'Sales Executive',
        'company': 'Welcomhotel by ITC Hotels',
        'location': 'Delhi',
        'period': 'Feb 2025 – Apr 2026',
        'points': [
            'Property show rounds and understanding guest requirements',
            'Venue selling and blocking',
            'Event documentation',
        ],
    },
    {
        'role': 'Event Coordinator',
        'company': 'Le Méridien Gurgaon',
        'location': 'Gurugram',
        'period': 'Oct 2022 – Dec 2024',
        'points': [
            'Executed events for more than 50 MNCs',
            'Handled more than 5 events in a day',
            'Understood the requirements of each event',
            'Awarded "Associate of the Month"',
            'Awarded "Associate of the Quarter"',
        ],
    },
]

HIGHLIGHTS = [
    {'icon': 'award', 'title': 'Associate of the Month',
     'text': 'Recognised at Le Méridien Gurgaon for outstanding event delivery.'},
    {'icon': 'star', 'title': 'Associate of the Quarter',
     'text': 'Awarded for consistent performance across a full quarter.'},
    {'icon': 'calendar', 'title': '50+ MNC events',
     'text': 'Planned and executed corporate events for leading multinationals.'},
    {'icon': 'trend', 'title': 'Corporate & MICE sales',
     'text': 'Building corporate, government, travel trade and MICE accounts at ITC Hotels.'},
]

EDUCATION = [
    {'degree': 'Masters of Hotel Management', 'school': 'IHTM, MDU', 'date': 'Oct 2022'},
    {'degree': 'Bachelor of Arts', 'school': 'Sh. Lal Nath Hindu College, Rohtak',
     'note': 'Indian Red Cross Society', 'date': 'Nov 2020'},
    {'degree': 'Basics of Tally', 'date': 'Jul 2020'},
    {'degree': '12th', 'school': 'Sh. Baba Mast Nath Public School, Rohtak',
     'note': 'Merit certificate', 'date': 'Mar 2017'},
]

SKILLS = [
    'Leadership', 'Public Speaking', 'MS Office',
    'Problem Solving', 'Time Management', 'Adaptability',
]

LANGUAGES = [
    {'name': 'English', 'level': 'Full professional proficiency', 'percent': 85},
    {'name': 'Hindi', 'level': 'Native or bilingual proficiency', 'percent': 100},
]

INTERESTS = ['Cooking', 'Social work', 'Music', 'Playing guitar']
