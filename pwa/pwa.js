// Register service worker to control making site work offline
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js").then(() => {
      console.log("Service Worker Registered");
    });
  }
  
  
  let deferredPrompt;
  const addBtn = document.getElementById('install-button');
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    console.log("beforeinstall")
    // Stash the event so it can be triggered later.
    deferredPrompt = e;
    // Update UI to notify the user they can add to home screen
    addBtn.style.display = 'block';
  
    addBtn.addEventListener('click', () => {
      alert("CLicked")
      // hide our user interface that shows our A2HS button
      addBtn.style.display = 'none'; 
      // Show the prompt
      deferredPrompt.prompt();
      // Wait for the user to respond to the prompt
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the A2HS prompt');
        } else {
          console.log('User dismissedthe A2HS prompt');
        }
        deferredPrompt = null;
      });
    });
  });