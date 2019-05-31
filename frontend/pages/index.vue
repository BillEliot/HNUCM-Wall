<template>
  <div>
    <header>
      <!-- navbar -->
      <navbar :userBaseInfo="userBaseInfo" />

      <a-carousel autoplay class="carousel">
        <img src="https://s2.ax1x.com/2019/05/26/VV8t9s.jpg">
        <img src="https://s2.ax1x.com/2019/05/26/VV8Jhj.jpg">
        <img src="https://s2.ax1x.com/2019/05/26/VV8N3n.jpg">
      </a-carousel>

    </header>
    
    <div style="margin-top: 100px"></div>

    <div class="container">
      <div class="row">
        
      </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'

export default {
  components: {
    navbar
  },
  data() {
    return {
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    return {
      userBaseInfo: userBaseInfo
    }
  },
  methods: {

  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.ant-carousel >>> .slick-dots {
  height: auto
}

.carousel {
  height: 300px;
}
.carousel img {
  height: 300px;
  opacity: 0.7;
  overflow: hidden;
}

@media (min-width: 1200px) {
  .carousel {
    height: 600px;
  }
  .carousel img {
    height: 600px;
  }
}
</style>
