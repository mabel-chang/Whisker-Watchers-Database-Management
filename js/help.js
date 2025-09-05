//BANNER TAB FUNCTIONS
function openTab(evt, tabName) {
  // URL of the HTML file you want to redirect to
  var newPageUrl = '../html/' + tabName + '.html';

  // Redirect to the new page
  window.location.href = newPageUrl;
}

function logout() {
  // URL of the sign-in page
  var signInPageUrl = '../html/sign_in.html';

  // Redirect to the sign-in page
  window.location.href = signInPageUrl;
}
