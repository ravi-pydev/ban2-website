/* Home (business) page: renders /api/home/ and handles the enquiry form. */
(function () {
    var esc = Ban2.esc;
    var icon = Ban2.icon;

    function map(list, fn) { return (list || []).map(fn).join(''); }

    function sectionHead(kicker, title, sub) {
        return '<div class="section-head center reveal">' +
            '<p class="kicker">' + esc(kicker) + '</p>' +
            '<h2 class="section-title">' + esc(title) + '</h2>' +
            (sub ? '<p class="section-sub">' + esc(sub) + '</p>' : '') +
            '</div>';
    }

    function hero(site, d) {
        var p = site.profile;
        return '<section class="biz-hero" style="--hero-img: url(\'' + esc(d.hero.image) + '\')">' +
            '<div class="container biz-hero-inner">' +
            '<div class="reveal">' +
            '<span class="badge"><span class="dot"></span>Taking enquiries for ' + new Date().getFullYear() + '</span>' +
            '<h1>' + esc(d.hero.heading) + '</h1>' +
            '<p class="biz-hero-text">' + esc(d.hero.text) + '</p>' +
            '<div class="hero-actions">' +
            '<a href="#contact" class="btn btn-primary">Plan my event</a>' +
            '<a href="#services" class="btn btn-ghost">Explore services</a>' +
            '</div></div>' +
            '<a href="/about/" class="profile-card reveal">' +
            '<img src="' + esc(p.image) + '" alt="Portrait of ' + esc(p.name) + '" width="72" height="72">' +
            '<div><strong>' + esc(p.name) + '</strong><span>' + esc(p.title) + '</span>' +
            '<em>About me ' + icon('arrow') + '</em></div></a>' +
            '</div>' +
            '<div class="container"><ul class="stats reveal">' +
            map(d.stats, function (s) { return '<li><strong>' + esc(s.value) + '</strong><span>' + esc(s.label) + '</span></li>'; }) +
            '</ul></div></section>';
    }

    function ribbon(d) {
        var items = map(d.client_types, function (c) { return '<span>' + esc(c) + '</span>'; });
        return '<div class="ribbon" aria-label="Who I work with"><div class="ribbon-track">' + items + items + '</div></div>';
    }

    function intro(d) {
        return '<section class="section"><div class="container intro">' +
            '<div class="intro-media reveal">' +
            '<img src="' + esc(d.intro.image) + '" alt="Conference hall set up for an event" loading="lazy">' +
            '<div class="intro-badge"><strong>50+</strong><span>MNC events<br>delivered</span></div></div>' +
            '<div class="reveal">' +
            '<p class="kicker">Why hire a hospitality professional</p>' +
            '<h2 class="section-title">' + esc(d.intro.heading) + '</h2>' +
            map(d.intro.paragraphs, function (t) { return '<p class="lead-text">' + esc(t) + '</p>'; }) +
            '<ul class="checklist">' +
            map(['Venue, menu and AV in one plan', 'Transparent quotations',
                'One point of contact, start to finish', 'On-site coordination on the day'],
                function (t) { return '<li>' + icon('check') + esc(t) + '</li>'; }) +
            '</ul>' +
            '<a href="/about/" class="text-link">Read my full story ' + icon('arrow') + '</a>' +
            '</div></div></section>';
    }

    function services(d) {
        return '<section id="services" class="section section-alt"><div class="container">' +
            sectionHead('What I offer', 'Services',
                'Everything you need to plan, book and deliver a successful event — handled by one experienced professional.') +
            '<div class="service-grid">' +
            map(d.services, function (s) {
                return '<article class="service-card reveal">' +
                    '<div class="service-img"><div class="service-frame"><img src="' + esc(s.image) + '" alt="" loading="lazy"></div>' +
                    '<div class="service-icon">' + icon(s.icon) + '</div></div>' +
                    '<div class="service-body"><h3>' + esc(s.title) + '</h3><p>' + esc(s.text) + '</p>' +
                    '<a href="#contact" class="text-link">Enquire ' + icon('arrow') + '</a></div></article>';
            }) +
            '</div></div></section>';
    }

    function sessions(d) {
        return '<section id="sessions" class="section"><div class="container">' +
            sectionHead('Portfolio', 'Successfully Organised Sessions',
                'Conferences, dinners, workshops and celebrations — a look at the kinds of events I have planned and delivered.') +
            '<div class="gallery">' +
            map(d.sessions, function (s) {
                return '<figure class="gallery-item reveal">' +
                    '<img src="' + esc(s.image) + '" alt="' + esc(s.title) + '" loading="lazy">' +
                    '<figcaption><h3>' + esc(s.title) + '</h3><p>' + esc(s.text) + '</p></figcaption></figure>';
            }) +
            '</div></div></section>';
    }

    function whyMe(d) {
        return '<section class="section section-dark"><div class="container">' +
            sectionHead('Why work with me', 'Experience you can rely on') +
            '<div class="highlight-grid">' +
            map(d.why_me, function (w) {
                return '<article class="highlight reveal"><div class="icon-box">' + icon(w.icon) + '</div>' +
                    '<h3>' + esc(w.title) + '</h3><p>' + esc(w.text) + '</p></article>';
            }) +
            '</div></div></section>';
    }

    function process(d) {
        return '<section id="process" class="section"><div class="container">' +
            sectionHead('How it works', 'From first call to final bill') +
            '<ol class="process">' +
            map(d.process, function (step, i) {
                return '<li class="process-step reveal"><span class="step-num">' + (i < 9 ? '0' : '') + (i + 1) + '</span>' +
                    '<h3>' + esc(step.title) + '</h3><p>' + esc(step.text) + '</p></li>';
            }) +
            '</ol></div></section>';
    }

    function clients(d) {
        return '<section id="clients" class="section section-alt"><div class="container">' +
            sectionHead('Testimonials', 'Happy Clients', 'What clients say about working with me.') +
            '<div class="testimonial-grid">' +
            map(d.testimonials, function (t) {
                return '<figure class="testimonial reveal">' +
                    (t.sample ? '<span class="sample-tag">Sample</span>' : '') +
                    icon('quote', 'quote-mark') +
                    '<div class="stars" aria-label="5 out of 5">★★★★★</div>' +
                    '<blockquote>' + esc(t.quote) + '</blockquote>' +
                    '<figcaption><span class="avatar">' + icon('user') + '</span>' +
                    '<span><strong>' + esc(t.name) + '</strong><small>' + esc(t.role) + '</small></span></figcaption>' +
                    '</figure>';
            }) +
            '</div>' +
            '<div class="client-types reveal"><p>Trusted by clients across</p><ul class="tags">' +
            map(d.client_types, function (c) { return '<li class="tag">' + esc(c) + '</li>'; }) +
            '</ul></div></div></section>';
    }

    function ctaBand(d) {
        var stage = d.sessions.filter(function (s) { return /stage\.jpg$/.test(s.image); })[0];
        var bg = stage ? stage.image : d.hero.image;
        return '<section class="cta-band" style="--cta-img: url(\'' + esc(bg) + '\')">' +
            '<div class="container cta-inner reveal"><div>' +
            '<h2>Have an event coming up?</h2>' +
            '<p>Share your date and guest count — I will come back with venue options and a clear plan.</p>' +
            '</div><a href="#contact" class="btn btn-primary btn-lg">Get a free consultation</a></div></section>';
    }

    function faq(d) {
        return '<section id="faq" class="section"><div class="container faq-wrap">' +
            '<div class="reveal"><p class="kicker">FAQ</p>' +
            '<h2 class="section-title">Questions clients often ask</h2>' +
            '<p class="lead-text">Can\'t find what you are looking for? <a href="#contact" class="text-link inline">Send me a message</a>.</p></div>' +
            '<div class="faq reveal">' +
            map(d.faqs, function (f, i) {
                return '<details' + (i === 0 ? ' open' : '') + '><summary>' + esc(f.q) + '</summary><p>' + esc(f.a) + '</p></details>';
            }) +
            '</div></div></section>';
    }

    function contact(site, d) {
        var p = site.profile;
        var options = map(d.services, function (s) { return '<option>' + esc(s.title) + '</option>'; }) + '<option>Other</option>';
        return '<section id="contact" class="section contact contact-split">' +
            '<div class="hero-glow hero-glow-1"></div>' +
            '<div class="container contact-grid">' +
            '<div class="reveal"><p class="kicker">Enquire</p>' +
            '<h2>Let\'s plan your next event</h2>' +
            '<p class="contact-lead">Tell me a little about your event and I will get back to you within one working day.</p>' +
            '<ul class="contact-points">' +
            '<li><span class="icon-box icon-box-sm">' + icon('mail') + '</span><a href="mailto:' + esc(p.email) + '">' + esc(p.email) + '</a></li>' +
            '<li><span class="icon-box icon-box-sm">' + icon('pin') + '</span>' + esc(p.service_area) + '</li>' +
            '<li><span class="icon-box icon-box-sm">' + icon('clock') + '</span>Reply within 1 working day</li>' +
            '</ul></div>' +
            '<form class="enquiry reveal" id="enquiry" novalidate>' +
            '<div class="hp" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>' +
            '<div class="field-row">' +
            '<label>Your name *<input name="name" required maxlength="100" autocomplete="name"></label>' +
            '<label>Company<input name="company" maxlength="120" autocomplete="organization"></label></div>' +
            '<div class="field-row">' +
            '<label>Email *<input name="email" type="email" required autocomplete="email"></label>' +
            '<label>Phone / WhatsApp<input name="phone" type="tel" maxlength="20" autocomplete="tel"></label></div>' +
            '<div class="field-row">' +
            '<label>Event type<select name="event_type">' + options + '</select></label>' +
            '<label>Guests<input name="guests" type="number" min="1" inputmode="numeric"></label></div>' +
            '<label>Preferred date<input name="date" type="date"></label>' +
            '<label>Details<textarea name="message" rows="4" maxlength="3000" placeholder="City, budget, anything else I should know"></textarea></label>' +
            '<button type="submit" class="btn btn-primary">Send enquiry</button>' +
            '<output class="form-status" aria-live="polite" hidden></output>' +
            '<p class="form-note">Your enquiry is emailed to me and WhatsApp opens with your message ready — just tap Send.</p>' +
            '</form></div></section>';
    }

    /* ---------- Enquiry form ---------- */

    function val(d, key) { return (d.get(key) || '').toString().trim() || '–'; }

    function niceDate(value) {
        if (!value) return '–';
        var date = new Date(value + 'T00:00:00');
        return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    }

    function whatsappUrl(number, d) {
        var text = [
            '*New event enquiry – Ban2Plans* 🎉',
            '',
            '👤 *Name:* ' + val(d, 'name'),
            '🏢 *Company:* ' + val(d, 'company'),
            '📧 *Email:* ' + val(d, 'email'),
            '📱 *Phone:* ' + val(d, 'phone'),
            '🎯 *Event type:* ' + val(d, 'event_type'),
            '👥 *Guests:* ' + val(d, 'guests'),
            '📅 *Preferred date:* ' + niceDate(d.get('date')),
            '',
            '📝 *Details:*',
            val(d, 'message'),
            '',
            '— Sent from the Ban2Plans website'
        ].join('\n');
        return 'https://wa.me/' + number + '?text=' + encodeURIComponent(text);
    }

    function firstError(body) {
        if (body.error) return body.error;
        if (body.detail) return body.detail;
        if (body.errors) {
            var field = Object.keys(body.errors)[0];
            return field + ': ' + [].concat(body.errors[field])[0];
        }
        return 'Please check the form and try again.';
    }

    function initEnquiry(site) {
        var form = document.getElementById('enquiry');
        var button = form.querySelector('button[type="submit"]');
        var status = form.querySelector('.form-status');

        function showStatus(html, kind) {
            status.hidden = false;
            status.className = 'form-status ' + kind;
            status.innerHTML = html;
        }

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            var data = new FormData(form);
            var waUrl = whatsappUrl(site.whatsapp_number, data);

            // Open WhatsApp straight away: browsers only allow new windows during the click.
            var waWindow = window.open(waUrl, '_blank');
            if (waWindow) waWindow.opener = null;
            var waLink = '<a href="' + esc(waUrl) + '" target="_blank" rel="noopener">Open WhatsApp</a>';

            var payload = {};
            data.forEach(function (value, key) { payload[key] = value; });

            button.disabled = true;
            button.textContent = 'Sending…';

            Ban2.api('enquiries/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
                body: JSON.stringify(payload)
            })
                .then(function (r) {
                    if (r.ok) {
                        showStatus('Thank you! Your enquiry has been emailed. ' +
                            (waWindow ? 'Tap Send in WhatsApp to share it there too.' : waLink + ' to send it on WhatsApp too.'), 'success');
                        form.reset();
                    } else {
                        showStatus(esc(firstError(r.body)) + ' ' + waLink, 'error');
                    }
                })
                .catch(function () {
                    showStatus('Network error — the email was not sent. ' + waLink + ' to reach me instead.', 'error');
                })
                .finally(function () {
                    button.disabled = false;
                    button.textContent = 'Send enquiry';
                });
        });
    }

    Ban2.boot({
        page: 'home',
        data: 'home/',
        title: function (site) { return site.site_name + ' | Corporate Events, MICE & Venue Sourcing'; },
        render: function (main, site, d) {
            main.innerHTML = hero(site, d) + ribbon(d) + intro(d) + services(d) + sessions(d) +
                whyMe(d) + process(d) + clients(d) + ctaBand(d) + faq(d) + contact(site, d);
            initEnquiry(site);
        }
    });
})();
