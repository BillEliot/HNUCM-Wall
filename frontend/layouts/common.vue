<template>
  <div>
    <!-- navbar -->
    <navbar />
    <!-- main -->
    <a-config-provider :locale="zh_CN">
      <Nuxt />
    </a-config-provider>
    <!-- footer -->
    <Footer />
  </div>
</template>

<script>
import zh_CN from 'ant-design-vue/lib/locale-provider/zh_CN.js'
import moment from 'moment'
import 'moment/locale/zh-cn.js'

import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

moment.locale('zh-cn')
export default {
  components: {
    Footer,
    navbar
  },
  data() {
    return {
      zh_CN
    }
  }
}
</script>

<style>

</style>
