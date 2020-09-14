document.getElementById('themeSwitch').addEventListener('change', function(event){
  (event.target.checked) ? document.body.setAttribute('data-theme', 'light') : document.body.removeAttribute('data-theme');
});

var themeSwitch = document.getElementById('themeSwitch');
if(themeSwitch) {
  initTheme(); // on page load, if user has already selected a specific theme -> apply it

  themeSwitch.addEventListener('change', function(event){
    resetTheme(); // update color theme
  });

  function initTheme() {
    var lightThemeSelected = (localStorage.getItem('themeSwitch') !== null && localStorage.getItem('themeSwitch') === 'light');
    // update checkbox
    themeSwitch.checked = lightThemeSelected;
    // update body data-theme attribute
    lightThemeSelected ? document.body.setAttribute('data-theme', 'light') : document.body.removeAttribute('data-theme');
  };

  function resetTheme() {
    if(themeSwitch.checked) { // dark theme has been selected
      document.body.setAttribute('data-theme', 'light');
      localStorage.setItem('themeSwitch', 'light'); // save theme selection 
    } else {
      document.body.removeAttribute('data-theme');
      localStorage.removeItem('themeSwitch'); // reset theme selection 
    } 
  };
}