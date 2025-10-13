const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/Scss/global.scss";`
      }
    }
  },
  devServer: {
    client: {
      overlay: false
    },
    port: 8888,
    proxy: {
      [process.env.VUE_APP_BASE_API]: {
        target: `http://39.107.49.94:8099`,
        changeOrigin: true,
        logLevel: 'info',
        pathRewrite: {
          ['^' + process.env.VUE_APP_BASE_API]: ''
        }
      }
    }
  },
  chainWebpack: config => {
    config.plugins.delete('prefetch')
  }
}
