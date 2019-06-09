import pkg from './package'

export default {
  mode: 'universal',

  /*
  ** Headers of the page
  */
  head: {
    title: pkg.name,
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: pkg.description }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },

  /*
  ** Global CSS
  */
  css: [
    'ant-design-vue/dist/antd.css',
    'mavon-editor/dist/css/index.css',
    '@assets/css/bootstrap.min.css',
    '@assets/css/style.css'
  ],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    {
      src: '~plugins/AntDesign',
      ssr: true
    },
    {
      src: '~plugins/VueInfiniteScroll',
      ssr: false
    },
    {
      src: '~plugins/VueVirtualScroller',
      ssr: true
    },
    {
      src: '~plugins/mavonEditor',
      ssr: false
    }
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/axios'
  ],

  /*
  ** Axios module configuration
  */
  axios: {
    proxy: true,
    prefix: '/api'
  },
  proxy: {
    '/api': { 
      target: 'http://localhost:8000',
      pathRewrite: {
        '^/api': '/api',
        changeOrigin: true
      } 
    }
  },

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
    }
  }
}
