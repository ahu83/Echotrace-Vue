<template>
  <div class="page forgot">
    <div class="looper"></div>

    <section class="wrap">
      <div class="card">
        <h1 class="title">Forgot Password?</h1>

        <el-form ref="form" :model="form" class="el-reset" @submit.native.prevent>
          <div class="input-like">
            <el-input
                v-model="form.email"
                placeholder="Enter Your Email"
                clearable
                @keyup.enter.native="send"
            />
          </div>

          <el-button
              class="primary"
              type="primary"
              :loading="loading"
              @click="send"
          >
            Send Verification Code
          </el-button>
        </el-form>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Forgot',
  data() {
    return {
      loading: false,
      form: { email: '' }
    };
  },
  methods: {
    async send() {
      const email = this.form.email.trim();
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      if (!ok) {
        this.$message && this.$message.warning
            ? this.$message.warning('Please enter a valid email')
            : console.warn('Please enter a valid email');
        return;
      }

      this.loading = true;
      try {
        // await http.post('/auth/forgot/send-code', { email })
        this.$message && this.$message.success
            ? this.$message.success('Verification code sent')
            : console.log('Verification code sent');
        this.$router.push("/forgotSent")
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$text: #E6E8EB;

.forgot {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
  overflow: hidden;
}

.looper {
  position: fixed;
  left: -361px; top: -659px;
  width: 2259.73px; height: 1396.15px;
  background: url(~@/assets/looper-bg.png) center / cover no-repeat;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
}

.wrap { display: grid; place-items: center; min-height: 100vh; padding: 24px; }
.card {
  width: 426px; height: 530px;
  background: #000;
  border-radius: 20px;
  box-shadow: 40px 40px 60px #1E1F21;
  padding: 48px 72px;
  display: flex; flex-direction: column; justify-content: center;
}

.title {
  margin: 0 0 24px;
  font: 700 28px/1 'Poppins', system-ui;
  color: #FAFAFA;
}

.el-reset { display: flex; flex-direction: column; gap: 24px; }

.input-like {
  border: 3px solid #FFFFFF;
  border-radius: 8px;
  overflow: hidden;
  ::v-deep .el-input__inner {
    height: 42px; line-height: 42px;
    background: transparent; border: none; color: #E6E8EB;
    padding: 0 16px;
  }
}

.primary {
  height: 52px; width: 100%;
  border-radius: 8px;
  background: #1570EF; border: none;
  font: 600 16px/1 'Poppins', system-ui; color: #FCFCFC;
}
@media (max-width: 720px) {
  .card { width: 100%; height: auto; padding: 32px 20px; }
}
</style>
