<template>
  <div class="signup-page">
    <!-- Static looper background -->
    <div class="looper"></div>

    <!-- Sign-up form -->
    <div class="signup-card">
      <h2>Create an account</h2>

      <form @submit.prevent="registerUser">
        <label>Email</label>
        <input v-model="email" type="email" required />
        <label>Password</label>
        <input v-model="password" type="password" required />
        <label>Confirm Password</label>
        <input v-model="confirmPassword" type="password" required />

        <button type="submit" class="primary-btn">Sign up now</button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>

      <p class="login-text">
        Already Have An Account? <router-link to="/login">Log In</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "SignUp",
  data() {
    return {
      email: "",
      password: "",
      confirmPassword: "",
      error: "",
      success: "",
    };
  },
  methods: {
    async registerUser() {
      this.error = "";
      this.success = "";

      if (!this.email || !this.password || !this.confirmPassword) {
        this.error = "Please fill out all fields.";
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.error = "Passwords do not match.";
        return;
      }

      try {
        const res = await api.post("/register", {
          username: this.email.split("@")[0],
          email: this.email.trim(),
          password: this.password.trim(),
        });

        this.success = res.data.message || "Account created successfully!";
        alert("Registration successful! Please log in.");
        this.$router.push("/login");
      } catch (err) {
        this.error =
          err.response?.data?.message || "An error occurred during registration.";
      }
    },
  },
};
</script>

<style scoped>
.signup-page {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  overflow: hidden;
}

/* 🟣 Static looper image background */
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

.signup-card {
  position: relative;
  z-index: 1;
  background: #0b0b0b;
  padding: 40px;
  border-radius: 12px;
  width: 380px;
  text-align: center;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
  color: #fff;
}

.signup-card h2 {
  margin-bottom: 20px;
  font-weight: 600;
}

.social-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 15px;
}

.social-btn {
  flex: 1;
  background: #1a1a1a;
  border: 1px solid #333;
  color: #ccc;
  padding: 8px 0;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.social-btn:hover {
  background: #222;
}

.social-btn.google {
  color: #db4437;
}

.social-btn.facebook {
  color: #1877f2;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #666;
  margin: 20px 0;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #333;
}

.divider span {
  padding: 0 10px;
}

form {
  text-align: left;
}

label {
  display: block;
  font-size: 0.9em;
  margin: 8px 0 2px;
}

input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #333;
  background: #111;
  color: #fff;
  margin-bottom: 10px;
}

.primary-btn {
  width: 100%;
  padding: 12px;
  background: #0066ff;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  transition: 0.3s;
}

.primary-btn:hover {
  background: #0051cc;
}

.error {
  color: #ef4444;
  margin-top: 10px;
  text-align: center;
}

.success {
  color: #10b981;
  margin-top: 10px;
  text-align: center;
}

.login-text {
  margin-top: 15px;
  font-size: 0.9em;
  color: #888;
}

.login-text a {
  color: #60a5fa;
  text-decoration: none;
}

.login-text a:hover {
  text-decoration: underline;
}
</style>
