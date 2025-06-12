// login modal script
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById("login-modal");
  const trigger = document.getElementById("login-trigger");
  const closeBtn = document.querySelector(".close-btn");

  if (trigger && modal && closeBtn) {
    trigger.onclick = () => modal.classList.remove("hidden");
    closeBtn.onclick = () => modal.classList.add("hidden");
    window.onclick = (e) => {
      if (e.target === modal) modal.classList.add("hidden");
    };
  }
});