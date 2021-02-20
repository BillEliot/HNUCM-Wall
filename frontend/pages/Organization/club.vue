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
                            <h1>学生社团联合会</h1>
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
                            <img src="~assets/img/club.jpg" style="width: 200px;">
                            <p>社联是代表社团联系校团委、学院、学生会及其他部门的纽带，反映社团的要求，推动学校校园文化建设，同时抓好自身建设，抓好学生社团负责人队伍建设，抓好学生社团发展建设，为建设有中医药院校特色高校文化生活而努力奋斗。社联在开展各项工作中，必须坚决贯彻党中央对全国高等院校社团管理的要求，围绕学校的中心工作，积极配合学校各工作部门，适应全国高校校园文化发展和情况的变化，不断改进管理方式和方法，建立起一套科学的、完善的、与学校实际情况相符的社团管理方案。</p>
                        </a-tab-pane>
                        <a-tab-pane tab="学生社团" key="2">
                            <router-link to="/club">
                                <a-button type="primary" size="large">查看所有社团</a-button>
                            </router-link>
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
import Footer from '~/components/footer'
import navbar from '~/components/navbar'
import { mapState } from 'vuex'

export default {
  components: {
      Footer,
      navbar,
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
