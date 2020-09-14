// once zero is reached, play chime : https://codereview.stackexchange.com/questions/60347/simple-web-alarm-clock
// https://stackoverflow.com/questions/20618355/the-simplest-possible-javascript-countdown-timer

// Load chime sound
// const chime = new Audio('/static/Ticket-machine-sound.mp3');

// Assign trigger, duration and display to variables
const trigger = document.querySelector("#trigger"),
      duration = document.getElementById("setpomo").innerHTML * 60,
      display = document.querySelector('#display'),
      progress = document.querySelector("#progress");

// Listen for trigger being clicked
trigger.onclick = function() {
    // When user click on "Start" button
    if (trigger.innerHTML === "Start") {
        // Set trigger to "Stop"
        trigger.innerHTML = "Stop";
        // Start timer
        startTimer();

    // When user click on "Stop" button
    } else {
      // Set trigger to "Start"
      trigger.innerHTML = "Start";
    }
}

// Timer controller
const startTimer = function () {
    // As total duration is already on display, start countdown at (duration - 1)
    let timer = duration-1;
    // Update timer display after every second
    let countdown = setInterval(function () {
        // Split duration into minutes and seconds
        let minutes = parseInt(timer / 60, 10);
        let seconds = parseInt(timer % 60, 10);
        // Choose how to display minutes and seconds
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        // Set minutes and seconds in html
        display.textContent = minutes + ":" + seconds;

        // Calculate % of progress
        let progressPercent = 100 - ((timer*100) / duration)
        // Update progress bar
        progress.style.width = progressPercent + "%"

        // Decrement timer
        timer--;
        // When timer reaches 0
        if (timer < -1) {
            // Stop setInterval
            clearInterval(countdown);
            // Play chime to alert user
            chime.play();
            // Display notification in case volume is muted
            breakTime();
            // Reset diplay
            reset();
        // When user clicked "Stop" which sets button to "Start"
        } else if (trigger.innerHTML === "Start") {
            // Stop setInterval
            clearInterval(countdown);
            // Reset diplay
            reset();
        }
    }, 1000);
}

// Reset display to duration
const reset = function () {

    minutes = parseInt(duration / 60, 10);
    seconds = parseInt(duration % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    display.textContent = minutes + ":" + seconds;
    // Set trigger to "Start"
    trigger.innerHTML = "Start"
    // Reset progress bar
    progress.style.width = "0%"
}

// Show notification when timer reaches 0
const breakTime = function () {
  // Check if the browser supports notifications
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  }

  // Check whether notification permissions have already been granted
  else if (Notification.permission !== "granted") {
    // If permission is granted, create a notification
    let notification = new Notification("Time for a break!");
  }

  // Otherwise, ask the user for permission
  else if (Notification.permission !== "denied") {
    Notification.requestPermission().then(function (permission) {
      // If the user accepts, create a notification
      if (permission === "granted") {
        let notification = new Notification("Time for a break!");
      }
    });
  }
}