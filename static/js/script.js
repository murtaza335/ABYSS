async function fetchLoggedInUser() {
  try {
    const response = await fetch("/api/loggedinuser", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    const data = await response.json();
    console.log("api called server");

    if (data.error) {
      console.warn("User not logged in");
      return null;
    }

    // Store only valid data
    addUserToLocalStorage(data);
    return data;
  } catch (error) {
    console.error("Error fetching logged-in user:", error);
    return null;
  }
}

function getLoggedInUserLocal() {
  if (!window.localStorage) {
    if ((username = fetchLoggedInUser())) {
      window.localStorage.setItem("username", JSON.stringify(username));
      return username;
    } else {
      return null;
    }
  } // Check if localStorage is available
  const user = window.localStorage.getItem("username");
  return user ? JSON.parse(user) : null;
}

function addUserToLocalStorage(user) {
  if (user) {
    window.localStorage.setItem("username", JSON.stringify(user));
    console.log("User added to local storage:", user);
  } else {
    console.error("Invalid user object provided.");
  }
}

function showLoginPopup() {
  if (document.getElementById("loginPopup")) return;

  // Overlay
  const overlay = document.createElement("div");
  overlay.id = "popupOverlay";
  overlay.style.cssText = `
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background-color: rgba(11, 12, 16, 0.85);
      z-index: 999;
    `;

  // Popup container
  const popup = document.createElement("div");
  popup.id = "loginPopup";
  popup.style.cssText = `
      position: fixed;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      background-color: #0b0c10;
      color: #c5c6c7;
      border: 2px solid #45a29e;
      border-radius: 12px;
      padding: 24px;
      z-index: 1000;
      width: 320px;
      font-family: 'Segoe UI', Tahoma, sans-serif;
      box-shadow: 0 0 30px rgba(102, 252, 241, 0.2);
    `;

  popup.innerHTML = `
      <h2 style="color: #66fcf1; margin-top: 0;">Login</h2>
      <input type="text" id="popupUsername" placeholder="Username"
        style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #45a29e; background-color: #1f2833; color: #c5c6c7; border-radius: 6px; font-size: 14px;" />
      <input type="password" id="popupPassword" placeholder="Password"
        style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #45a29e; background-color: #1f2833; color: #c5c6c7; border-radius: 6px; font-size: 14px;" />
      <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px;">
        <button id="loginCancel"
          style="padding: 10px 16px; background: transparent; color: #c5c6c7; border: 1px solid #c5c6c7; border-radius: 6px; cursor: pointer;">
          Cancel
        </button>
        <button id="loginSubmit"
          style="padding: 10px 16px; background: #66fcf1; color: #0b0c10; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">
          Login
        </button>
      </div>
      <p style="margin-top: 16px; text-align: center; font-size: 14px;">
        Don’t have an account?
        <a id="signupLink" href="#" style="color: #66fcf1; text-decoration: underline; cursor: pointer;">Sign up</a>
      </p>
    `;

  document.body.appendChild(overlay);
  document.body.appendChild(popup);

  // Button actions
  document.getElementById("loginSubmit").onclick = function () {
    const username = document.getElementById("popupUsername").value.trim();
    const password = document.getElementById("popupPassword").value.trim();

    if (!username || !password) {
      alert("Please enter both username and password.");
      return;
    }

    fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Invalid credentials");
        return response.json();
      })
      .then((data) => {
        addUserToLocalStorage(data.username);
        console.log("Username saved:", data.username);
        // Only reload after storage
        setTimeout(() => location.reload(), 100);
        // Reload the page to reflect the logged-in state
        //  add the logged in usar to the local storage of the browser

        closePopup();
      })
      .catch((err) => {
        alert("Login failed: " + err.message);
      });
  };

  document.getElementById("loginCancel").onclick = closePopup;
  overlay.onclick = closePopup;

  // Signup link logic
  document.getElementById("signupLink").onclick = function (e) {
    e.preventDefault();
    closePopup();
    window.location.href = "/auth"; // Change to your actual signup page/route
  };

  function closePopup() {
    document.body.removeChild(popup);
    document.body.removeChild(overlay);
  }
}

// following is the logic for the upvote of the discusions
function voteDiscussion(username, discussionId, callback) {
  if (!username || !discussionId) {
    console.error("Missing username or discussion ID.");
    return;
  }

  fetch(`/api/voteDiscussion/${username}/${discussionId}`, {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (callback) callback(data);
    })
    .catch((err) => {
      console.error("Vote request failed:", err);
      if (callback) callback(false);
    });
}

// check if the user has upvoted or not
async function checkUserUpvoted(username, discussionId) {
  try {
    const res = await fetch(
      `/api/checkUpvoteDiscussion/${username}/${discussionId}`,
      {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch upvote status");
    }

    const data = await res.json();

    if (data.success) {
      if (data.upvote) {
        document
          .getElementById("upvote-button")
          .classList.remove("text-abyss-light");
        document
          .getElementById("upvote-button")
          .classList.add("text-abyss-accent");
      }
    }
  } catch (err) {
    console.error("Error checking upvote status:", err);
  }
}
// here is the js for the navigation bar
function goToHome() {
  window.location.href = "/";
}

function goToLeaderboard() {
  window.location.href = "/";
}

function goToCommunity() {
  window.location.href = "/community";
}

function goToProfile() {
  if ((username = getLoggedInUserLocal())) {
    console.log("User is logged in:", username);
    window.location.href = `/profilepage/${username}`;
  } else {
    showLoginPopup();
  }
}

function logout() {
  fetch("/api/logout", {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Logout failed");
      }
      return response.json();
    })
    .then((data) => {
      window.localStorage.removeItem("username"); // Clear local storage
      //  we will just reload the page to reflect the changes
      setTimeout(() => location.reload(), 100);
    })
    .catch((error) => {
      console.error("Error during logout:", error);
      alert("Logout failed. Please try again.");
    });
}

function toggleProfileDropdown() {
  if (!getLoggedInUserLocal()) {
    showLoginPopup();
    return;
  }
  const dropdown = document.getElementById("profileDropdown");
  dropdown.style.display =
    dropdown.style.display === "block" ? "none" : "block";
}

// Optional: Close dropdown if user clicks outside of it
document.addEventListener("click", function (event) {
  const dropdown = document.getElementById("profileDropdown");
  const profileMenu = document.querySelector(".profile-menu");
  if (!profileMenu.contains(event.target)) {
    dropdown.style.display = "none";
  }
});

// navigate to page logic
function navigateToPage(url) {
  window.location.href = url;
}

//responsive navbar
// Toggle mobile menu
function toggleMobileMenu() {
  const hamburger = document.querySelector(".hamburger");
  const navMenu = document.getElementById("nav-menu");

  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
}

// Toggle profile dropdown
// function toggleProfileDropdown() {
//   const dropdown = document.getElementById("profileDropdown");

//   // On mobile, simply toggle display
//   if (window.innerWidth <= 768) {
//     if (dropdown.style.display === "block") {
//       dropdown.style.display = "none";
//     } else {
//       dropdown.style.display = "block";
//     }
//   } else {
//     // On desktop, check if dropdown is outside viewport
//     dropdown.style.display =
//       dropdown.style.display === "block" ? "none" : "block";
//   }
// }

// Close mobile menu when clicking a link
document.querySelectorAll("#nav-menu a").forEach((link) => {
  link.addEventListener("click", function () {
    if (window.innerWidth <= 768) {
      // Don't close menu when opening profile dropdown
      if (this.textContent !== "Profile") {
        document.querySelector(".hamburger").classList.remove("active");
        document.getElementById("nav-menu").classList.remove("active");
      }
    }
  });
});

// Close dropdown and menu when clicking outside
document.addEventListener("click", function (event) {
  const dropdown = document.getElementById("profileDropdown");
  const profileLink = document.querySelector(".profile-menu > a");
  const navMenu = document.getElementById("nav-menu");
  const hamburger = document.querySelector(".hamburger");

  // Close profile dropdown if clicking outside profile menu
  if (
    !event.target.closest(".profile-menu") &&
    dropdown.style.display === "block"
  ) {
    dropdown.style.display = "none";
  }

  // Close mobile menu if clicking outside nav menu and hamburger
  if (
    window.innerWidth <= 768 &&
    !event.target.closest("#nav-menu") &&
    !event.target.closest(".hamburger") &&
    navMenu.classList.contains("active")
  ) {
    navMenu.classList.remove("active");
    hamburger.classList.remove("active");
  }
});
// function to get relative time 
function getRelativeTime(dateStr) {
  const now = new Date();
  const past = new Date(dateStr);
  const diffMs = now - past;

  const minutes = Math.floor(diffMs / (1000 * 60));
  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);

  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}min`;
  if (hours < 24) return `${hours}hr`;
  if (days < 30) return `${days}d`;
  if (days < 365) return `${months}months`;
  return `${years}y`;
}

// footer js 
 // Footer JavaScript Functionality
    document.addEventListener('DOMContentLoaded', function() {
      // Mobile accordion for footer columns
      const footerHeadings = document.querySelectorAll('.footer-column h3');
      
      // Only apply accordion on mobile screens
      function setupFooterAccordion() {
        if (window.innerWidth <= 576) {
          footerHeadings.forEach(heading => {
            // Add click event and toggle class
            heading.addEventListener('click', toggleAccordion);
            heading.classList.add('accordion-toggle');
          });
        } else {
          // Remove accordion functionality on larger screens
          footerHeadings.forEach(heading => {
            heading.removeEventListener('click', toggleAccordion);
            heading.classList.remove('accordion-toggle');
            
            // Make sure lists are visible on desktop
            const content = heading.nextElementSibling;
            if (content && (content.tagName === 'UL' || content.tagName === 'P')) {
              content.style.maxHeight = 'none';
              content.style.opacity = '1';
            }
          });
        }
      }
      
      // Toggle accordion function
      function toggleAccordion() {
        this.classList.toggle('active');
        
        // Toggle the next element (ul or p)
        let content = this.nextElementSibling;
        
        // Handle first column specially (has both p and social icons)
        if (content && content.tagName === 'P') {
          if (this.classList.contains('active')) {
            content.style.maxHeight = content.scrollHeight + 'px';
            content.style.opacity = '1';
            
            // Also show social icons
            const socialIcons = content.nextElementSibling;
            if (socialIcons && socialIcons.classList.contains('social-icons')) {
              socialIcons.style.maxHeight = socialIcons.scrollHeight + 'px';
              socialIcons.style.opacity = '1';
            }
          } else {
            content.style.maxHeight = '0';
            content.style.opacity = '0';
            
            // Also hide social icons
            const socialIcons = content.nextElementSibling;
            if (socialIcons && socialIcons.classList.contains('social-icons')) {
              socialIcons.style.maxHeight = '0';
              socialIcons.style.opacity = '0';
            }
          }
        } 
        // Handle navigation lists
        else if (content && content.tagName === 'UL') {
          if (this.classList.contains('active')) {
            content.style.maxHeight = content.scrollHeight + 'px';
            content.style.opacity = '1';
          } else {
            content.style.maxHeight = '0';
            content.style.opacity = '0';
          }
        }
      }
      
      // Smooth scroll to top when clicking the logo
      const logoElement = document.querySelector('.footer-column h3');
      if (logoElement && logoElement.textContent.trim() === 'ABYSS') {
        logoElement.style.cursor = 'pointer';
        logoElement.addEventListener('click', function(e) {
          if (window.innerWidth > 576) { // Only on desktop
            e.preventDefault();
            window.scrollTo({
              top: 0,
              behavior: 'smooth'
            });
          }
        });
      }
      
      // Animate social icons on hover
      const socialIcons = document.querySelectorAll('.social-icon');
      socialIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
          this.style.transform = 'translateY(-3px)';
        });
        
        icon.addEventListener('mouseleave', function() {
          this.style.transform = 'translateY(0)';
        });
      });
      
      // Add year dynamically to copyright
      const copyrightYear = document.querySelector('.copyright p');
      if (copyrightYear) {
        const currentYear = new Date().getFullYear();
        copyrightYear.innerHTML = copyrightYear.innerHTML.replace(/\d{4}/, currentYear);
      }
      
      // Initialize the accordion behavior
      setupFooterAccordion();
      
      // Update accordion on window resize
      window.addEventListener('resize', setupFooterAccordion);
      
      // Add scroll to top button functionality
      const scrollTopBtn = document.createElement('button');
      scrollTopBtn.innerHTML = '&uarr;';
      scrollTopBtn.className = 'scroll-top-btn';
      document.body.appendChild(scrollTopBtn);
      
      // Show/hide scroll button based on scroll position
      window.addEventListener('scroll', function() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
          scrollTopBtn.classList.add('visible');
        } else {
          scrollTopBtn.classList.remove('visible');
        }
      });
      
      // Scroll to top when button is clicked
      scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    });




