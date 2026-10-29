/* About Me (resume) page: renders /api/about/. */
(function () {
    var esc = Ban2.esc;
    var icon = Ban2.icon;

    function map(list, fn) { return (list || []).map(fn).join(''); }

    function sectionHead(kicker, title) {
        return '<div class="section-head reveal"><p class="kicker">' + esc(kicker) + '</p>' +
            '<h2 class="section-title">' + esc(title) + '</h2></div>';
    }

    function hero(site, d) {
        var p = site.profile;
        return '<section class="hero">' +
            '<div class="hero-glow hero-glow-1"></div><div class="hero-glow hero-glow-2"></div>' +
            '<div class="container hero-inner">' +
            '<div class="hero-text reveal">' +
            '<span class="badge"><span class="dot"></span>Currently at Welcomhotel by ITC Hotels</span>' +
            '<h1>' + esc(p.name) + '</h1>' +
            '<p class="hero-title">' + esc(p.title) + ' <em>· Hospitality, Sales &amp; Events</em></p>' +
            '<p class="hero-summary">' + esc(p.summary) + '</p>' +
            '<div class="hero-actions">' +
            '<a href="/#contact" class="btn btn-primary">Plan an event with me</a>' +
            '<a href="#experience" class="btn btn-ghost">View experience</a>' +
            '</div></div>' +
            '<div class="hero-photo reveal"><div class="photo-ring">' +
            '<img src="' + esc(p.image) + '" alt="Portrait of ' + esc(p.name) + '" width="320" height="320"></div>' +
            '<div class="photo-chip">' + icon('award') + 'Associate of the Quarter</div></div>' +
            '</div>' +
            '<div class="container"><ul class="stats reveal">' +
            map(d.stats, function (s) { return '<li><strong>' + esc(s.value) + '</strong><span>' + esc(s.label) + '</span></li>'; }) +
            '</ul></div></section>';
    }

    function experience(d) {
        return '<section id="experience" class="section"><div class="container">' +
            sectionHead('Career', 'Work Experience') +
            '<ol class="timeline">' +
            map(d.experience, function (job, i) {
                return '<li class="timeline-item reveal">' +
                    '<div class="timeline-meta"><span class="period">' + esc(job.period) + '</span>' +
                    '<span class="place">' + esc(job.location) + '</span></div>' +
                    '<div class="card job-card' + (i === 0 ? ' is-current' : '') + '">' +
                    (i === 0 ? '<span class="current-tag">Current role</span>' : '') +
                    '<h3>' + esc(job.role) + '</h3><p class="company">' + esc(job.company) + '</p>' +
                    '<ul class="points">' + map(job.points, function (pt) { return '<li>' + esc(pt) + '</li>'; }) + '</ul>' +
                    '</div></li>';
            }) +
            '</ol></div></section>';
    }

    function highlights(d) {
        return '<section id="highlights" class="section section-dark"><div class="container">' +
            sectionHead('Recognition', 'Highlights') +
            '<div class="highlight-grid">' +
            map(d.highlights, function (h) {
                return '<article class="highlight reveal"><div class="icon-box">' + icon(h.icon) + '</div>' +
                    '<h3>' + esc(h.title) + '</h3><p>' + esc(h.text) + '</p></article>';
            }) +
            '</div></div></section>';
    }

    function education(d) {
        return '<section id="education" class="section section-alt"><div class="container">' +
            sectionHead('Learning', 'Education') +
            '<div class="grid">' +
            map(d.education, function (e) {
                return '<article class="card edu-card reveal">' +
                    '<div class="edu-top"><div class="icon-box icon-box-sm">' + icon('grad') + '</div>' +
                    '<span class="period">' + esc(e.date) + '</span></div>' +
                    '<h3>' + esc(e.degree) + '</h3>' +
                    (e.school ? '<p class="company">' + esc(e.school) + '</p>' : '') +
                    (e.note ? '<p class="note">' + esc(e.note) + '</p>' : '') +
                    '</article>';
            }) +
            '</div></div></section>';
    }

    function skills(d) {
        return '<section id="skills" class="section"><div class="container split">' +
            '<div class="reveal"><p class="kicker">Strengths</p><h2 class="section-title">Skills</h2><ul class="tags">' +
            map(d.skills, function (s) { return '<li class="tag tag-solid">' + esc(s) + '</li>'; }) +
            '</ul></div>' +
            '<div class="reveal"><p class="kicker">Communication</p><h2 class="section-title">Languages</h2><ul class="languages">' +
            map(d.languages, function (l) {
                return '<li><div class="lang-row"><strong>' + esc(l.name) + '</strong><span>' + esc(l.level) + '</span></div>' +
                    '<div class="meter"><span style="width: ' + Number(l.percent) + '%"></span></div></li>';
            }) +
            '</ul></div>' +
            '<div class="reveal"><p class="kicker">Beyond work</p><h2 class="section-title">Interests</h2><ul class="tags">' +
            map(d.interests, function (s) { return '<li class="tag">' + esc(s) + '</li>'; }) +
            '</ul></div>' +
            '</div></section>';
    }

    function contact(site) {
        var p = site.profile;
        function card(iconName, label, value, href) {
            var inner = '<div class="icon-box">' + icon(iconName) + '</div><span>' + label + '</span>' + esc(value);
            return '<li>' + (href
                ? '<a href="' + esc(href) + '" class="contact-card">' + inner + '</a>'
                : '<div class="contact-card">' + inner + '</div>') + '</li>';
        }
        return '<section class="section contact"><div class="hero-glow hero-glow-2"></div>' +
            '<div class="container contact-inner reveal">' +
            '<p class="kicker">Contact</p><h2>Let\'s work together</h2>' +
            '<p class="contact-lead">Corporate, MICE, travel trade or event enquiries are welcome.</p>' +
            '<ul class="contact-cards">' +
            card('mail', 'Email', p.email, 'mailto:' + p.email) +
            card('pin', 'Location', p.location) +
            card('cake', 'Date of birth', p.dob) +
            '</ul>' +
            '<a href="/#contact" class="btn btn-primary btn-lg">Send an enquiry</a>' +
            '</div></section>';
    }

    Ban2.boot({
        page: 'about',
        data: 'about/',
        title: function (site) { return 'About ' + site.profile.name + ' | ' + site.site_name; },
        render: function (main, site, d) {
            main.innerHTML = hero(site, d) + experience(d) + highlights(d) + education(d) + skills(d) + contact(site);
        }
    });
})();
