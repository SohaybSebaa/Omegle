$(() => {
  $('#message').keypress((event) => {
  if (event.key === 'Enter') {
  event.preventDefault();
  $('#send').click();
  }
  });
  });