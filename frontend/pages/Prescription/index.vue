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
                    <!-- filter -->
                    <div class="text-left">
                        <a-tag @click="getAllPrescription('解表剂')">解表剂</a-tag>
                        <a-tag @click="getAllPrescription('泻下剂')">泻下剂</a-tag>
                        <a-tag @click="getAllPrescription('和解剂')">和解剂</a-tag>
                        <a-tag @click="getAllPrescription('清热剂')">清热剂</a-tag>
                        <a-tag @click="getAllPrescription('祛暑剂')">祛暑剂</a-tag>
                        <a-tag @click="getAllPrescription('温里剂')">温里剂</a-tag>
                        <a-tag @click="getAllPrescription('表里双解剂')">表里双解剂</a-tag>
                        <a-tag @click="getAllPrescription('补益剂')">补益剂</a-tag>
                        <a-tag @click="getAllPrescription('固涩剂')">固涩剂</a-tag>
                        <a-tag @click="getAllPrescription('安神剂')">安神剂</a-tag>
                        <a-tag @click="getAllPrescription('开窍剂')">开窍剂</a-tag>
                        <a-tag @click="getAllPrescription('理气剂')">理气剂</a-tag>
                        <a-tag @click="getAllPrescription('理血剂')">理血剂</a-tag>
                        <a-tag @click="getAllPrescription('治风剂')">治风剂</a-tag>
                        <a-tag @click="getAllPrescription('治燥剂')">治燥剂</a-tag>
                        <a-tag @click="getAllPrescription('祛湿剂')">祛湿剂</a-tag>
                        <a-tag @click="getAllPrescription('祛痰剂')">祛痰剂</a-tag>
                        <a-tag @click="getAllPrescription('消食剂')">消食剂</a-tag>
                        <a-tag @click="getAllPrescription('驱虫剂')">驱虫剂</a-tag>
                        <a-tag @click="getAllPrescription('涌吐剂')">涌吐剂</a-tag>
                        <a-tag @click="getAllPrescription('治痈殇剂')">治痈殇剂</a-tag>
                    </div>
                    <hr />
                    <p class="text-center description">
                        {{ allPrescription.description }}
                    </p>
                    <prescription :allPrescription="allPrescription.allPrescription"></prescription>
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

import prescription from '~/components/prescription/prescription'

export default {
  components: {
      Footer,
      navbar,
      prescription
  },
  data() {
    return {
        page: 1
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
        allPrescription = response.data
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
            this.allPrescription = response.data
          })
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
