<template>
  <div class="page detect">
    <side-panel />

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel fixed-panel">
        <header class="head">
          <h2 class="title">AI Detection</h2>
        </header>

        <p class="sub">Likelihood of being AI generated</p>

        <div class="chart-row">
          <div class="donut">
            <svg
              :width="size"
              :height="size"
              :viewBox="`0 0 ${size} ${size}`"
              role="img"
              aria-label="AI detection progress"
            >
              <defs>
                <linearGradient :id="gradId" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#A855F7" />
                  <stop offset="100%" stop-color="#3B82F6" />
                </linearGradient>
              </defs>

              <circle
                :cx="center"
                :cy="center"
                :r="radius"
                :stroke="`url(#${gradId})`"
                :stroke-width="stroke"
                fill="none"
                stroke-linecap="butt"
                :stroke-dasharray="ringDash"
                :transform="rotate"
              />
            </svg>

            <div class="center-text">
              <div v-if="detecting" class="line2 recording">●</div>
              <div v-else class="line2">{{ score }}%</div>
            </div>

            <div class="button-wrap">
              <button
                class="detect-btn"
                :disabled="detecting"
                @click="toggleDetect"
              >
                {{ buttonText }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import SidePanel from "@/components/SidePanel.vue";

export default {
  name: "DetectionResult",
  components: { SidePanel },
  data() {
    const size = 466;
    const stroke = 48;
    const center = size / 2;
    const radius = (size - stroke) / 2;
    const circum = 2 * Math.PI * radius;
    return {
      size,
      stroke,
      center,
      radius,
      circum,
      gradId: "grad-donut-" + Math.random().toString(36).slice(2, 8),
      rotate: `rotate(-90 ${center} ${center})`,
      detecting: false,
      score: 0,
      mediaRecorder: null,
      audioChunks: [],
    };
  },
  computed: {
    ringDash() {
      const gap = this.circum * 0.06;
      const effective = this.circum - gap;
      const show = Math.max(0, Math.min(1, this.score / 100)) * effective;
      const hide = this.circum - show;
      return `${show} ${hide}`;
    },
    buttonText() {
      return this.detecting ? "Recording..." : "Detect";
    },
  },
  methods: {
    async toggleDetect() {
      if (this.detecting) return;
      this.detecting = true;
      this.score = 0;

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(stream);

        this.mediaRecorder.ondataavailable = (e) => this.audioChunks.push(e.data);
        this.mediaRecorder.start();
        console.log("Recording started...");

        await new Promise((resolve) => setTimeout(resolve, 5000));
        this.mediaRecorder.stop();
        console.log("Recording stopped.");

        const audioBlob = await new Promise((resolve) => {
          this.mediaRecorder.onstop = () => {
            const blob = new Blob(this.audioChunks, { type: "audio/wav" });
            resolve(blob);
          };
        });

        const base64Audio = await this.blobToBase64(audioBlob);

        console.log("Sending audio to Flask...");
        const response = await fetch("http://127.0.0.1:5000/detect", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ audio: base64Audio }),
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();
        const targetScore = data.score ?? 0;
        console.log("Detection score:", targetScore);

        this.animateScore(targetScore);
      } catch (err) {
        console.error("Detection error:", err);
        this.score = 0;
      } finally {
        this.detecting = false;
      }
    },

    blobToBase64(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(",")[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    },

    animateScore(target) {
      const step = (target - this.score) / 30;
      const interval = setInterval(() => {
        this.score += step;
        if (
          (step > 0 && this.score >= target) ||
          (step < 0 && this.score <= target)
        ) {
          this.score = Math.round(target);
          clearInterval(interval);
        }
      }, 30);
    },
  },
};
</script>

<style lang="scss" scoped>
$bg: #0a0a0a;
$border: rgba(255, 255, 255, 0.08);
$text: #e6e8eb;

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
  opacity: 0.5;
  transform: rotate(15deg);
  pointer-events: none;
}

.panel {
  max-width: 1077px;
  margin: 0 auto 80px;
  background: #000;
  border: 1px solid $border;
  border-radius: 16px;
  box-shadow: 0 4px 50px rgba(33, 33, 33, 0.08),
    0 4px 6px rgba(33, 33, 33, 0.04);
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
  font: 800 36px/1.2 "Cabin", "Segoe UI", Arial, sans-serif;
  color: #fff;
}

.sub {
  margin: 0 0 14px;
  font: 500 18px/1.6 "Cabin", sans-serif;
  color: #fff;
  opacity: 0.95;
}

.chart-row {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 457px;
}

.donut {
  position: relative;
  width: 466px;
  height: 466px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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
    font: 900 90px/1 "Roboto", system-ui;
    color: #fff;
    text-align: center;
  }

  .recording {
    font-size: 120px;
    color: #ff4d4d;
    animation: pulse 1s infinite alternate;
  }
}

@keyframes pulse {
  from {
    opacity: 0.2;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1.1);
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
  background-color: #a855f7;
  color: #fff;
  font: 700 18px/1 "Roboto", sans-serif;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;

  &:hover {
    opacity: 0.9;
    transform: scale(1.05);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

html,
body {
  margin: 0;
}
</style>
