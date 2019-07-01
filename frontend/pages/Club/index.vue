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
                            <h1>社团</h1>
                            <p class="subheading">找找心爱的社团吧～</p>
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
                    <!-- filter -->
                    <div class="text-left">
                        <a-tag color="green">医药学术类</a-tag>
                        <a-tag color="red">公益实践类</a-tag>
                        <a-tag color="blue">文化科研类</a-tag>
                        <a-tag>体育竞技类</a-tag>
                        <a-tag color="purple">艺术表演类</a-tag>
                    </div>
                    <hr />
                    <div v-for="club in clubs" :key="club" class="col-md-4 card">
                        <a-card hoverable style="padding: 0;">
                            <img
                                src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
                                slot="cover"
                            />
                            <a-card-meta
                                title="Europe Street beat">
                                <template slot="description">www.instagram.com</template>
                            </a-card-meta>
                        </a-card>
                    </div>
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

.card {
    float: left;
    padding: 8px;
}
</style>
