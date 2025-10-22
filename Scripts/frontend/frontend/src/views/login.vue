<template>
  <div class="page login">
    <div class="looper"></div>

    <section class="form-wrap">
      <div class="form-card">
        <h2 class="title">Login to your account</h2>

        <form @submit.prevent="submit">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="Enter your email" required />

          <label>Password</label>
          <div class="password-field">
            <input
              v-model="form.password"
              :type="showPwd ? 'text' : 'password'"
              placeholder="Enter your password"
              required
            />
            <i
              :class="['el-icon-view', 'eye', { on: showPwd }]"
              @click.stop="showPwd = !showPwd"
              title="Show / Hide"
            />
          </div>

          <button type="submit" class="primary-btn" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login now' }}
          </button>

          <p v-if="error" class="error">{{ error }}</p>

          <div class="bottom-row">
            <span>Don't have an account?</span>
            <router-link class="link" to="/signup">Sign Up</router-link>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "LoginPage",
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      showPwd: false,
      loading: false,
      error: "",
    };
  },
  methods: {
    async submit() {
      this.error = "";
      this.loading = true;
      try {
        const res = await api.post("/login", {
          email: this.form.email.trim(),
          password: this.form.password.trim(),
        });

        localStorage.setItem("token", res.data.token);
        localStorage.setItem("username", res.data.username);
        this.$router.push("/home");
      } catch (err) {
        this.error = err.response?.data?.message || "Invalid credentials";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.page.login {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  color: #fff;
  overflow: hidden;
}

.looper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("@/assets/looper-bg.png") center center / cover no-repeat;
  opacity: 0.4;
  z-index: 0;
}

.form-wrap {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 100vh;
}

.form-card {
  background: #0b0b0b;
  padding: 40px;
  border-radius: 12px;
  width: 380px;
  text-align: center;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
}

.title {
  margin-bottom: 25px;
  font-size: 1.6em;
  font-weight: 600;
  color: #fafafa;
}

form {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  display: block;
  font-size: 0.9em;
  margin: 10px 0 5px;
  color: #d1d1d6;
}

input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 6px;
  border: 1px solid #333;
  background: #111;
  color: #fff;
  font-size: 0.95em;
  outline: none;
  margin-bottom: 12px;
  transition: 0.2s ease;
}

input:focus {
  border-color: #3b82f6;
}

.password-field {
  position: relative;
}

.eye {
  position: absolute;
  right: 12px;
  top: 32%;
  color: #70707b;
  cursor: pointer;
}

.eye.on {
  color: #f2f2f7;
}

.primary-btn {
  width: 100%;
  padding: 12px;
  background: #0066ff;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  margin-top: 8px;
  transition: 0.3s;
}

.primary-btn:hover {
  background: #0051cc;
}

.primary-btn:disabled {
  background: #333;
  cursor: not-allowed;
}

.error {
  color: #ef4444;
  text-align: center;
  margin-top: 10px;
  font-size: 0.9em;
}

.bottom-row {
  text-align: center;
  margin-top: 15px;
  font-size: 0.9em;
  color: #888;
}

.bottom-row .link {
  color: #60a5fa;
  text-decoration: none;
  margin-left: 5px;
}

.bottom-row .link:hover {
  text-decoration: underline;
}
</style>
