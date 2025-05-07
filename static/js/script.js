async function fetchLoggedInUser() {
  try {
    const response = await fetch("/api/loggedinuser", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    const data = await response.json();
    console.log("Response from logged-in user API:", data);

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
  const user = window.localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

function addUserToLocalStorage(user) {
  if (user) {
    window.localStorage.setItem("user", JSON.stringify(user));
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
        location.reload();
        // Reload the page to reflect the logged-in state
        //  add the logged in usar to the local storage of the browser
        addUsernameToLocalStorage(data.username);
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
// here is the js for the footer
