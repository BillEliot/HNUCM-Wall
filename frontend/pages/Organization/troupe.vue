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
                            <h1>大学生艺术团</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12 text-center">
                    <a-tabs type="card">
                        <a-tab-pane tab="组织介绍" key="1">
                            <img src="~assets/img/troupe.jpg">
                            <p>校团委大学生艺术团是校团委旗下的四大学生组织之一，主要负责组织各类文艺类活动和比赛，以及文艺演出。艺术团主要由八支队伍和综合管理处组成，八支队伍分别是：合唱队、器乐队、模特队、街舞队、表演队、舞蹈队、主持人队、化妆队。八支队伍每周都有常规训练，训练严格，高要求，但不失轻松，活泼，而综合管理处负责平时的日常工作，以保证艺术团能够正常运转，如：宣传，外联，网络，办公室等等。校艺术团的每一位团员都是因为热爱艺术而聚集在一起，我们没有森严的等级制度，但有一颗热爱艺术的心，有欢乐，愉快的艺术氛围。我们期待你的加入，扩大我们的家族！</p>
                        </a-tab-pane>
                    </a-tabs>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'
import { mapState } from 'vuex'

export default {
  components: {
      Footer,
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
        userBaseInfo: userBaseInfo,
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
    text-decoration: none;
}
</style>
