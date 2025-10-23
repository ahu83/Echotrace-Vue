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
                :stroke="(hasDetected || detecting) ? `url(#${gradId})` : 'transparent'"
                :stroke-width="stroke"
                fill="none"
                stroke-linecap="round"
                :stroke-dasharray="ringDash"
                :transform="rotate"
              />
            </svg>

            <div class="center-text">
              <div class="line2">{{ Math.round(score) }}%</div>
            </div>

            <div class="upload-wrap">
              <input
                id="audioUpload"
                type="file"
                accept="audio/*"
                @change="handleFileUpload"
                class="file-input"
              />
              <label
                for="audioUpload"
                class="upload-label"
                :class="{ done: uploaded }"
              >
                {{ uploaded ? "Uploaded" : "Choose Audio File" }}
              </label>

              <p v-if="fileName" class="file-status">
                Selected: {{ fileName }}
              </p>
            </div>

            <div class="button-wrap">
              <button
                class="detect-btn"
                :disabled="detecting || !file"
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
import api from "@/api";

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
      hasDetected: false,
      score: 0,
      file: null,
      fileName: "",
      uploaded: false,
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
      if (!this.file) return "Detect";
      return this.detecting ? "Detecting..." : "Detect";
    },
  },
  methods: {
    handleFileUpload(e) {
      const selected = e.target.files && e.target.files[0];
      if (!selected) return;
      this.file = selected;
      this.fileName = selected.name;
      this.uploaded = true;
      this.hasDetected = false;
      this.score = 0;
    },

    async toggleDetect() {
      if (this.detecting) return;
      if (!this.file) {
        alert("Please select an audio file before detection.");
        return;
      }

      this.detecting = true;
      this.hasDetected = true;
      await this.animateScoreTo(0, 200);

      try {
        const base64Audio = await this.fileToBase64(this.file);
        const token = localStorage.getItem("token");


        const res = await api.post(
          "/detect",
          { audio: base64Audio },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const targetScore = Number(res.data.score ?? 0);
        await this.animateScoreTo(targetScore, 900);
      } catch (err) {
        console.error("Detection error:", err);
        alert("Error detecting watermark. Check console for details.");
        await this.animateScoreTo(0, 200);
      } finally {
        this.detecting = false;
      }
    },

    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          const result = reader.result;
          if (typeof result === "string" && result.includes(",")) {
            resolve(result.split(",")[1]);
          } else {
            reject(new Error("Invalid file data"));
          }
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    },

    animateScoreTo(target, duration = 800) {
      return new Promise((resolve) => {
        target = Math.max(0, Math.min(100, target));
        const start = this.score;
        const delta = target - start;
        if (duration <= 0 || Math.abs(delta) < 0.1) {
          this.score = Math.round(target);
          return resolve();
        }

        const startTime = performance.now();
        const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

        const tick = (now) => {
          const t = Math.min(1, (now - startTime) / duration);
          const eased = easeOutCubic(t);
          this.score = start + delta * eased;
          if (t < 1) requestAnimationFrame(tick);
          else {
            this.score = Math.round(target);
            resolve();
          }
        };

        requestAnimationFrame(tick);
      });
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
  top: 38%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;

  .line2 {
    font: 900 80px/1 "Roboto", system-ui;
    color: #fff;
    text-align: center;
  }
}

.upload-wrap {
  text-align: center;
  margin-top: 20px;
}
.file-input {
  display: none;
}
.upload-label {
  display: inline-block;
  background: #1f1f1f;
  border: 1px solid #3a3a3a;
  color: #ddd;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}
.upload-label:hover {
  background: #3b3b3b;
}
.upload-label.done {
  border-color: #00ff99;
  color: #00ff99;
}
.file-status {
  margin-top: 8px;
  font-size: 14px;
  color: #a0a0ab;
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
</style>
