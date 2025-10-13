<template>
  <div class="page home">
    <nav-bar style="height: 100px"/>

    <div class="looper"/>

    <section class="section hero">
      <h1 class="title">
        Explore our range watermarking solutions
      </h1>
    </section>

    <section class="section card-section" style="width: 100%; display: flex; justify-content: center;">
      <el-row :gutter="32" style="max-width: 1200px; justify-content: center; width: 100%;">
        <el-col :xs="24" :sm="12" :md="8">
          <div class="card">
            <img class="thumb" :src="imgs.tts" alt="">
            <div class="cta">
              <button class="pill" @click="$router.push('/tts')">
                Text-To-Speech <i class="el-icon-arrow-right"/>
              </button>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <div class="card">
            <img class="thumb" :src="imgs.detect2" alt="">
            <div class="cta">
              <button class="pill" @click="$router.push('/result')">
                Deepfake Detection <i class="el-icon-arrow-right"/>
              </button>
            </div>
          </div>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'Home',
  components: { NavBar },
  data() {
    return {
      imgs: {
        tts: require('@/assets/tts.png'),
        detect2: require('@/assets/detect2.png')
      }
    };
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000000;
$border: rgba(255, 255, 255, .08);

.home {
  position: relative;
  background: $bg;
  color: #E6E8EB;
  overflow-x: hidden;
}

.looper {
  position: absolute;
  inset: 0;
  background: url(~@/assets/looper-bg.png) center bottom / 1400px auto no-repeat;
  background-size: 100%;
  opacity: .5;
  pointer-events: none;
  transform: rotate(0.5deg);
}

.title {
  max-width: 1303px;
  margin: 72px auto 8px;
  font-family: 'Cabin', 'Segoe UI', Arial, sans-serif;
  font-weight: 400;
  font-size: 56px;
  line-height: 78px;
  letter-spacing: .02em;
  background: linear-gradient(91.06deg, #FF1CF7 2.26%, #00F0FF 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
}

.card-section {
  padding-top: 16px;
  padding-bottom: 80px;
}

.el-row {
  display: flex !important;
  justify-content: center !important;
  flex-wrap: wrap;
  width: 100%;
}

.el-col {
  display: flex;
  justify-content: center;
}

.card {
  position: relative;
  background: $panel;
  border: 1px solid $border;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, .35);
  padding-bottom: 24px;
  height: 300px;
  width: 100%;
  max-width: 360px;
  margin: 0 16px;
}

.thumb {
  width: 260px;
  height: auto;
  margin: 30px auto;
  display: block;
}

.cta {
  display: flex;
  justify-content: center;
  padding-top: 18px;
}

.pill {
  position: relative;
  height: 48px;
  padding: 0 52px 0 18px;
  border-radius: 100px;
  background: #000;
  color: #fff;
  border: 2px solid #EA2DF8;
  font-family: 'Poppins', system-ui, Arial, sans-serif;
  font-weight: 600;
  font-size: 16px;
  line-height: 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: transform .15s ease, box-shadow .15s ease;

  &:after {
    content: '';
    position: absolute;
    right: 6px;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    border-radius: 20px;
    background: linear-gradient(270deg, #FF1CF7 0%, #EA2DF8 8.17%, #DE38F8 12.98%, #CF44F9 18.75%, #BC54F9 26.44%, #AD60FA 32.21%, #A467FA 35.58%, #8681FB 47.6%, #6D95FC 57.21%, #52ACFC 67.79%, #43B8FD 73.56%, #32C6FD 80.29%, #15DFFE 91.83%, #00F0FF 100%);
  }

  &:before {
    content: '';
    position: absolute;
    right: 2px;
    top: 50%;
    transform: translateY(-50%);
    width: 50px;
    height: 80px;
    background-repeat: no-repeat;
    background-position: center;
    background-size: 100% 100%;
    background-image: url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>\
<path fill='%23FFFFFF' d='M6 11h8V9l5 3-5 3v-2H6z'/>\
</svg>");
    pointer-events: none;
    z-index: 2;
  }

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(0, 0, 0, .35);
  }
}

@media (max-width: 1200px) {
  .title {
    font-size: 48px;
    line-height: 58px;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 36px;
    line-height: 44px;
    margin-top: 40px;
  }
}
</style>
