<template>
  <section class="section">
    <div class="container">
      <div v-for="i in Math.ceil(allPrescription.length / 3)" class="row text-center" style="margin-top: 20px;">
        <div v-if="allPrescription.length - (i-1)*3 >= 3">
          <div v-for="j in 3" class="col-md-4">
            <a-card hoverable :title="allPrescription[(i-1)*3+j-1].name" @click="prescriptionDetail(allPrescription[(i-1)*3+j-1].name)" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
              <a-card title="功效">
                <p>{{ allPrescription[(i-1)*3+j-1].function }}</p>
              </a-card>
            </a-card>
          </div>
        </div>
        <div v-else>
          <div  v-for="j in allPrescription.length - (i-1)*3" class="col-md-4">
            <a-card hoverable :title="allPrescription[(i-1)*3+j-1].name" @click="prescriptionDetail(allPrescription[(i-1)*3+j-1].name)" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
              <a-card title="功效">
                <p>{{ allPrescription[(i-1)*3+j-1].function }}</p>
              </a-card>
            </a-card>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  props: ['allPrescription'],
  data() {
    return {
    }
  },
  methods: {
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
.section {
    padding: 2em 0;
    position: relative;
}

img {
    width: 300px;
    height: 300px;
    margin: 0 auto
}
</style>
