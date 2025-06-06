const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}

  },
  devServer: {
    proxy: {
      // tout ce qui commence par /function ...
      '/function': {
        target: 'http://127.0.0.1:8080', // URL de ta gateway
        changeOrigin: true
      }
    }
  }
})
