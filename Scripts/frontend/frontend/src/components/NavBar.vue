<template>
  <el-header class="nav">
    <div class="nav-left">
      <img class="logo" :src="logo" alt="logo"/>
      <span class="brand" style="margin-left: 10px">Echo Trace</span>
    </div>

  </el-header>
</template>

<script>
export default {
  name: 'NavBar',
  props: {logo: {type: String, default: require('@/assets/logo.png')}}
}
</script>

<style scoped>
.nav {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #0A0A0A;
  border-bottom: 1px solid rgba(255, 255, 255, .06)
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 12px
}

.logo {
  width: 70px;
  height: 70px;
  object-fit: contain;
}

.brand {
  color: #fff;
  font-weight: 700;
  letter-spacing: .2px;
  font-size: 42px;
}
</style>
