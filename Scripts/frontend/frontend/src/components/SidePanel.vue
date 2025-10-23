<template>
  <aside
    class="side"
    :class="{ expanded }"
    @mouseenter="expanded = true"
    @mouseleave="expanded = false"
  >
    <!-- Brand -->
    <div class="brand" @click="$router.push('/home')">
      <img class="logo" :src="logo" alt="logo" />
      <span class="brand-text">Echo-trace</span>
    </div>

    <!-- Navigation -->
    <nav class="nav">
      <button class="item" @click="$router.push('/result')">
        <span class="icon">
          <svg viewBox="0 0 24 24">
            <path fill="#fff" d="M11 7h2v8h-2V7zm0 10h2v2h-2v-2z" />
          </svg>
        </span>
        <span class="label">Deepfake Detection</span>
      </button>

      <button class="item" @click="$router.push('/tts')">
        <span class="icon">
          <svg viewBox="0 0 24 24">
            <path
              fill="#fff"
              d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V20H8v2h8v-2h-3v-2.08A7 7 0 0 0 19 11h-2z"
            />
          </svg>
        </span>
        <span class="label">Text to Speech</span>
      </button>

      <button class="item" @click="$router.push('/AiHistory')">
        <span class="icon">
          <svg viewBox="0 0 24 24">
            <path
              fill="#fff"
              d="M3 4h18v2H3V4zm2 3h14v13H5V7zm4 2v9h2V9H9zm4 0v9h2V9h-2z"
            />
          </svg>
        </span>
        <span class="label">AI History</span>
      </button>
    </nav>

    <!-- Sign Out -->
    <div class="signout">
      <button class="item logout" @click="$emit('signout')">
        <span class="icon">
          <svg viewBox="0 0 24 24">
            <path
              fill="#FF4B4B"
              d="M16 13v-2H7V8l-5 4 5 4v-3h9zm3-10H5c-1.1 0-2 .9-2 2v4h2V5h14v14H5v-4H3v4c0 1.1.9 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2z"
            />
          </svg>
        </span>
        <span class="label">Sign Out</span>
      </button>
    </div>
  </aside>
</template>

<script>
export default {
  name: "SidePanel",
  props: {
    logo: { type: String, default: require("@/assets/logo.png") },
  },
  data() {
    return { expanded: false };
  },
};
</script>

<style lang="scss" scoped>
$black: #000000;
$text: #ffffff;

.side {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 72px;
  background: $black;
  z-index: 20;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.07);
  transition: width 0.25s ease;

  &.expanded {
    width: 250px;
  }

  /* ---------- Brand ---------- */
  .brand {
    height: 60px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    cursor: pointer;
  }

  .logo {
    width: 32px;
    height: 32px;
    object-fit: contain;
  }

  .brand-text {
    color: $text;
    font-family: "Inria Sans", system-ui;
    font-size: 17px;
    font-weight: 600;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  &.expanded .brand-text {
    opacity: 1;
  }

  /* ---------- Navigation ---------- */
  .nav {
    flex: 1;
    padding: 24px 10px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .item {
    height: 46px;
    display: flex;
    align-items: center;
    background: transparent;
    border: none;
    color: $text;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s ease, transform 0.12s ease;
    padding: 0 12px;

    &:hover {
      background: rgba(255, 255, 255, 0.08);
      transform: scale(1.02);
    }

    .icon {
      width: 32px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-right: 16px;
      flex-shrink: 0; /* keeps icons still */
    }

    .icon svg {
      width: 22px;
      height: 22px;
    }

    .label {
      flex: 1;
      text-align: left; /* left-align text */
      font-family: "Cabin", sans-serif;
      font-size: 15.5px;
      font-weight: 500;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.2s ease;
    }
  }

  &.expanded .item .label {
    opacity: 1;
  }

  /* ---------- Signout ---------- */
  .signout {
    margin-top: auto;
    padding: 14px 10px 18px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);

    .logout {
      color: #ff4b4b;

      &:hover {
        background: rgba(255, 75, 75, 0.12);
      }

      .label {
        color: #ff4b4b;
      }
    }
  }
}
</style>
