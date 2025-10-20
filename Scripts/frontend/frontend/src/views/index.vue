<template>
  <div class="page index">
    <nav-bar :logo="logo" style="height: 100px"/>

    <div class="bg">
      <div class="looper looper-top"></div>
      <div class="looper looper-bottom"></div>
      <div class="glow glow-pink"></div>
      <div class="glow glow-blue"></div>
      <div class="glow glow-violet"></div>
    </div>

    <section class="hero">
      <h1 class="hero-title">Uncover Deepfakes Instantly</h1>
      <p class="hero-desc">
        Echo-Trace Technology ensures audio authenticity with invisible watermarks,
        enabling reliable deepfake speech detection to protect communications against
        AI-driven misinformation in an accessible, user-friendly platform.
      </p>

      <div class="cta">
        <button class="cta-pill" @click="$router.push('/signup')">
          <span class="cta-text">Get Started</span>
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'Index',
  components: { NavBar },
  data() {
    return {
      logo: require('@/assets/logo.png')
    };
  }
};
</script>

<style lang="scss" scoped>
$bg: #000;
$text: #E6E8EB;

.index {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
  overflow-x: hidden;
}

.bg { position: absolute; inset: 0; pointer-events: none; }

.looper {
  position: absolute;
  background: url(~@/assets/looper-bg.png) center / cover no-repeat;
  opacity: .5;
  transform: rotate(15deg);
}
.looper-top { width: 2284.64px; height: 1326.07px; left: -361px; top: -591px; }
.looper-bottom { width: 2259.73px; height: 1396.15px; left: -361px; top: 691px; }

.glow {
  position: absolute; filter: blur(100px); opacity: .2; border-radius: 50%;
}
.glow-pink { width: 494px; height: 494px; left: 1018px; top: 783px; background:#FC4FF6; }
.glow-blue { width: 494px; height: 494px; left: 35px;   top: 772px; background:#899AFF; }
.glow-violet{ width: 426px; height: 426px; left: 608px;  top: 626px; background:#485DFF; filter: blur(125px); }

.hero {
  position: relative;
  max-width: 1120px;
  margin: 140px auto 120px;
  padding: 0 24px;
  text-align: center;
}

.hero-title {
  margin: 0;
  font-family: 'Abyssinica SIL','Cabin','Times New Roman',serif;
  font-weight: 400;
  font-size: 64px;
  line-height: 85px;
  letter-spacing: .02em;
  background: linear-gradient(91.06deg, #FF1CF7 2.26%, #00F0FF 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-desc {
  max-width: 836px;
  margin: 18px auto 40px;
  font-family: 'Actor','Segoe UI',Arial,sans-serif;
  font-size: 20px;
  line-height: 33px;
  letter-spacing: .72px;
  color: #fff;
  opacity: .92;
}

.cta { display: flex; justify-content: center; }
.cta-pill {
  position: relative;
  width: 442px; height: 70px;
  padding: 0 72px 0 72px;
  border-radius: 100px;
  border: 1.5px solid transparent;
  background-image:
      linear-gradient(#000, #000),
      linear-gradient(91.06deg, #FF1CF7 2.26%, #00F0FF 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;

  display: inline-flex; align-items: center; justify-content: center;
  cursor: pointer; color: #fff;
  box-shadow: 0 10px 24px rgba(0,0,0,.35);
  transition: transform .15s ease, box-shadow .15s ease;

  &:after{
    content: '';
    position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
    width: 40px; height: 40px; border-radius: 20px;
    background: linear-gradient(270deg, #FF1CF7 0%, #EA2DF8 8.17%, #DE38F8 12.98%, #CF44F9 18.75%,
        #BC54F9 26.44%, #AD60FA 32.21%, #A467FA 35.58%, #8681FB 47.6%, #6D95FC 57.21%,
        #52ACFC 67.79%, #43B8FD 73.56%, #32C6FD 80.29%, #15DFFE 91.83%, #00F0FF 100%);
    box-shadow: 0 0 0 2px #FFFFFF;
    z-index: 1;
  }
  &:before {
    content: '';
    position: absolute;
    right: 6px;
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
  &:hover{ transform: translateY(-2px); box-shadow: 0 14px 30px rgba(0,0,0,.45); }
}
.cta-text{
  font-family: 'Space Grotesk',system-ui,Arial,sans-serif;
  font-weight: 700; font-size: 20px; line-height: 26px;
}

@media (max-width: 1200px){
  .hero { margin-top: 120px; }
  .hero-title{ font-size: 52px; line-height: 68px; }
}
@media (max-width: 768px){
  .hero-title{ font-size: 40px; line-height: 52px; }
  .hero-desc{ font-size: 18px; line-height: 28px; }
  .cta-pill{ width: 100%; max-width: 420px; height: 60px; }
}
</style>
