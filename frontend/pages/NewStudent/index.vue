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
                        <h1>新生指南</h1>
                        <p class="subheading">来了解大学生活的方方面面吧～</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
        <div class="col-md-8 col-md-offset-2 text-center">
          <h1>Direction</h1>
          <p>ヽ(✿ﾟ▽ﾟ)ノ</p>
          <hr />
        </div>
        <!-- row_1 -->
        <div class="row text-center">
          <div class="col-md-4">
            <a-card hoverable style="width: 320px">
                <img slot="cover" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />
                <a-card-meta title="学校地图">
                    <template slot="description">记好才不会迷路哦～</template>
                </a-card-meta>
            </a-card>
          </div>
          <div class="col-md-4">
            <a-card hoverable style="width: 320px">
                <img slot="cover" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />
                <a-card-meta title="学生组织">
                    <template slot="description">记好各个组织的职能哦～</template>
                </a-card-meta>
            </a-card>
          </div>
          <div class="col-md-4">
            <a-card hoverable style="width: 320px">
                <img slot="cover" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />
                <a-card-meta title="吃喝玩乐">
                    <template slot="description">潇洒去吧～</template>
                </a-card-meta>
            </a-card>
          </div>
        </div>
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
</style>
