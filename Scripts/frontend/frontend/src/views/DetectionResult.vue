<template>
  <div class="page detect">
    <side-panel/>

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel fixed-panel">
        <header class="head">
          <h2 class="title">AI Detection</h2>
        </header>

        <p class="sub">Likelihood of being AI generated</p>

        <div class="chart-row">
          <div class="donut">
            <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" role="img"
                 aria-label="AI detection progress">
              <defs>
                <linearGradient :id="gradId" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%"  stop-color="#A855F7"/>
                  <stop offset="100%" stop-color="#3B82F6"/>
                </linearGradient>
              </defs>

              <circle
                  :cx="center" :cy="center" :r="radius"
                  :stroke="`url(#${gradId})`"
                  :stroke-width="stroke"
                  fill="none"
                  stroke-linecap="butt"
                  :stroke-dasharray="ringDash"
                  :stroke-dashoffset="dashOffset"
                  :transform="rotate"
              />


            </svg>

            <div class="center-text">
              <div class="line2">{{ score }}%</div>
            </div>
            <div class="button-wrap">
              <button class="detect-btn" @click="toggleDetect">{{ buttonText }}</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import SidePanel from '@/components/SidePanel.vue';

export default {
  name: 'DetectionResult',
  components: {SidePanel},
  props: {
    score: {type: Number, default: 0}
  },
  data() {
    const size = 466;
    const stroke = 48;
    const center = size / 2;
    const radius = (size - stroke) / 2;
    const circum = 2 * Math.PI * radius;
    return {
      size, stroke, center, radius, circum,
      gradId: 'grad-donut-' + Math.random().toString(36).slice(2, 8),
      bgId: 'grad-bg-' + Math.random().toString(36).slice(2, 8),
      rotate: `rotate(-90 ${center} ${center})`,
      gapRatio: 0.06,
      detecting: false,
      intervalId: null
    };
  },
  computed: {
    dashProgress() {
      const gap = this.circum * this.gapRatio;
      const effective = this.circum - gap;
      const show = Math.max(0, Math.min(1, this.score / 100)) * effective;
      const hide = this.circum - show;
      return `${show} ${hide}`;
    },
    gapDash() {
      const gap = this.circum * this.gapRatio;
      return `${gap} ${this.circum}`;
    },
    buttonText() {
      return this.detecting ? 'Detecting...' : 'Detect';
    },
    ringDash() {
      return this.dashProgress;
    },
    dashOffset() {
      return 0;
    }
  },
  methods: {
    async toggleDetect() {
      if (this.detecting) return;
      this.detecting = true;
      this.score = 0;

      await fetch("http://127.0.0.1:5000/start", { method: "POST" });

      let displayed = 0;
      this.intervalId = setInterval(async () => {
        const res = await fetch("http://127.0.0.1:5000/progress");
        const data = await res.json();
        const target = data.value;

        // ease toward the real value
        displayed += (target - displayed) * 0.2;
        this.score = Math.min(100, Math.round(displayed));

        if (target >= 100 && Math.abs(displayed - target) < 0.5) {
          clearInterval(this.intervalId);
          this.detecting = false;
          this.score = 100;
        }
      }, 30); // refresh ~33 fps
    }
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000;
$border: rgba(255, 255, 255, .08);
$text: #E6E8EB;

.detect {
  min-height: 100vh;
  background: $bg;
  color: $text;
}

.panel-wrap {
  padding-left: 72px;
}

.fixed-panel {
  position: relative !important;
  left: 0 !important;
}

.looper {
  position: fixed;
  inset: 0 0 0 72px;
  background: url(~@/assets/looper-bg.png) center / 1600px auto no-repeat;
  background-size: 100%;
  background-position: 0px -300px;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
}

.panel {
  max-width: 1077px;
  margin: 0 auto 80px;
  background: #000;
  border: 1px solid $border;
  border-radius: 16px;
  box-shadow: 0 4px 50px rgba(33, 33, 33, .08), 0 4px 6px rgba(33, 33, 33, .04);
  padding: 24px 24px 32px;
  top: 160px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title {
  margin: 0 0 8px 0;
  font: 800 36px/1.2 'Cabin', 'Segoe UI', Arial, sans-serif;
  color: #fff;
}

.sub {
  margin: 0 0 14px;
  font: 500 18px/1.6 'Cabin', sans-serif;
  color: #fff;
  opacity: .95;
}

.chart-row {
  display: flex;
  justify-content: center; 
  align-items: center;      
  min-height: 457px;
}

.donut {
  position: relative;
  align-items: center;
  width: 466px;
  height: 466px;
  margin: 4px 0 4px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.center-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -75%);
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;

  .line2 {
    font: 900 90px/1 'Roboto', system-ui;
    color: #fff;
    text-align: center;
  }
}

.button-wrap {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 30px;
}

.detect-btn {
  padding: 12px 28px;
  border: none;
  border-radius: 10px;
  background-color: #A855F7;
  color: #fff;
  font: 700 18px/1 'Roboto', sans-serif;
  cursor: pointer;
  transition: transform .2s, opacity .2s;

  &:hover {
    opacity: 0.9;
    transform: scale(1.05);
  }
}

html, body {
  margin: 0;
}
</style>
