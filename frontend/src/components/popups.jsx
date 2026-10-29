import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import { useApi } from '../hooks.js';
import EnquiryForm from './enquiry/EnquiryForm.jsx';
import FeedbackForm from './feedback/FeedbackForm.jsx';
import Icon from './Icon.jsx';

/*
 * Site-wide popups: the enquiry form and the feedback form.
 * Any component can open them with useEnquiry() / useFeedback(),
 * or render <EnquireButton> / <FeedbackButton>.
 */

const PopupContext = createContext({ openEnquiry() {}, openFeedback() {} });

export function useEnquiry() {
  return useContext(PopupContext).openEnquiry;
}

export function useFeedback() {
  return useContext(PopupContext).openFeedback;
}

/** Opens the enquiry popup, optionally with an event type pre-selected. */
export function EnquireButton({ eventType, className = 'btn btn-primary', onClick, children }) {
  const openEnquiry = useEnquiry();
  return (
    <button type="button" className={className} aria-haspopup="dialog"
      onClick={(e) => { onClick?.(e); openEnquiry(eventType); }}>
      {children}
    </button>
  );
}

/** Opens the feedback popup. */
export function FeedbackButton({ className = 'btn btn-primary', onClick, children }) {
  const openFeedback = useFeedback();
  return (
    <button type="button" className={className} aria-haspopup="dialog"
      onClick={(e) => { onClick?.(e); openFeedback(); }}>
      {children}
    </button>
  );
}

function Loading() {
  return <div className="modal-loading" role="status"><span />Loading…</div>;
}

function LoadError() {
  return <p className="form-status error modal-message">The form could not be loaded. Please try again.</p>;
}

function Success({ title, children, onClose, onAgain, againLabel }) {
  return (
    <div className="modal-success">
      <span className="success-icon"><Icon name="check" /></span>
      <h3>{title}</h3>
      {children}
      <div className="success-actions">
        <button type="button" className="btn btn-primary" onClick={onClose}>Close</button>
        {onAgain && <button type="button" className="btn btn-ghost-dark" onClick={onAgain}>{againLabel}</button>}
      </div>
    </div>
  );
}

function EnquiryBody({ site, eventType, onClose }) {
  // Event types come from the API, so the popup works on every page.
  const { data, error } = useApi('enquiries/');
  const [sent, setSent] = useState(null);

  if (sent) {
    return (
      <Success title="Thank you!" onClose={onClose} onAgain={() => setSent(null)} againLabel="Send another enquiry">
        <p>{sent.message} I will get back to you within one working day.</p>
        <p>
          {sent.waOpened
            ? 'WhatsApp has opened with your message — just tap Send there too.'
            : <><a href={sent.waUrl} target="_blank" rel="noopener noreferrer">Open WhatsApp</a> to send it there too.</>}
        </p>
      </Success>
    );
  }
  if (error) return <LoadError />;
  if (!data) return <Loading />;
  const types = data.event_types;
  return (
    <EnquiryForm site={site} eventTypes={types}
      defaultEventType={types.includes(eventType) ? eventType : undefined}
      onSuccess={setSent} />
  );
}

function FeedbackBody({ onClose }) {
  const { data, error } = useApi('feedback/');
  const [sent, setSent] = useState(false);

  if (sent) {
    return (
      <Success title="Thank you for your feedback!" onClose={onClose}>
        <p>Your review will appear on the site once it has been checked.</p>
      </Success>
    );
  }
  if (error) return <LoadError />;
  if (!data) return <Loading />;
  return <FeedbackForm events={data.events} onSuccess={() => setSent(true)} />;
}

const POPUPS = {
  enquiry: { kicker: 'Enquire', title: "Let's plan your next event" },
  feedback: { kicker: 'Existing clients', title: 'Share your feedback' },
};

export function PopupProvider({ site, children }) {
  const dialogRef = useRef(null);
  // `key` remounts the body on every open, so forms always start fresh.
  const [state, setState] = useState({ type: null, eventType: undefined, key: 0 });

  const openEnquiry = useCallback((eventType) => {
    setState((s) => ({ type: 'enquiry', eventType, key: s.key + 1 }));
  }, []);
  const openFeedback = useCallback(() => {
    setState((s) => ({ type: 'feedback', eventType: undefined, key: s.key + 1 }));
  }, []);
  const close = useCallback(() => setState((s) => ({ ...s, type: null })), []);

  // React state decides whether the dialog is open; the effect syncs the <dialog> element.
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (state.type && !dialog.open) dialog.showModal();
    if (!state.type && dialog.open) dialog.close();
  }, [state.type, state.key]);

  // The browser fires "close" asynchronously (also when Esc is pressed). Ignore a late
  // event that arrives after the dialog has already been reopened.
  function handleNativeClose() {
    if (!dialogRef.current?.open) close();
  }

  const popup = state.type && POPUPS[state.type];

  return (
    <PopupContext.Provider value={{ openEnquiry, openFeedback }}>
      {children}
      <dialog
        ref={dialogRef}
        className="site-modal"
        aria-labelledby="site-modal-title"
        onClose={handleNativeClose}
        onClick={(e) => { if (e.target === e.currentTarget) close(); }}
      >
        {popup && (
          <div className="modal-inner">
            <header className="modal-header">
              <div>
                <p className="kicker">{popup.kicker}</p>
                <h2 id="site-modal-title">{popup.title}</h2>
              </div>
              <button type="button" className="modal-close" aria-label="Close" onClick={close}>×</button>
            </header>
            {state.type === 'enquiry'
              ? <EnquiryBody key={state.key} site={site} eventType={state.eventType} onClose={close} />
              : <FeedbackBody key={state.key} onClose={close} />}
          </div>
        )}
      </dialog>
    </PopupContext.Provider>
  );
}
