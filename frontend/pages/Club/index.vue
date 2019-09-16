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
                        <a-tag color="green" @click="page = 1">医药学术类</a-tag>
                        <a-tag color="red" @click="page = 2">公益实践类</a-tag>
                        <a-tag color="blue" @click="page = 3">文化科研类</a-tag>
                        <a-tag @click="page = 4">体育竞技类</a-tag>
                        <a-tag color="purple" @click="page = 5">艺术表演类</a-tag>
                    </div>
                    <hr />
                    <club_learning v-if="page == 1"></club_learning>
                    <club_practice v-if="page == 2"></club_practice>
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

import club_learning from '~/components/club/club_learning'
import club_practice from '~/components/club/club_practice'

export default {
  components: {
      Footer,
      navbar,
      club_learning,
      club_practice
  },
  data() {
    return {
        page: 1
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
