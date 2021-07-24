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
                <div class="row">
                    <div class="text-center col-md-6">
                        <a-card title="功效" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                            <p class="card-text">
                                {{ prescriptionDetail.function }}
                            </p>
                        </a-card>
                    </div>
                    <div class="text-center col-md-6">
                        <a-card title="主治" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                            <p class="card-text">
                                {{ prescriptionDetail.application }}
                            </p>
                        </a-card>
                    </div>
                </div>
                <a-divider />
                <div class="row">
                    <div class="text-center col-md-6">
                        <a-card title="方歌" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                            <div v-for="p in prescriptionDetail.song.split(',')" :key="p" class="card-text">
                                {{ p }}
                            </div>
                        </a-card>
                    </div>
                    <div class="text-center col-md-6">
                        <a-card title="组成" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                            <a v-for="medicine in prescriptionDetail.medicine" :key="medicine" @click="openMedicineDetail(medicine)" class="card-text">
                                {{ medicine }}
                            </a>
                        </a-card>
                    </div>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
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
          params: {
              name: query.name
          }
      })
      .then((response) => {
          prescriptionDetail = response.data.data
      })

      return {
          userBaseInfo: userBaseInfo,
          prescriptionDetail: prescriptionDetail
      }
  },
  methods: {
      openMedicineDetail(name) {
          let routeData = this.$router.resolve({ path: '/medicine/detail', query: { name: name } });
          window.open(routeData.href, '_blank');
      }
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
    font-size: 17px;
}
</style>
