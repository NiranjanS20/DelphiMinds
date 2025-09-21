// Use relative paths for API calls to work in any environment
const API_BASE = '';

function saveTokens(tokens){
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
  if(tokens.user){ localStorage.setItem('user', JSON.stringify(tokens.user)); }
}

function getAccess(){ return localStorage.getItem('access_token'); }
function authHeaders(){ return { 'Authorization': `Bearer ${getAccess()}`, 'Content-Type': 'application/json' }; }

async function login(username, password){
  const res = await fetch(`/auth/login/`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username, password}) });
  if(!res.ok) throw new Error('Login failed');
  const data = await res.json();
  saveTokens(data);
  window.location.href = 'dashboard.html';
}

async function signup(payload){
  const res = await fetch(`/auth/register/`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
  if(!res.ok){
    let msg = 'Signup failed';
    try{ const data = await res.json(); msg = JSON.stringify(data); }catch(e){}
    throw new Error(msg);
  }
  await login(payload.username, payload.password);
}

async function fetchSkills(){
  const res = await fetch(`/skills/`, { headers: authHeaders() });
  if(!res.ok) throw new Error('Load skills failed');
  return res.json();
}

async function fetchMySkills(){
  const res = await fetch(`/skills/my/`, { headers: authHeaders() });
  if(!res.ok) throw new Error('Load my skills failed');
  return res.json();
}

async function addMySkill(skillId, level){
  const res = await fetch(`/skills/my/`, { method:'POST', headers: authHeaders(), body: JSON.stringify({ skill_id: skillId, level }) });
  if(!res.ok) throw new Error('Add skill failed');
  return res.json();
}

async function fetchRecommendations(){
  const res = await fetch(`/recommendations/`, { headers: authHeaders() });
  if(!res.ok) throw new Error('Recommendations failed');
  return res.json();
}

function requireAuth(){ if(!getAccess()){ window.location.href = 'login.html'; } }
function logout(){ localStorage.clear(); window.location.href = 'login.html'; }

// Sidebar toggle function for all pages
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('-translate-x-full');
        overlay.classList.toggle('hidden');
    }
}

// Get CSRF token function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', async () => {
  const loginForm = document.getElementById('loginForm');
  if(loginForm){
    loginForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const username = document.getElementById('login-username').value;
      const password = document.getElementById('login-password').value;
      try{ await login(username, password); } catch(err){ alert(err.message); }
    });
  }

  const signupForm = document.getElementById('signupForm');
  if(signupForm){
    signupForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const payload = {
        username: document.getElementById('su-username').value,
        email: document.getElementById('su-email').value,
        password: document.getElementById('su-password').value,
        role: document.getElementById('su-role').value,
      };
      try{ await signup(payload); } catch(err){ alert(err.message); }
    });
  }

  if(document.body.contains(document.getElementById('logoutBtn'))){
    document.getElementById('logoutBtn').addEventListener('click', logout);
  }

  // Dashboard logic
  if(window.location.pathname.endsWith('dashboard.html')){
    requireAuth();
    const skillSelect = document.getElementById('skillSelect');
    const mySkills = document.getElementById('mySkills');
    const recs = document.getElementById('recs');
    const addSkillForm = document.getElementById('addSkillForm');
    const refreshRecs = document.getElementById('refreshRecs');

    let skills = [];
    let mine = [];
    try{
      [skills, mine] = await Promise.all([fetchSkills(), fetchMySkills()]);
      skillSelect.innerHTML = skills.map(s=>`<option value="${s.id}">${s.name}</option>`).join('');
      mySkills.innerHTML = mine.map(m=>`<li class="flex justify-between border rounded p-2"><span>${m.skill.name}</span><span>${m.level}</span></li>`).join('');
    }catch(err){ alert(err.message); }

    addSkillForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const skillId = parseInt(skillSelect.value, 10);
      const level = parseInt(document.getElementById('skillLevel').value, 10);
      try{
        await addMySkill(skillId, level);
        const mine = await fetchMySkills();
        mySkills.innerHTML = mine.map(m=>`<li class="flex justify-between border rounded p-2"><span>${m.skill.name}</span><span>${m.level}</span></li>`).join('');
      }catch(err){ alert(err.message); }
    });

    refreshRecs.addEventListener('click', async ()=>{
      try{
        const list = await fetchRecommendations();
        recs.innerHTML = list.map(r=>`<div class="border rounded p-3"><div class="font-semibold">${r.career_path.title}</div><div class="text-sm text-gray-600">Score: ${r.score}%</div></div>`).join('');
      }catch(err){ alert(err.message); }
    });

    // Chart: visualize skill levels vs. 100 target
    const ctx = document.getElementById('skillsChart');
    if(ctx){
      const labels = mine.map(m=>m.skill.name);
      const data = mine.map(m=>m.level);
      // eslint-disable-next-line no-undef
      new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Your Level', data, backgroundColor: '#3b82f6' }] },
        options: { scales: { y: { beginAtZero: true, max: 100 } } }
      });
    }
  }
});


