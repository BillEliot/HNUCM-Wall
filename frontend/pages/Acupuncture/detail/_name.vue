<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ acupointDetail.name }}</h1>
                            <p class="subheading">{{ acupointDetail.channel }}</p>
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
                    <div class="row">
                        <div class="text-center col-md-6">
                            <a-card title="定位" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                <p class="card-text">
                                    {{ acupointDetail.location }}
                                </p>
                            </a-card>
                        </div>
                        <div class="text-center col-md-6">
                            <a-card title="类型" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                <a-tag v-for="(type, index) in acupointDetail.type.split(';')" :key="index" :color="randomColor()" class="card-text">
                                    {{ type }}
                                </a-tag>
                            </a-card>
                        </div>
                    </div>
                    <a-divider />
                    <div class="row">
                        <div class="text-center col-md-6">
                            <a-card title="主治" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                <div v-for="(_function, index) in acupointDetail.function.split(';')" :key="index" class="card-text">
                                    {{ _function }}
                                </div>
                            </a-card>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
    }
  },
  async asyncData({ $axios, query }) {
      let acupointDetail = null
      
      await $axios.get('getAcupointDetail', {
          params: {
              name: query.name
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              acupointDetail = response.data.data
          }
      })

      return {
          acupointDetail: acupointDetail
      }
  },
  methods: {
      randomColor() {
          let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
          return color[Math.round(Math.random() * (color.length - 1))]
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
    font-size: 18px;
}
</style>
