<template>
  <div class="page tts">
    <side-panel @signout="onSignout"/>
    <div class="looper"></div>

    <section class="panel-wrap fixed-panel">
      <div class="panel">
        <h2 class="title">Text-To-Speech</h2>
        <p class="desc">Enter your text in the box to generate</p>
        <p class="desc2">Only support .txt and PDF</p>

        <el-input
            class="area"
            type="textarea"
            :rows="8"
            v-model="text"
            placeholder="Paste text here…">
        </el-input>

        <div class="center">
          <button class="btn-generate" @click="onGenerate" :disabled="loading">
            <svg viewBox="0 0 24 24" aria-hidden="true" style="margin-left: 33%">
              <path fill="#fff" d="M8 5v14l11-7z"/>
            </svg>
            <span>Generate</span>
          </button>
        </div>

        <el-divider></el-divider>
        <hr>

        <div class="audios">
          <button class="audio-btn" v-for="(a, i) in audios" :key="i" @click="toggle(i)">
            <svg v-if="!a.playing" viewBox="0 0 24 24">
              <path fill="#fff" d="M8 5v14l11-7z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24">
              <path fill="#fff" d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
            <span>{{ a.name }}</span>
            <audio :ref="'audio'+i" :src="a.src" @ended="a.playing=false"></audio>
          </button>
        </div>

        <div class="center">
          <button class="btn-save" @click="save">
            <svg viewBox="0 0 24 24">
              <path fill="#9747FF" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
            </svg>
            <span>Save this audio</span>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import SidePanel from '@/components/SidePanel.vue';

export default {
  name: 'TextToSpeech',
  components: { SidePanel },
  data() {
    return {
      loading: false,
      text: '',
      audios: [
        { name: 'Unwatermarked', src: '/mock/audio1.mp3', playing: false },
        { name: 'Watermarked', src: '/mock/audio2.mp3', playing: false }

      ]
    };
  },
  methods: {
    onSignout() {
      this.$message('Sign out clicked');
    },
    async onGenerate() {
      this.loading = true;
      try {
        this.$message.success('Generated!');
      } finally {
        this.loading = false;
      }
    },
    toggle(i) {
      const el = this.$refs['audio' + i];
      const item = this.audios[i];
      if (!el) return;
      if (item.playing) {
        el.pause();
        item.playing = false;
      } else {
        el.play();
        item.playing = true;
      }
    },
    save() {
      this.$message.info('Hook save API');
    }
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000;
$muted: #A0A0AB;
$border: rgba(255, 255, 255, .08);

.tts {
  min-height: 100vh;
  background: $bg;
  color: #E6E8EB;
}

.panel-wrap {
  padding-left: 72px;
  transition: none !important;
}

.side.expanded + .looper + .panel-wrap {
  padding-left: 72px !important; /* stop it from shifting when sidebar expands */
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
  max-width: 771px;
  margin: 0 auto 80px;
  background: $panel;
  box-shadow: 0 4px 50px rgba(33, 33, 33, .08), 0 4px 6px rgba(33, 33, 33, .04);
  border-radius: 16px;
  border: 1px solid $border;
  padding: 24px;
  position: relative;
  top: 200px;
}

.title {
  font-family: 'Cabin', sans-serif;
  font-weight: 700;
  font-size: 32px;
  color: #fff;
  margin: 0 0 8px;
}

.desc {
  font: 400 14px/20px 'Inter', system-ui;
  margin: 0 0 12px;
}

.desc2 {
  color: $muted;
  font: 400 14px/20px 'Inter', system-ui;
  margin: 0 0 12px;
}

.area ::v-deep textarea {
  background: rgba(19, 19, 22, .8);
  border: 1px dashed #D1D1D6;
  color: #E6E8EB;
  border-radius: 8px;
}

.center {
  text-align: center;
  margin: 18px 0 8px;
}

.btn-generate {
  height: 47px;
  width: 440px;
  padding: 0 24px;
  border-radius: 12px;
  background: #9747FF;
  border: none;
  color: #fff;
  font: 500 19px/23px 'Inter', system-ui;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;

  svg {
    width: 24px;
    height: 24px;
  }

  &:disabled {
    opacity: .6;
    cursor: not-allowed;
  }
}

.audios {
  display: flex;
  justify-content: center;
  gap: 18px;
  margin: 12px 0 12px;
  padding: 5px;
}

.audio-btn {
  height: 47px;
  padding: 0 24px; /* add padding left and right */
  border-radius: 12px;
  background: #6D6D6D;
  border: none;
  color: #fff;
  font: 500 19px/23px 'Inter', system-ui;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;

  svg {
    width: 20px;
    height: 20px;
  }
}

.btn-save {
  height: 47px;
  padding: 0 24px;
  border-radius: 12px;
  background: #fff;
  border: none;
  color: #9747FF;
  font: 500 18px/22px 'Inter', system-ui;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;

  svg {
    width: 24px;
    height: 24px;
  }
}

::v-deep .el-divider {
  background-color: #fff;
  opacity: .9;
}
</style>
