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
                            <h1>{{ prescriptionDetail.name }}</h1>
                            <p class="subheading">{{ prescriptionDetail.type }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="text-center col-md-12">
                    <a-card title="功效" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text">
                            {{ prescriptionDetail.function }}
                        </p>
                    </a-card>
                    <a-card title="组成" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <!--<a slot="extra" href="#">More</a>-->
                        <p class="card-text">
                        </p>
                    </a-card>
                    <a-card title="方歌" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text">
                            {{ prescriptionDetail.song }}
                        </p>
                    </a-card>
                </div>
            </div>
        </div>

        <Footer />

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
  async asyncData({ $axios, query }) {
      let userBaseInfo = null
      let prescriptionDetail = null

      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })
      
      await $axios.get('getPrescriptionDetail', {
          name: query.name
      })
      .then((response) => {
          prescriptionDetail = response.data
      })

      return {
          userBaseInfo: userBaseInfo,
          prescriptionDetail: prescriptionDetail
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

.card-text {
    font-size: 18px;
}
</style>
