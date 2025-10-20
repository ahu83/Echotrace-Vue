<template>
  <div class="page login">
    <div class="looper"></div>

    <section class="form-wrap">
      <div class="form-card">
        <h1 class="title">Login to your account</h1>

        <el-form ref="f" :model="form" class="el-reset" @submit.native.prevent>
          <div class="field">
            <label class="label">Email</label>
            <div class="input-like">
              <el-input v-model="form.email" placeholder="balamia@gmail.com" clearable />
            </div>
          </div>

          <div class="field">
            <div class="label-row">
              <label class="label">Password</label>
              <router-link class="forgot" to="/forgot">Forgot ?</router-link>
            </div>
            <div class="input-like">
              <el-input
                  :type="showPwd ? 'text' : 'password'"
                  v-model="form.password"
                  placeholder="Enter your password"
                  @keyup.enter.native="submit"
              >
                <i
                    slot="suffix"
                    :class="['el-icon-view','eye', { on: showPwd }]"
                    @click.stop="showPwd = !showPwd"
                    title="Show / Hide"
                    style="position: relative;top: 25%;"
                />
              </el-input>
            </div>
          </div>

          <el-button class="primary" type="primary" @click="submit" :loading="loading">
            Login now
          </el-button>

          <div class="bottom-row">
            <span>Don't Have An Account?</span>
            <router-link class="link" to="/signup">Sign Up</router-link>
          </div>
        </el-form>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loading: false,
      showPwd: false,
      form: { email: '', password: '' }
    };
  },
  methods: {
    async submit() {
      if (!this.form.email || !this.form.password) {
        this.$message && this.$message.warning
            ? this.$message.warning('Please fill email & password')
            : console.warn('Please fill email & password');
        return;
      }
      this.loading = true;
      try {
        // await http.post('/auth/login', this.form)
        this.$message && this.$message.success
            ? this.$message.success('Logged in!')
            : console.log('Logged in!');
        this.$router.push('/home');
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

.login {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
  overflow: hidden;
}

.looper {
  position: fixed;
  inset: 0;
  left: -361px; top: -659px;
  width: 2259.73px; height: 1396.15px;
  background: url(~@/assets/looper-bg.png) center / cover no-repeat;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
}

.form-wrap { display: grid; place-items: center; min-height: 100vh; padding: 24px; }
.form-card {
  width: 426px;
  background: #000;
  border-radius: 20px;
  box-shadow: 40px 40px 60px #1E1F21;
  padding: 48px 72px;
}

.title {
  margin: 0 0 24px;
  font: 600 28px/1 'Poppins', system-ui;
  color: #FAFAFA;
}

.el-reset { display: flex; flex-direction: column; gap: 24px; }
.field { display: flex; flex-direction: column; gap: 12px; }
.label { font: 400 16px/1 'Poppins', system-ui; color: #D1D1D6; }
.label-row { display: flex; align-items: center; justify-content: space-between; }
.forgot { color: #A0A0AB; font: 400 16px/1 'Poppins', system-ui; }

.input-like {
  border: 3px solid #EBEDF0;
  border-radius: 8px;
  overflow: hidden;
  ::v-deep .el-input__inner {
    height: 42px; line-height: 42px;
    background: transparent; border: none; color: #F2F2F7;
    padding: 0 36px 0 16px;
  }
  ::v-deep .el-input__suffix { right: 10px; }
  .eye { color: #70707B; cursor: pointer; }
  .eye.on { color: #F2F2F7; }
}

.primary {
  height: 52px; width: 100%;
  border-radius: 8px;
  background: #1570EF; border: none;
  font: 600 16px/1 'Poppins', system-ui; color: #FCFCFC;
}

.bottom-row {
  display: flex; justify-content: center; gap: 8px; margin-top: 4px;
  span { color: #70707B; font: 400 16px/1 'Poppins', system-ui; }
  .link { color: #A0A0AB; font: 400 16px/1 'Poppins', system-ui; }
}

@media (max-width: 720px) {
  .form-card { width: 100%; padding: 32px 20px; }
}
</style>
