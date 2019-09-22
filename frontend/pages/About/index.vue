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
                        <h1>关于我们</h1>
                        <p class="subheading">About Us</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
          <a-card title="关于社区">
          </a-card>
          <hr />
          <a-card title="商务广告">
            <p>广告投放、商务合作邮箱：eliotwjz@gmail.com</p>
          </a-card>
          <hr />
          <a-card title="捐赠">
            <img src="~assets/img/alipay.jpg" class="alipay">
            <img src="~assets/img/wechatpay.jpg" class="wechatpay">
          </a-card>
      </div>
    </section>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
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

.section {
  padding: 2em 0;
  position: relative;
}
.alipay {
  width: 30%;
  float: left;
}
.wechatpay {
  width: 30%;
  float: right;
}
</style>
