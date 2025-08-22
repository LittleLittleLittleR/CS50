document.addEventListener('DOMContentLoaded', function() {
  
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

});


// Emails View Section
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  load_email_previews(mailbox);
}

function load_email_previews(mailbox) {
  const route = `/emails/${mailbox}`;
  fetch(route)
  .then(response => response.json())
  .then(emails => {

    let emails_view = document.querySelector("#emails-view");
    emails.forEach((email) => {

      let div_id = email.read ? "email-preview-read" : "email-preview-unread";
      let content = `<div class="${div_id} email-preview">
      <p class="email-id" name="email_id">${email.id}</p>
      <p class="email-preview-sender">${email.sender}</p>
      <p class="email-preview-subject">${email.subject}</p>
      <p class="email-preview-timestamp">${email.timestamp}</p>
      </div>`;
  
      emails_view.innerHTML += content;
    });

    document.querySelectorAll('.email-preview').forEach((email) => {
      const email_id = email.querySelector('.email-id').innerText;
      email.addEventListener('click', () => load_email(email_id, mailbox));
    });
})};


// Email View Section
function load_email(email_id, mailbox) {
  const route = `/emails/${email_id}`;
  fetch(route)
  .then(response => response.json())
  .then(email => {

    document.querySelector('#emails-view').innerHTML = '';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    
    document.querySelector('#email-subject').innerText = email.subject;
    document.querySelector('#email-timestamp').innerText = email.timestamp;
    document.querySelector('#email-sender').value = email.sender;
    document.querySelector('#email-recipients').value = email.recipients;
    document.querySelector('#email-body').value = email.body;

    let email_archived = document.querySelector('#email-archived')
    if (mailbox !== 'sent') {
      email_archived.style.display = 'inline-block';
      if (email.archived) {
        email_archived.innerText = 'Unarchive'
        email_archived.addEventListener('click', () => mark_as_archived(email.id, false));
      } else {
        email_archived.innerText = 'Archive'
        email_archived.addEventListener('click', () => mark_as_archived(email.id, true));
      };
    } else {
      email_archived.style.display = 'none';
    };

    let email_reply = document.querySelector('#email-reply');
    email_reply.addEventListener('click', function() { compose_email(event, email); })

    mark_as_read(email_id);
  });
};

function mark_as_read(email_id) {
  const route = `/emails/${email_id}`;
  fetch(route, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
};

function mark_as_archived(email_id, archive) {
  const route = `/emails/${email_id}`;
  
  fetch(route, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archive
    })
  });

  location.reload();
};


// Compose View Section
function compose_email(event, email=null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (email) {
    document.querySelector('#compose-recipients').value = email.sender;

    let subject_prefill = email.subject.startsWith("Re: ") ? email.subject : `Re: ${email.subject}`;
    document.querySelector('#compose-subject').value = subject_prefill;

    let body_prefill = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}`
    document.querySelector('#compose-body').value = body_prefill;
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  };
};

async function send_email() {
  event.preventDefault();

  await fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      sender: document.querySelector('#compose-sender').value,
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value, 
      read: false,
      archived: false
    })
  })
  .then(response => response.json())
  .then(() => {
    load_mailbox("sent");
  });
};