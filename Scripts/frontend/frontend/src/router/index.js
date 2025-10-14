import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/views/home.vue'

Vue.use(VueRouter)

const TextToSpeech = () => import('@/views/TextToSpeech.vue');
const DetectionResult = () => import('@/views/DetectionResult.vue');

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
	{
	  path: '/tts',
	  name: 'TextToSpeech',
	  component: () => import('@/views/TextToSpeech.vue')
	},
    {
        path: '/result',
        name: 'DetectionResult',
        component: DetectionResult
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
