<template>
  <div class="page tts">
    <side-panel />

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel fixed-panel">
        <header class="head">
          <h2 class="title">Text to Speech</h2>
        </header>

        <p class="sub">Enter text to generate AI audio</p>

        <div class="input-container">
          <textarea
            v-model="text"
            class="tts-input"
            placeholder="Type your text here..."
            rows="6"
          ></textarea>
        </div>

        <div class="button-wrap">
          <button
            class="detect-btn"
            :disabled="loading"
            @click="onGenerate"
          >
            {{ loading ? "Generating..." : "Generate Audio" }}
          </button>
        </div>

        <div v-if="audiosVisible" class="audio-section">
          <div
            v-for="(audio, i) in audios"
            :key="i"
            class="audio-card"
          >
            <h3>{{ audio.name }}</h3>
            <audio
              :ref="'audio' + i"
              :src="audio.src"
              controls
              preload="none"
            ></audio>

            <div class="button-wrap">
              <!-- ✅ Only Download button remains -->
              <button
                class="detect-btn"
                @click="download(i)"
              >
                Download
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import SidePanel from "@/components/SidePanel.vue";

export default {
  name: "TextToSpeech",
  components: { SidePanel },
  data() {
    return {
      loading: false,
      text: "",
      audiosVisible: false,
      audios: [
        { name: "Unwatermarked", src: "", playing: false },
        { name: "Watermarked", src: "", playing: false }
      ]
    };
  },
  methods: {
    async onGenerate() {
      if (!this.text.trim()) {
        alert("Please enter some text first!");
        return;
      }

      this.loading = true;

      try {
        const token = localStorage.getItem("token");
        const res = await axios.post(
          "http://127.0.0.1:5000/generate",
          { text: this.text },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const toBlob = (b64) =>
          URL.createObjectURL(
            new Blob([Uint8Array.from(atob(b64), (c) => c.charCodeAt(0))], {
              type: "audio/wav",
            })
          );

        this.audios = [
          { name: "Unwatermarked", src: toBlob(res.data.unwatermarked), playing: false },
          { name: "Watermarked", src: toBlob(res.data.watermarked), playing: false },
        ];

        this.audiosVisible = true;
      } catch (err) {
        console.error("Error generating audio:", err);
        alert("Error generating audio. Check console for details.");
      } finally {
        this.loading = false;
      }
    },

    // ✅ Only download logic remains
    download(i) {
      const item = this.audios[i];
      if (!item?.src) return;
      const a = document.createElement("a");
      a.href = item.src;
      a.download = `${item.name.replace(/\s+/g, "_")}.wav`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
  },
};
</script>

<style scoped lang="scss">
$bg: #0a0a0a;
$border: rgba(255, 255, 255, 0.08);
$text: #e6e8eb;

.tts {
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
  padding: 40px 48px 48px;
  top: 160px;
  box-sizing: border-box;
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
  margin: 0 0 18px;
  font: 500 18px/1.6 "Cabin", sans-serif;
  color: #fff;
  opacity: 0.95;
}

.input-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.tts-input {
  width: 100%;
  background: #111;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 14px;
  color: #fff;
  font-size: 1em;
  resize: none;
  outline: none;
  margin: 0 auto 20px;
  transition: 0.2s;
  box-sizing: border-box;
}

.tts-input:focus {
  border-color: #a855f7;
}

.button-wrap {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 20px;
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
  margin: 6px;

  &:hover {
    opacity: 0.9;
    transform: scale(1.05);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.audio-section {
  display: flex;
  justify-content: space-evenly;
  margin-top: 40px;
}

.audio-card {
  background: #111;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 20px;
  width: 45%;
  text-align: center;

  h3 {
    color: #fff;
    margin-bottom: 10px;
  }

  audio {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
