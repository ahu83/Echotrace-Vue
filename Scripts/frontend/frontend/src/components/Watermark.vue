<!-- Watermark.vue -->
<template>
  <div class="watermark" v-if="visible" ref="watermark"></div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    },
    visible: {
      type: Boolean,
      default: true
    }
  },
  mounted() {
    this.addWatermark(this.text)
  },
  methods: {
    addWatermark(text) {
      const watermarkDiv = this.$refs.watermark
      const canvas = document.createElement('canvas')
      canvas.width = 200
      canvas.height = 200

      const ctx = canvas.getContext('2d')
      ctx.rotate((-20 * Math.PI) / 180)
      ctx.font = '20px Arial'
      ctx.fillStyle = 'rgba(200, 200, 200, 0.30)'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(text, canvas.width / 2, canvas.height / 2)

      watermarkDiv.style.backgroundImage = `url(${canvas.toDataURL('image/png')})`
      watermarkDiv.style.pointerEvents = 'none'
      watermarkDiv.style.position = 'fixed'
      watermarkDiv.style.top = 0
      watermarkDiv.style.left = 0
      watermarkDiv.style.width = '100%'
      watermarkDiv.style.height = '100%'
      watermarkDiv.style.zIndex = 50
    }
  }
}
</script>
