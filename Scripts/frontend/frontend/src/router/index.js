import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/views/home.vue'

Vue.use(VueRouter)

const TextToSpeech = () => import('@/views/TextToSpeech.vue');
const DetectionResult = () => import('@/views/DetectionResult.vue');
const SignUp = () => import('@/views/SignUp.vue');
const index = () => import('@/views/index.vue');
const login  = () => import('@/views/login.vue');
const Forgot = () => import('@/views/Forgot.vue');
const ForgotSent = () => import('@/views/ForgotSent.vue');

const routes = [
    {
        path: '/',
        name: 'index',
        component: index
    },
    {
        path: '/login',
        name: 'login',
        component: login
    },
    {
        path: '/forgot',
        name: 'forgot',
        component: Forgot
    },
    {
        path: '/forgotSent',
        name: 'forgotSent',
        component: ForgotSent
    },
    {
        path: '/home',
        name: 'home',
        component: HomeView
    },
    {
        path: '/tts',
        name: 'TextToSpeech',
        component: TextToSpeech
    },
    {
        path: '/result',
        name: 'DetectionResult',
        component: DetectionResult
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUp
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
