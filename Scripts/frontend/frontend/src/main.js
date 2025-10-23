import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// ---- Element UI (EN locale) ----
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI, { locale })

// ---- Global styles ----
import '@/utils/flexible'
import '@/Scss/theme.scss'
import './CSS/base.css'

// ---- Axios ----
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)

// ---- Watermark plugin ----
import VueWatermark from 'vue-watermark'
Vue.component('VueWatermark', VueWatermark)

// ---- Image Viewer ----
import Viewer from 'v-viewer'
import 'viewerjs/dist/viewer.css'
Vue.use(Viewer)
Viewer.setDefaults({
  Options: {
    inline: true,
    button: true,
    navbar: true,
    title: true,
    toolbar: true,
    tooltip: true,
    fullscreen: true,
    loading: true,
    loop: true,
    movable: true,
    zoomable: true,
    rotatable: true,
    scalable: true,
    toggleOnDblclick: true,
    transition: true,
    keyboard: true,
    zoomRatio: 0.4,
    minZoomRatio: 0.01,
    maxZoomRatio: 100,
    url: 'data-source'
  }
})

// ---- Progress bar (NProgress) ----
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({
  easing: 'ease',
  speed: 500,
  showSpinner: false,
  trickleSpeed: 200,
  minimum: 0.3
})

router.beforeEach((to, from, next) => {
  NProgress.start()
  NProgress.inc()
  next()
})

router.afterEach(() => {
  NProgress.done()
})

// ---- Vue config ----
Vue.config.productionTip = false

// ---- App mount ----
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
