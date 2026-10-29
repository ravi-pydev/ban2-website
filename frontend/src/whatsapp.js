function val(data, key) {
  return String(data[key] ?? '').trim() || '–';
}

function niceDate(value) {
  if (!value) return '–';
  return new Date(`${value}T00:00:00`).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'short', year: 'numeric',
  });
}

/** Build a wa.me link with the enquiry pre-written as a WhatsApp message. */
export function whatsappUrl(number, siteName, data) {
  const text = [
    `*New event enquiry – ${siteName}* 🎉`,
    '',
    `👤 *Name:* ${val(data, 'name')}`,
    `🏢 *Company:* ${val(data, 'company')}`,
    `📧 *Email:* ${val(data, 'email')}`,
    `📱 *Phone:* ${val(data, 'phone')}`,
    `🎯 *Event type:* ${val(data, 'event_type')}`,
    `👥 *Guests:* ${val(data, 'guests')}`,
    `📅 *Preferred date:* ${niceDate(data.date)}`,
    `📍 *Event location:* ${val(data, 'event_location')}`,
    '',
    '📝 *Details:*',
    val(data, 'message'),
    '',
    `— Sent from the ${siteName} website`,
  ].join('\n');
  return `https://wa.me/${number}?text=${encodeURIComponent(text)}`;
}
