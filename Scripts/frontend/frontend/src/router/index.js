import Vue from 'vue'
import VueRouter from 'vue-router'
import { isTokenValid } from '@/utils/auth'

import Home from '@/views/home.vue'
import Login from '@/views/login.vue'
import SignUp from '@/views/SignUp.vue'
import Forgot from '@/views/Forgot.vue'
import ForgotSent from '@/views/ForgotSent.vue'
import TextToSpeech from '@/views/TextToSpeech.vue'
import DetectionResult from '@/views/DetectionResult.vue'
import AiHistory from '@/views/AiHistory.vue'
import Index from '@/views/index.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: Index },
  { path: '/login', component: Login },
  { path: '/signup', component: SignUp },
  { path: '/forgot', component: Forgot },
  { path: '/forgotSent', component: ForgotSent },
  { path: '/tts', component: TextToSpeech, meta: { requiresAuth: true } },
  { path: '/result', component: DetectionResult, meta: { requiresAuth: true } },
  { path: '/home', component: Home, meta: { requiresAuth: true } },
  { path: '/AiHistory', component: AiHistory, meta: { requiresAuth: true } }
]

const router = new VueRouter({ mode: 'history', routes })

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(r => r.meta.requiresAuth)) {
    const valid = await isTokenValid()
    if (!valid) next('/login')
    else next()
  } else next()
})

export default router