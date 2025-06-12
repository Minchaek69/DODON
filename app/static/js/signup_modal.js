document.addEventListener('DOMContentLoaded', function () {
  const signupModal = document.getElementById("signup-modal");
  const signupTriggers = document.querySelectorAll(".open-signup");
  const signupClose = document.querySelector(".signup-close");

  if (signupModal && signupTriggers.length > 0) {
    signupTriggers.forEach(btn => {
      btn.onclick = () => signupModal.classList.remove("hidden");
    });
    signupClose.onclick = () => signupModal.classList.add("hidden");
    window.onclick = (e) => {
      if (e.target === signupModal) signupModal.classList.add("hidden");
    };
  }
});