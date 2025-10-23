<template>
  <div class="page contact">
    <side-panel />

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel fixed-panel">
        <header class="head">
          <h2 class="title">Contact Us</h2>
        </header>

        <p class="sub">
          Have a question or feedback? Fill out the form below and we’ll get back to you.
        </p>

        <form class="contact-form">
          <label for="email">Your Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            required
          />

          <label for="message">Message</label>
          <textarea
            id="message"
            rows="6"
            placeholder="Type your message here..."
            required
          ></textarea>

          <button type="submit" class="send-btn">Send Message</button>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import SidePanel from "@/components/SidePanel.vue";

export default {
  name: "ContactUs",
  components: { SidePanel },
};
</script>

<style scoped lang="scss">
$bg: #0a0a0a;
$border: rgba(255, 255, 255, 0.08);
$text: #e6e8eb;

.contact {
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
  text-align: left; 
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

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 14px;

  label {
    font-weight: 600;
    color: #fff;
  }

  input,
  textarea {
    width: 100%;
    background: #111;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 12px;
    color: #fff;
    font-size: 1em;
    outline: none;
    resize: none;
    transition: 0.2s;

    &:focus {
      border-color: #a855f7;
    }
  }

  .send-btn {
    margin-top: 10px;
    align-self: flex-start;
    padding: 12px 28px;
    border: none;
    border-radius: 10px;
    background-color: #a855f7;
    color: #fff;
    font: 700 18px/1 "Roboto", sans-serif;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;

    &:hover {
      opacity: 0.9;
      transform: scale(1.05);
    }
  }
}
</style>
