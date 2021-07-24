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
                <div class="text-center col-md-6">
                    <a-card title="性味" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <p class="card-text">
                            {{ medicineDetail.flavor }}
                        </p>
                    </a-card>
                </div>
                <div class="text-center col-md-6">
                    <a-card title="归经" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <p class="card-text">
                            {{ medicineDetail.channel }}
                        </p>
                    </a-card>
                </div>
            </div>
            <a-divider />
            <div class="row">
                <div class="text-center col-md-6">
                    <a-card title="功效" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <div v-for="_function in medicineDetail.function.split(';')" :key="_function" class="card-text-bold">
                            {{ _function }}
                        </div>
                    </a-card>
                </div>
                <div class="text-center col-md-6">
                    <a-card title="应用" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <div v-for="application in medicineDetail.application.split(';')" :key="application" class="card-text-bold">
                            {{ application }}
                        </div>
                    </a-card>
                </div>
            </div>
            <a-divider />
            <div class="row">
                <div class="text-center col-md-6">
                    <a-card title="毒性" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <a-tag v-if="medicineDetail.toxicity == '无毒'" class="card-text">无毒</a-tag>
                        <a-tag v-else-if="medicineDetail.toxicity == '小毒'" color="pink" class="card-text">小毒</a-tag>
                        <a-tag v-else-if="medicineDetail.toxicity == '有毒'" color="red" class="card-text">有毒</a-tag>
                        <a-tag v-else-if="medicineDetail.toxicity == '大毒'" color="purple" class="card-text">大毒</a-tag>
                    </a-card>
                </div>
                    <div class="text-center col-md-6">
                    <a-card title="相关药物" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <a v-for="medicine in medicineDetail.relevantMedicine.split(';')" :key="medicine" @click="openMedicineDetail(medicine)" class="card-text">
                            {{ medicine }}
                        </a>
                    </a-card>
                </div>
            </div>
            <a-divider />
            <div class="row">
                <div class="text-center col-md-12">
                    <a-card title="重点" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                        <p class="card-text-bold">
                            {{ medicineDetail.hightlight }}
                        </p>
                    </a-card>
                </div>
            </div>
            <a-divider />
            <!-- image -->
            <img :src="baseUrl + medicineDetail.image" class="img-responsive" />
        </div>
    </div>
</template>

<script>
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
    font-size: 18px;
}
.card-text-bold {
    font-size: 18px;
    font-weight: bold;
}
</style>
