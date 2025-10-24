<template>
  <div class="page home">
    <nav-bar style="height: 100px"/>


    <div class="looper"/>

    <section class="section hero">
      <h1 class="title">
        Explore our range of watermarking solutions
      </h1>
    </section>

    <section class="section card-section" style="width: 100%; display: flex; justify-content: center;">
      <el-row :gutter="32" style="max-width: 1200px; justify-content: center; width: 100%;">
        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="card">
            <div class="thumb-container">
              <img class="thumb" :src="imgs.tts" alt="Text-To-Speech">
            </div>
            <div class="cta">
              <button class="pill" @click="$router.push('/tts')">
                Text-To-Speech <i class="el-icon-arrow-right"/>
              </button>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="card">
            <div class="thumb-container">
              <img class="thumb" :src="imgs.det" alt="Deepfake Detection">
            </div>
            <div class="cta">
              <button class="pill" @click="$router.push('/result')">
                Deepfake Detection <i class="el-icon-arrow-right"/>
              </button>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="card">
            <div class="thumb-container">
              <img class="thumb" :src="imgs.history" alt="History">
            </div>
            <div class="cta">
              <button class="pill" @click="$router.push('/AiHistory')">
                History <i class="el-icon-arrow-right"/>
              </button>
            </div>
          </div>
        </el-col>

        <el-col :xs="24" :sm="12" :md="6" :lg="6">
          <div class="card">
            <div class="thumb-container">
              <img class="thumb" :src="imgs.support" alt="Support">
            </div>
            <div class="cta">
              <button class="pill" @click="$router.push('/contactus')">
                Support <i class="el-icon-arrow-right"/>
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
import SidePanel from "@/components/SidePanel.vue";

export default {
  name: 'Home',
  components: { SidePanel, NavBar },
  data() {
    return {
      imgs: {
        tts: require('@/assets/tts.png'),
        det: require('@/assets/det.png'),
        history: require('@/assets/history.png'),
        support: require('@/assets/support.png')
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
  font-family: "Cabin", sans-serif;
  font-weight: 400;
  font-size: 50px;
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
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
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
  height: 250px;  /* Reduced the height */
  width: 100%;
  max-width: 400px;  /* Increased the width */
  margin: 0 16px;
}

.thumb-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 180px;  /* Reduced container height */
  overflow: hidden;
}

.thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
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
  font-family: "Cabin", sans-serif;
  font-weight: 600;
  font-size: 16px;
  line-height: 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: transform .15s ease, box-shadow .15s ease;

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
