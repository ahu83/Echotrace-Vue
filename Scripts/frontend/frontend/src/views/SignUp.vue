<template>
  <div class="page signup">
    <div class="looper looper-top"></div>
    <div class="looper looper-bottom"></div>

    <section class="form-wrap">
      <div class="form-card">
        <h1 class="title">Create an account</h1>

        <div class="social-row">
          <button class="social-btn">
            <svg viewBox="0 0 24 24" class="ico"><path fill="#EA4335" d="M12 10.2v3.6h5.1c-.2 1.2-1.5 3.5-5.1 3.5-3.1 0-5.7-2.6-5.7-5.8S8 5.7 11.1 5.7c1.8 0 3 .8 3.7 1.5l2.5-2.4C16 3.4 14.2 2.6 11.1 2.6 6.4 2.6 2.6 6.4 2.6 11.1S6.4 19.6 11.1 19.6c6.4 0 8.8-4.5 8.1-9.4H12z"/></svg>
            <span>Google</span>
          </button>
          <button class="social-btn">
            <svg viewBox="0 0 24 24" class="ico"><path fill="#1877F2" d="M22 12a10 10 0 1 0-11.6 9.9v-7h-2.3V12h2.3V9.8c0-2.3 1.4-3.6 3.5-3.6 1 0 2 .2 2 .2v2.2h-1.1c-1.1 0-1.5.7-1.5 1.4V12h2.6l-.4 2.9h-2.2v7A10 10 0 0 0 22 12"/></svg>
            <span>facebook</span>
          </button>
        </div>

        <div class="divider">
          <span class="line"></span>
          <span class="or">Or</span>
          <span class="line"></span>
        </div>

        <el-form :model="form" ref="f" class="el-reset" @submit.native.prevent>
          <label class="label">Email</label>
          <div class="input-like">
            <el-input v-model="form.email" placeholder="" clearable></el-input>
          </div>

          <label class="label">Password</label>
          <div class="input-like">
            <el-input v-model="form.password" placeholder="" show-password></el-input>
          </div>

          <el-button class="primary" type="primary" @click="submit" :loading="loading">
            Sign up now
          </el-button>
        </el-form>

        <div class="bottom-row">
          <span>Already Have An Account ?</span>
          <router-link class="login-link" to="/login">Log In</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'SignUp',
  data() {
    return {
      loading: false,
      form: { email: '', password: '' }
    };
  },
  methods: {
    async submit() {
      if (!this.form.email || !this.form.password) {
        this.$message.warning('Please fill email & password');
        return;
      }
      this.loading = true;
      try {
        // await http.post('/auth/signup', this.form)
        this.$message.success('Signed up!');
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
$muted: #70707B;

.signup {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
  overflow: hidden;
}

.looper {
  position: fixed;
  left: -361px;
  width: 2284.64px;
  height: 1326.07px;
  background: url(~@/assets/looper-bg.png) center / cover no-repeat;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
}
.looper-top { top: -591px; }
.looper-bottom {
  top: 691px;
  width: 2259.73px; height: 1396.15px;
}

.form-wrap { display:grid; place-items:center; min-height:100vh; padding:24px; }
.form-card {
  width: 426px;
  background: #000;
  border-radius: 20px;
  padding: 48px 72px;
  box-shadow: 20px 40px 60px rgba(0,0,0,.5);
  position: relative;
}
.title {
  margin: 0 0 24px;
  font: 600 28px/1 'Poppins', system-ui;
  color: #FAFAFA;
  text-align: center;
}

.social-row { display:flex; gap:16px; justify-content:center; margin-bottom: 24px; }
.social-btn {
  height: 48px; width: 233px;
  display:flex; align-items:center; justify-content:center; gap:8px;
  background:#26272B; color:#A0A0AB; border:none; border-radius:8px; cursor:pointer;
}
.ico { width:20px; height:20px; }

.divider { display:flex; align-items:center; gap:12px; margin: 10px 0 14px; }
.line { flex:1; height:1px; background:#fff; opacity:.9; }
.or { font: 600 20px/1 'Poppins', system-ui; color:#70707B; }

.el-reset {
  display:flex; flex-direction:column; gap:24px; margin-top: 8px;
}
.label {
  font: 400 16px/1 'Poppins', system-ui; color:#D1D1D6; margin-bottom: 8px;
}
.input-like {
  border: 3px solid #EBEDF0; border-radius: 8px; overflow: hidden;
  ::v-deep .el-input__inner {
    height: 42px; line-height:42px; border:none; background:transparent; color:#E6E8EB;
  }
}

.primary {
  height: 48px; border-radius: 8px; background:#1570EF; border:none;
  width: 100%; font: 600 16px/1 'Poppins', system-ui;
}

.bottom-row {
  margin-top: 24px; display:flex; justify-content:center; gap:8px;
  span { color: $muted; font: 400 16px/1 'Poppins', system-ui; }
  .login-link { color:#A0A0AB; font: 400 16px/1 'Poppins', system-ui; }
}

@media (max-width: 720px) {
  .form-card { width:100%; padding:32px 20px; }
  .social-row { flex-direction:column; }
  .social-btn { width:100%; }
}
</style>
