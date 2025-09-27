<template>
  <div class="loading-wrap">
    <div class="glow"></div>
    <div class="card">
      <img class="logo" src="/src/assets/logo.png" alt="HawAI" />
      <h1 class="brand">Haw<span>AI</span></h1>
      <p class="tag">İyiliğin aklı • Akılcı ilk yardım</p>
      <div class="dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts"></script>

<style scoped>
.loading-wrap {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: radial-gradient(1200px 600px at 50% -10%, rgba(34,197,94,.10), transparent),
              radial-gradient(800px 400px at 100% 0%, rgba(16,185,129,.15), transparent),
              linear-gradient(180deg, var(--bg), var(--bg));
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  z-index: 2000;
}

.glow {
  position: absolute;
  width: 520px;
  height: 520px;
  border-radius: 50%;
  background: radial-gradient(closest-side, rgba(34,197,94,.25), rgba(34,197,94,0));
  filter: blur(30px);
  animation: float 5.2s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0) scale(1); opacity: .9; }
  50% { transform: translateY(-12px) scale(1.02); opacity: 1; }
  100% { transform: translateY(0) scale(1); opacity: .9; }
}

.card {
  position: relative;
  padding: 40px 48px;
  border-radius: 20px;
  border: 1px solid rgba(34,197,94,.25);
  background: linear-gradient(180deg, rgba(255,255,255,.75), rgba(255,255,255,.65));
  box-shadow: 0 10px 40px rgba(16,185,129,.15);
  text-align: center;
}
:root[data-theme='dark'] .card {
  background: linear-gradient(180deg, rgba(17,24,39,.85), rgba(17,24,39,.75));
}

.logo {
  width: 72px;
  height: 72px;
  object-fit: contain;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,.15);
}

.brand {
  margin: 12px 0 6px 0;
  font-size: 40px;
  letter-spacing: .3px;
  font-weight: 900;
  color: var(--text-900);
}
.brand span { color: var(--brand-600); }

.tag {
  margin: 0 0 18px 0;
  color: var(--text-600);
}

.dots { display: inline-flex; gap: 6px; }
.dots span {
  width: 8px; height: 8px; border-radius: 999px;
  background: var(--brand-600);
  box-shadow: 0 0 0 6px var(--brand-100);
  animation: pulse 1.2s infinite ease-in-out;
}
.dots span:nth-child(2) { animation-delay: .15s; }
.dots span:nth-child(3) { animation-delay: .3s; }

@keyframes pulse {
  0%, 100% { transform: scale(.9); opacity: .8; }
  50% { transform: scale(1.15); opacity: 1; }
}
</style>


