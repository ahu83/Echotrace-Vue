<template>
  <div class="page forgot-sent">
    <div class="looper"></div>

    <section class="wrap">
      <div class="card">
        <h1 class="title">Email Sent</h1>
        <p class="desc">Please follow the link in your email to reset the password</p>

        <el-button class="primary" type="primary" @click="$router.push('/login')">
          Back to Login
        </el-button>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ForgotSent'
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$text: #E6E8EB;

.forgot-sent {
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
  gap: 24px;
}

.title {
  margin: 0;
  font: 600 48px/1 'Poppins', system-ui;
  color: #fff;
}
.desc {
  margin: 8px 0 28px;
  font: 600 20px/1.3 'Poppins', system-ui;
  color: #fff;
  max-width: 480px;
}

.primary {
  height: 52px; width: 100%;
  border-radius: 8px;
  background: #1570EF; border: none;
  font: 600 16px/1 'Poppins', system-ui; color: #FCFCFD;
}

@media (max-width: 720px) {
  .card { width: 100%; height: auto; padding: 32px 20px; }
  .title { font-size: 36px; }
  .desc  { font-size: 18px; }
}
</style>
