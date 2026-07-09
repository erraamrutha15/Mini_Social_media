/* ============================================
   MiniSocial — Frontend Application (Vanilla JS)
   Complete SPA-like logic with Fetch API
   ============================================ */

// ── API Base URL ──
const API_BASE = 'https://minisocialmedia-production.up.railway.app';

// ============================================
// SECTION 1: Auth Utility Functions
// ============================================

/** Retrieve the stored authentication token from localStorage. */
function getToken() {
  return localStorage.getItem('token');
}

/** Retrieve the stored username from localStorage. */
function getUsername() {
  return localStorage.getItem('username');
}

/** Retrieve the stored user ID from localStorage. */
function getUserId() {
  return localStorage.getItem('user_id');
}

/**
 * Save authentication data to localStorage after login/register.
 * @param {string} token - The auth token.
 * @param {string} username - The user's username.
 * @param {string|number} userId - The user's ID.
 */
function setAuth(token, username, userId) {
  localStorage.setItem('token', token);
  localStorage.setItem('username', username);
  localStorage.setItem('user_id', String(userId));
}

/** Remove all authentication data from localStorage (logout). */
function clearAuth() {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  localStorage.removeItem('user_id');
}

/** Check whether the user is currently logged in. */
function isLoggedIn() {
  return !!getToken();
}

// ============================================
// SECTION 2: API Request Helper
// ============================================

/**
 * Perform an API request with automatic auth headers and JSON handling.
 * @param {string} endpoint - API endpoint path (e.g., '/posts/').
 * @param {string} method - HTTP method.
 * @param {object|null} body - Request body (will be JSON-stringified).
 * @returns {Promise<{ok: boolean, status: number, data: any}>}
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };

  const token = getToken();
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const config = { method, headers };
  if (body && method !== 'GET') {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);

    // Handle 204 No Content (e.g., delete)
    if (response.status === 204) {
      return { ok: true, status: 204, data: null };
    }

    const data = await response.json().catch(() => null);
    return { ok: response.ok, status: response.status, data };
  } catch (error) {
    console.error('API Request Error:', error);
    return {
      ok: false,
      status: 0,
      data: { detail: 'Network error. Make sure the Django server is running at http://127.0.0.1:8000' }
    };
  }
}

// ============================================
// SECTION 3: UI Helpers
// ============================================

/**
 * Show a toast notification message.
 * @param {string} message - The message to display.
 * @param {'success'|'error'} type - Toast type for styling.
 */
function showToast(message, type = 'success') {
  // Create container if it doesn't exist
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const icon = type === 'success' ? '✓' : '✕';
  toast.innerHTML = `
    <span class="toast-icon">${icon}</span>
    <span class="toast-message">${escapeHTML(message)}</span>
  `;

  container.appendChild(toast);

  // Auto-remove after 3.5 seconds
  setTimeout(() => {
    toast.classList.add('toast-exit');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/** Show the full-screen loading overlay. */
function showLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) overlay.classList.add('active');
}

/** Hide the full-screen loading overlay. */
function hideLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) overlay.classList.remove('active');
}

/**
 * Convert an ISO date string into a relative time string.
 * @param {string} dateString - ISO 8601 date string.
 * @returns {string} Human-readable relative time.
 */
function timeAgo(dateString) {
  const now = new Date();
  const date = new Date(dateString);
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 10) return 'just now';

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 },
  ];

  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
    }
  }

  return 'just now';
}

/**
 * Escape HTML special characters to prevent XSS.
 * @param {string} str - Raw string.
 * @returns {string} Escaped string safe for innerHTML.
 */
function escapeHTML(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Get the first letter of a string, uppercased (for avatars).
 * @param {string} str
 * @returns {string}
 */
function getInitial(str) {
  return str ? str.charAt(0).toUpperCase() : '?';
}

/**
 * Parse error response from Django REST Framework into a readable string.
 * @param {object} data - Error response data.
 * @returns {string}
 */
function parseErrors(data) {
  if (!data) return 'An unknown error occurred.';
  if (typeof data === 'string') return data;
  if (data.detail) return data.detail;

  // DRF field errors: { field: ["error1", "error2"] }
  const messages = [];
  for (const key in data) {
    if (Array.isArray(data[key])) {
      messages.push(`${key}: ${data[key].join(', ')}`);
    } else {
      messages.push(`${key}: ${data[key]}`);
    }
  }
  return messages.join(' | ') || 'An unknown error occurred.';
}

// ============================================
// SECTION 4: Authentication Functions
// ============================================

/**
 * Register a new user account.
 * On success, stores auth data and redirects to feed.
 */
async function register(username, email, password, firstName, lastName) {
  showLoading();
  const res = await apiRequest('/api/accounts/register/', 'POST', {
    username,
    email,
    password,
    first_name: firstName,
    last_name: lastName,
  });
  hideLoading();

  if (res.ok) {
    setAuth(res.data.token, res.data.username, res.data.user_id);
    showToast('Account created successfully! Welcome! 🎉');
    setTimeout(() => { window.location.href = 'feed.html'; }, 600);
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Log in with existing credentials.
 * On success, stores auth data and redirects to feed.
 */
async function login(username, password) {
  showLoading();
  const res = await apiRequest('/accounts/login/', 'POST', { username, password });
  hideLoading();

  if (res.ok) {
    setAuth(res.data.token, res.data.username, res.data.user_id);
    showToast(`Welcome back, ${res.data.username}! 👋`);
    setTimeout(() => { window.location.href = 'feed.html'; }, 600);
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/** Log out: clear auth data and redirect to home page. */
function logout() {
  clearAuth();
  window.location.href = 'index.html';
}

// ============================================
// SECTION 5: Post Functions
// ============================================

/** Load all posts from the API and render them into the feed. */
async function loadPosts() {
  showLoading();
  const res = await apiRequest('/api/posts/');
  hideLoading();

  if (res.ok) {
    renderPosts(res.data);
  } else {
    showToast('Failed to load posts.', 'error');
  }
}

/**
 * Create a new post with the given content.
 * @param {string} content - Post text content.
 * @param {File} mediaFile - Optional media file (image/video).
 */
async function createPost(content, mediaFile = null) {
  if (!content.trim() && !mediaFile) {
    showToast('Post content or media cannot be empty.', 'error');
    return;
  }

  showLoading();
  let res;
  
  if (mediaFile) {
    // Use FormData for file uploads
    const formData = new FormData();
    formData.append('content', content);
    
    if (mediaFile.type.startsWith('image/')) {
      formData.append('image', mediaFile);
    } else if (mediaFile.type.startsWith('video/')) {
      formData.append('video', mediaFile);
    }

    const headers = {};
    const token = getToken();
    if (token) headers['Authorization'] = `Token ${token}`;

    try {
      const response = await fetch(`${API_BASE}/posts/`, {
        method: 'POST',
        headers,
        body: formData
      });
      const data = await response.json().catch(() => null);
      res = { ok: response.ok, status: response.status, data };
    } catch (err) {
      res = { ok: false, data: { detail: 'Network error.' } };
    }
  } else {
    // Normal JSON request
    res = await apiRequest('/posts/', 'POST', { content });
  }
  
  hideLoading();

  if (res.ok) {
    showToast('Post published! 🚀');
    const textarea = document.getElementById('post-content');
    const fileInput = document.getElementById('post-media');
    if (textarea) textarea.value = '';
    if (fileInput) fileInput.value = '';
    loadPosts();
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Delete a post by ID (only own posts).
 * @param {number} postId - The post ID to delete.
 */
async function deletePost(postId) {
  if (!confirm('Are you sure you want to delete this post?')) return;

  showLoading();
  const res = await apiRequest(`/posts/${postId}/`, 'DELETE');
  hideLoading();

  if (res.ok) {
    showToast('Post deleted.');
    loadPosts();
  } else {
    showToast('Failed to delete post.', 'error');
  }
}

/**
 * Like a post.
 * @param {number} postId
 */
async function likePost(postId) {
  const res = await apiRequest(`/posts/${postId}/like/`, 'POST');
  if (res.ok) {
    loadPosts();
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Unlike a post.
 * @param {number} postId
 */
async function unlikePost(postId) {
  const res = await apiRequest(`/posts/${postId}/unlike/`, 'POST');
  if (res.ok) {
    loadPosts();
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Toggle like/unlike based on current state.
 * @param {number} postId
 * @param {boolean} isLiked - Current like state.
 */
function toggleLike(postId, isLiked) {
  if (!isLoggedIn()) {
    showToast('Please log in to like posts.', 'error');
    return;
  }
  if (isLiked) {
    unlikePost(postId);
  } else {
    likePost(postId);
  }
}

// ============================================
// SECTION 6: Comment Functions
// ============================================

/**
 * Toggle the comments section visibility for a post.
 * @param {number} postId
 */
function loadComments(postId) {
  const section = document.getElementById(`comments-${postId}`);
  if (!section) return;

  if (section.classList.contains('open')) {
    section.classList.remove('open');
  } else {
    section.classList.add('open');
  }
}

/**
 * Add a comment to a post.
 * @param {number} postId
 * @param {string} content - Comment text.
 */
async function addComment(postId, content) {
  if (!content.trim()) {
    showToast('Comment cannot be empty.', 'error');
    return;
  }

  const res = await apiRequest(`/posts/${postId}/comments/`, 'POST', { content });

  if (res.ok) {
    showToast('Comment added! 💬');
    const input = document.getElementById(`comment-input-${postId}`);
    if (input) input.value = '';
    loadPosts();
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Handle the comment form submission.
 * @param {Event} e - Form submit event.
 * @param {number} postId
 */
function handleAddComment(e, postId) {
  e.preventDefault();
  const input = document.getElementById(`comment-input-${postId}`);
  if (input) {
    addComment(postId, input.value);
  }
}

// ============================================
// SECTION 7: Profile Functions
// ============================================

/**
 * Load a user's profile and render it.
 * @param {string} username - The username to load.
 */
async function loadProfile(username) {
  showLoading();
  const res = await apiRequest(`/accounts/profile/${username}/`);
  hideLoading();

  if (res.ok) {
    renderProfile(res.data);
  } else {
    showToast('Failed to load profile.', 'error');
    const container = document.getElementById('profile-content');
    if (container) {
      container.innerHTML = `
        <div class="card">
          <div class="empty-state">
            <div class="empty-icon">😕</div>
            <h3>Profile not found</h3>
            <p>The user "${escapeHTML(username)}" doesn't exist.</p>
          </div>
        </div>
      `;
    }
  }
}

/**
 * Update the current user's profile.
 * @param {string} bio
 * @param {string} firstName
 * @param {string} lastName
 */
async function updateProfile(bio, firstName, lastName) {
  const username = getUsername();
  showLoading();
  const res = await apiRequest(`/accounts/profile/${username}/`, 'PUT', {
    bio,
    first_name: firstName,
    last_name: lastName,
  });
  hideLoading();

  if (res.ok) {
    showToast('Profile updated! ✨');
    loadProfile(username);
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Follow a user by their ID.
 * @param {number} userId
 */
async function followUser(userId) {
  const res = await apiRequest('/accounts/follow/', 'POST', { following_id: userId });
  if (res.ok) {
    showToast('Followed! 🤝');
    // Reload the profile page to update the state
    const urlParams = new URLSearchParams(window.location.search);
    const profileUser = urlParams.get('user') || getUsername();
    loadProfile(profileUser);
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/**
 * Unfollow a user by their ID.
 * @param {number} userId
 */
async function unfollowUser(userId) {
  const res = await apiRequest('/accounts/unfollow/', 'POST', { following_id: userId });
  if (res.ok) {
    showToast('Unfollowed.');
    const urlParams = new URLSearchParams(window.location.search);
    const profileUser = urlParams.get('user') || getUsername();
    loadProfile(profileUser);
  } else {
    showToast(parseErrors(res.data), 'error');
  }
}

/** Load the list of all users for the "Discover" sidebar. */
async function loadUsers() {
  const res = await apiRequest('/accounts/users/');
  if (res.ok) {
    renderUsers(res.data);
  }
}

// ============================================
// SECTION 8: Rendering — Posts
// ============================================

/**
 * Render an array of post objects into the posts list container.
 * @param {Array} posts - Array of post objects from the API.
 */
function renderPosts(posts) {
  const container = document.getElementById('posts-list');
  if (!container) return;

  if (!posts || posts.length === 0) {
    container.innerHTML = `
      <div class="card">
        <div class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>No posts yet</h3>
          <p>Be the first to share something with the community!</p>
        </div>
      </div>
    `;
    return;
  }

  const currentUser = getUsername();
  container.innerHTML = posts.map((post, index) => {
    const isOwn = post.author_username === currentUser;
    const likedClass = post.is_liked ? 'liked' : '';
    const heartIcon = post.is_liked ? '♥' : '♡';
    const authorInitial = getInitial(post.author_username);

    // Build comments HTML
    const commentsHTML = (post.comments || []).map(comment => `
      <div class="comment-item">
        <div class="comment-avatar">${getInitial(comment.author_username)}</div>
        <div class="comment-body">
          <strong><a href="profile.html?user=${encodeURIComponent(comment.author_username)}">${escapeHTML(comment.author_username)}</a></strong>
          <p>${escapeHTML(comment.content)}</p>
          <div class="comment-time">${timeAgo(comment.created_at)}</div>
        </div>
      </div>
    `).join('');

    // Build media HTML
    let mediaHTML = '';
    if (post.image) {
      mediaHTML = `<img src="${post.image}" class="post-media-content" alt="Post Image" />`;
    } else if (post.video) {
      mediaHTML = `<video controls class="post-media-content"><source src="${post.video}" type="video/mp4">Your browser does not support the video tag.</video>`;
    }

    return `
      <div class="post-card" style="animation-delay: ${index * 80}ms">
        <div class="post-header">
          <div class="post-author">
            <div class="post-avatar">${authorInitial}</div>
            <div class="post-author-info">
              <h4><a href="profile.html?user=${encodeURIComponent(post.author_username)}">${escapeHTML(post.author_username)}</a></h4>
              <span class="post-time">${timeAgo(post.created_at)}</span>
            </div>
          </div>
          ${isOwn ? `
            <button class="post-action-btn post-delete-btn" onclick="deletePost(${post.id})" title="Delete post">
              🗑
            </button>
          ` : ''}
        </div>

        <div class="post-content">${escapeHTML(post.content)}</div>
        ${mediaHTML}

        <div class="post-actions">
          <button class="post-action-btn ${likedClass}" onclick="toggleLike(${post.id}, ${post.is_liked})">
            <span class="action-icon">${heartIcon}</span>
            <span>${post.like_count || 0}</span>
          </button>

          <button class="post-action-btn" onclick="loadComments(${post.id})">
            <span class="action-icon">💬</span>
            <span>${post.comment_count || 0}</span>
          </button>
        </div>

        <div class="comments-section" id="comments-${post.id}">
          <div class="comments-list">
            ${commentsHTML || '<p class="text-muted" style="font-size: 0.85rem; padding: 8px 0;">No comments yet.</p>'}
          </div>
          <form class="comment-form" onsubmit="handleAddComment(event, ${post.id})">
            <input type="text" class="form-input" id="comment-input-${post.id}" placeholder="Write a comment..." autocomplete="off">
            <button type="submit" class="btn btn-primary btn-sm">Post</button>
          </form>
        </div>
      </div>
    `;
  }).join('');
}

// ============================================
// SECTION 9: Rendering — Profile
// ============================================

/**
 * Render the profile data into the profile page.
 * @param {object} profile - Profile object from the API.
 */
function renderProfile(profile) {
  const container = document.getElementById('profile-content');
  if (!container) return;

  const isOwnProfile = profile.username === getUsername();
  const initial = getInitial(profile.username);
  const fullName = [profile.first_name, profile.last_name].filter(Boolean).join(' ') || profile.username;

  // Profile card
  let html = `
    <div class="card profile-card">
      <div class="profile-avatar-lg">${initial}</div>
      <h2 class="profile-name">${escapeHTML(fullName)}</h2>
      <p class="profile-username">@${escapeHTML(profile.username)}</p>
      <p class="profile-bio">${profile.bio ? escapeHTML(profile.bio) : 'No bio yet.'}</p>
      <div class="profile-stats">
        <div class="profile-stat">
          <div class="stat-number">${profile.followers_count || 0}</div>
          <div class="stat-label">Followers</div>
        </div>
        <div class="profile-stat">
          <div class="stat-number">${profile.following_count || 0}</div>
          <div class="stat-label">Following</div>
        </div>
        <div class="profile-stat">
          <div class="stat-number">${(profile.posts || []).length}</div>
          <div class="stat-label">Posts</div>
        </div>
      </div>
  `;

  // Follow / Unfollow button (only on other users' profiles)
  if (!isOwnProfile && isLoggedIn()) {
    if (profile.is_following) {
      html += `<button class="btn btn-secondary" onclick="unfollowUser(${profile.id})">Unfollow</button>`;
    } else {
      html += `<button class="btn btn-primary" onclick="followUser(${profile.id})">Follow</button>`;
    }
  }

  html += `</div>`;

  // Edit profile form (own profile only)
  if (isOwnProfile) {
    html += `
      <div class="card edit-profile-section">
        <h3>✏️ Edit Profile</h3>
        <form id="edit-profile-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="edit-first-name">First Name</label>
              <input type="text" class="form-input" id="edit-first-name" value="${escapeHTML(profile.first_name || '')}" placeholder="First name">
            </div>
            <div class="form-group">
              <label class="form-label" for="edit-last-name">Last Name</label>
              <input type="text" class="form-input" id="edit-last-name" value="${escapeHTML(profile.last_name || '')}" placeholder="Last name">
            </div>
          </div>
          <div class="form-group">
            <label class="form-label" for="edit-bio">Bio</label>
            <textarea class="form-input" id="edit-bio" rows="3" placeholder="Tell us about yourself...">${escapeHTML(profile.bio || '')}</textarea>
          </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
      </div>
    `;
  }

  // User's posts section
  html += `
    <div>
      <h3 class="section-title"><span class="title-icon">📄</span> Posts</h3>
  `;

  if (profile.posts && profile.posts.length > 0) {
    html += profile.posts.map(post => {
      let mediaHTML = '';
      if (post.image) {
        mediaHTML = `<img src="${post.image}" class="post-media-content" alt="Post Image" />`;
      } else if (post.video) {
        mediaHTML = `<video controls class="post-media-content"><source src="${post.video}" type="video/mp4">Your browser does not support the video tag.</video>`;
      }
      
      return `
      <div class="post-card">
        <div class="post-content">${escapeHTML(post.content)}</div>
        ${mediaHTML}
        <div class="post-actions">
          <span class="post-action-btn" style="cursor:default;">
            <span class="action-icon">♥</span>
            <span>${post.like_count || 0}</span>
          </span>
          <span class="post-action-btn" style="cursor:default;">
            <span class="action-icon">💬</span>
            <span>${post.comment_count || 0}</span>
          </span>
          <span class="post-time" style="margin-left:auto;">${timeAgo(post.created_at)}</span>
        </div>
      </div>
    `}).join('');
  } else {
    html += `
      <div class="card">
        <div class="empty-state">
          <div class="empty-icon">📭</div>
          <h3>No posts yet</h3>
          <p>${isOwnProfile ? 'Head to the feed to create your first post!' : "This user hasn't posted yet."}</p>
        </div>
      </div>
    `;
  }

  html += `</div>`;
  container.innerHTML = html;

  // Attach edit profile form handler if own profile
  if (isOwnProfile) {
    const editForm = document.getElementById('edit-profile-form');
    if (editForm) {
      editForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const bio = document.getElementById('edit-bio').value;
        const firstName = document.getElementById('edit-first-name').value;
        const lastName = document.getElementById('edit-last-name').value;
        updateProfile(bio, firstName, lastName);
      });
    }
  }
}

// ============================================
// SECTION 10: Rendering — Users List (Discover)
// ============================================

/**
 * Render a list of users in the sidebar "Discover People" section.
 * @param {Array} users - Array of user objects.
 */
function renderUsers(users) {
  const container = document.getElementById('users-list');
  if (!container) return;

  const currentUser = getUsername();
  const otherUsers = users.filter(u => u.username !== currentUser);

  if (otherUsers.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="padding: 16px 0;">
        <p class="text-muted" style="font-size: 0.85rem;">No other users yet. Invite your friends!</p>
      </div>
    `;
    return;
  }

  container.innerHTML = otherUsers.map(user => {
    const fullName = [user.first_name, user.last_name].filter(Boolean).join(' ');
    return `
      <a href="profile.html?user=${encodeURIComponent(user.username)}" class="user-card">
        <div class="user-avatar">${getInitial(user.username)}</div>
        <div class="user-info">
          <h4>${escapeHTML(user.username)}</h4>
          <p>${fullName ? escapeHTML(fullName) : 'MiniSocial user'}</p>
        </div>
      </a>
    `;
  }).join('');
}

// ============================================
// SECTION 11: Navigation Helpers
// ============================================

/**
 * Update navigation bar based on login state.
 * Highlights the active page link and shows/hides auth-dependent links.
 */
function updateNavigation() {
  const loggedIn = isLoggedIn();
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  // Update nav links visibility
  document.querySelectorAll('.nav-auth-link').forEach(el => {
    if (loggedIn) {
      el.classList.remove('disabled');
    } else {
      el.classList.add('disabled');
    }
  });

  // Show/hide login vs logout buttons
  const loginLink = document.getElementById('nav-login');
  const logoutLink = document.getElementById('nav-logout');
  if (loginLink) loginLink.style.display = loggedIn ? 'none' : '';
  if (logoutLink) logoutLink.style.display = loggedIn ? '' : 'none';

  // Set active state on current page nav link
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });
}

/**
 * Redirect to index.html if the user is not authenticated.
 * Used to protect feed and profile pages.
 */
function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = 'index.html';
    return false;
  }
  return true;
}

// ============================================
// SECTION 12: Page Initialization
// ============================================

/**
 * Initialize the Home page (index.html).
 * Sets up auth tabs and login/register form handlers.
 */
function initHomePage() {
  updateNavigation();

  // If already logged in, redirect to feed
  if (isLoggedIn()) {
    window.location.href = 'feed.html';
    return;
  }

  // Auth tab switching
  const tabs = document.querySelectorAll('.auth-tab');
  const forms = document.querySelectorAll('.auth-form');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;

      tabs.forEach(t => t.classList.remove('active'));
      forms.forEach(f => f.classList.remove('active'));

      tab.classList.add('active');
      document.getElementById(`${target}-form`).classList.add('active');
    });
  });

  // Login form submission
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const username = document.getElementById('login-username').value.trim();
      const password = document.getElementById('login-password').value;

      if (!username || !password) {
        showToast('Please fill in all fields.', 'error');
        return;
      }

      login(username, password);
    });
  }

  // Register form submission
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const username = document.getElementById('reg-username').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const password = document.getElementById('reg-password').value;
      const firstName = document.getElementById('reg-first-name').value.trim();
      const lastName = document.getElementById('reg-last-name').value.trim();

      if (!username || !email || !password) {
        showToast('Username, email, and password are required.', 'error');
        return;
      }

      register(username, email, password, firstName, lastName);
    });
  }
}

/**
 * Initialize the Feed page (feed.html).
 * Loads posts and sets up the create-post form.
 */
function initFeedPage() {
  if (!requireAuth()) return;
  updateNavigation();

  // Load posts on page load
  loadPosts();

  // Create post form
  const createForm = document.getElementById('create-post-form');
  if (createForm) {
    createForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const content = document.getElementById('post-content').value;
      const fileInput = document.getElementById('post-media');
      const file = fileInput && fileInput.files.length > 0 ? fileInput.files[0] : null;
      createPost(content, file);
    });
  }

  // Display greeting
  const greeting = document.getElementById('feed-greeting');
  if (greeting) {
    greeting.textContent = `What's on your mind, ${getUsername()}?`;
  }
}

/**
 * Initialize the Profile page (profile.html).
 * Reads ?user= query param, loads profile and user list.
 */
function initProfilePage() {
  if (!requireAuth()) return;
  updateNavigation();

  // Determine which profile to load
  const urlParams = new URLSearchParams(window.location.search);
  const profileUsername = urlParams.get('user') || getUsername();

  loadProfile(profileUsername);
  loadUsers();
}
