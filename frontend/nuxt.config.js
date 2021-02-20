export default {
  /*
  ** Headers of the page
  */
  head: {
    title: '寻可校园墙',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '寻可校园墙' },
      { name: "keywords", content: "湖南中医药大学,校园墙,题库,查题,表白墙,失物招领" }
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
  plugins: [{
    src: '@/plugins/AxiosInterceptor',
    ssr: true
  }, {
    src: '@/plugins/AntDesign',
    ssr: true
  }, {
    src: '@/plugins/VueInfiniteScroll',
    ssr: false
  }, {
    src: '@/plugins/VueVirtualScroller',
    ssr: true
  }, {
    src: '@/plugins/mavonEditor',
    ssr: false
  }, {
    src: '@/plugins/VueAMap',
    ssr: false
  }, {
    src: '@/plugins/AudioRecorder',
    ssr: false
  }, {
    src: '@/plugins/baidu.js',
    ssr: false
  }],
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
        '^/api': '/api'
      },
      changeOrigin: true
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
