<template>
  <div>
    <!-- navbar -->
    <navbar :userBaseInfo="userBaseInfo" />
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>学校地图</h1>
                        <p class="subheading">记好才不会迷路哦～</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <div class="container">
        <div class="row">
            <div class="col-md-12 col-xs-12 text-center">
                <a-tabs type="card">
                    <a-tab-pane tab="高德地图" key="1">
                        <client-only>
                            <el-amap vid="amap" :zoom="zoom" :center="center" class="map">
                                <el-amap-marker v-for="(marker, index) in markers" :position="marker.position" :visible="marker.visible" :key="index" :vid="index"></el-amap-marker>
                            </el-amap>
                        </client-only>
                    </a-tab-pane>
                    <a-tab-pane tab="卡通地图" key="2">
                        <img src="~assets/img/map.jpg" />
                    </a-tab-pane>
                </a-tabs>
            </div>
        </div>
    </div>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
        zoom: 16,
        center: [112.894234, 28.129244],
        markers: [{
            position: [112.894234, 28.129244],
            visible: true,
            draggable: false,
            template: '<span>1</span>',
        }]
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

  }
}
</script>

<style scoped>
.map {
  width: 100%;
  height: 600px;
}

img {
  width: 100%
}
</style>
