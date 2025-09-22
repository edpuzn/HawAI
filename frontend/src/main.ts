import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './styles/theme.css'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Chat from './views/Chat.vue'
import AboutView from './views/AboutView.vue'
import DevelopersView from './views/DevelopersView.vue'

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/chat', component: Chat },
  { path: '/about', component: AboutView },
  { path: '/developers', component: DevelopersView }
]

const router = createRouter({ history: createWebHistory(), routes })

createApp(App).use(store).use(router).mount('#app')
