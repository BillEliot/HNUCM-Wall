<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ medicineDetail.name }}</h1>
                            <p class="subheading">{{ medicineDetail.type + '/' + medicineDetail.subType }}</p>
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
                    <a-card title="性味" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text">
                            {{ medicineDetail.flavor }}
                        </p>
                    </a-card>
                    <a-card title="归经" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <!--<a slot="extra" href="#">More</a>-->
                        <p class="card-text">
                            {{ medicineDetail.channel }}
                        </p>
                    </a-card>
                    <a-card title="功效" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text">
                            {{ medicineDetail.function }}
                        </p>
                    </a-card>
                    <a-card title="应用" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text">
                            {{ medicineDetail.application }}
                        </p>
                    </a-card>
                    <a-card title="图片" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <img :src="baseUrl + medicineDetail.image" style="height: 300px" />
                    </a-card>
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
      let medicineDetail = null
      
      await $axios.get('getMedicineDetail', {
          params: {
              name: query.name
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              medicineDetail = response.data.data
          }
      })

      return {
          medicineDetail: medicineDetail
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
