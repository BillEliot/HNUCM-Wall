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
                            <h1>方剂库</h1>
                            <p class="subheading"></p>
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
                    <a-select
                        placeholder="请选择方剂类型"
                        @change="onChange_selectType"
                        style="width: 20%"
                    >
                        <a-select-option value='解表剂'>解表剂</a-select-option>
                        <a-select-option value='泻下剂'>泻下剂</a-select-option>
                        <a-select-option value='和解剂'>和解剂</a-select-option>
                        <a-select-option value='清热剂'>清热剂</a-select-option>
                        <a-select-option value='祛暑剂'>祛暑剂</a-select-option>
                        <a-select-option value='温里剂'>温里剂</a-select-option>
                        <a-select-option value='表里双解剂'>表里双解剂</a-select-option>
                        <a-select-option value='补益剂'>补益剂</a-select-option>
                        <a-select-option value='固涩剂'>固涩剂</a-select-option>
                        <a-select-option value='安神剂'>安神剂</a-select-option>
                        <a-select-option value='开窍剂'>开窍剂</a-select-option>
                        <a-select-option value='理气剂'>理气剂</a-select-option>
                        <a-select-option value='理血剂'>理血剂</a-select-option>
                        <a-select-option value='治风剂'>治风剂</a-select-option>
                        <a-select-option value='治燥剂'>治燥剂</a-select-option>
                        <a-select-option value='祛湿剂'>祛湿剂</a-select-option>
                        <a-select-option value='祛痰剂'>祛痰剂</a-select-option>
                        <a-select-option value='消食剂'>消食剂</a-select-option>
                        <a-select-option value='驱虫剂'>驱虫剂</a-select-option>
                        <a-select-option value='涌吐剂'>涌吐剂</a-select-option>
                        <a-select-option value='治痈殇剂'>治痈殇剂</a-select-option>
                    </a-select>
                    <a-button type="link" @click="$router.push({ path: '/prescription/search' })">没找到想要的？来直接搜索吧！</a-button>
                    <hr />
                    <!--------------------------------------------------------------------->
                    <div v-for="i in Math.ceil(allPrescription.length / 3)" :key="i" class="row text-center" style="margin-top: 20px;">
                        <div v-if="allPrescription.length - (i-1)*3 >= 3">
                            <div v-for="j in 3" :key="j" class="col-md-4">
                                <a-card hoverable :title="allPrescription[(i-1)*3+j-1].name" @click="prescriptionDetail(allPrescription[(i-1)*3+j-1].name)" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                                    <a-card title="功效" :headStyle="{ 'font-weight': 'bold' }">
                                        <p>{{ allPrescription[(i-1)*3+j-1].function }}</p>
                                    </a-card>
                                    <a-card title="主治" :headStyle="{ 'font-weight': 'bold' }">
                                        <p>{{ allPrescription[(i-1)*3+j-1].application }}</p>
                                    </a-card>
                                </a-card>
                            </div>
                        </div>
                        <div v-else>
                            <div  v-for="j in allPrescription.length - (i-1)*3" :key="j" class="col-md-4">
                                <a-card hoverable :title="allPrescription[(i-1)*3+j-1].name" @click="prescriptionDetail(allPrescription[(i-1)*3+j-1].name)" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                                    <a-card title="功效" :headStyle="{ 'font-weight': 'bold' }">
                                        <p>{{ allPrescription[(i-1)*3+j-1].function }}</p>
                                    </a-card>
                                    <a-card title="主治" :headStyle="{ 'font-weight': 'bold' }">
                                        <p>{{ allPrescription[(i-1)*3+j-1].application }}</p>
                                    </a-card>
                                </a-card>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'
import { mapState } from 'vuex'

import prescription from '~/components/prescription/prescription'

export default {
  components: {
      Footer,
      navbar,
      prescription
  },
  data() {
    return {
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let allPrescription = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    await $axios.get('getAllPrescription', {
        params: {
            type: '解表剂'
        }
    })
    .then((response) => {
        allPrescription = response.data.data
    })

    return {
        userBaseInfo: userBaseInfo,
        allPrescription: allPrescription
    }
  },
  methods: {
      getAllPrescription(type) {
          this.$axios.get('getAllPrescription', {
              params: {
                  type: type
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.allPrescription = response.data.data
              }
          })
      },
      onChange_selectType(value) {
          this.$axios.get('getAllPrescription', {
              params: {
                  type: value,
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.allPrescription = response.data.data
              }
          })
      },
      prescriptionDetail(name) {
          let routeData = this.$router.resolve({ path: '/prescription/detail', query: { name: name } });
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

.card {
    float: left;
    padding: 8px;
}

.description {
    color: red;
    font-style: italic;
    font-weight: bold;
}
</style>
