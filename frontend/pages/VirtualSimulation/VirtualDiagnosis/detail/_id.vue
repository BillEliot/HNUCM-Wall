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
                        <h1>诊断记录</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>

    <div class="container entry text-center">
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" tab="患者状况">
            <div class="row">
                <div class="col-md-4">
                <a-card title="姓名">
                    <p>{{ detail.patient_name }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="性别">
                    <p>{{ detail.patient_gender }}</p>
                </a-card> 
                </div>
                <div class="col-md-4">
                <a-card title="年龄">
                    <p>{{ detail.patient_age }}</p>
                </a-card>
                </div>
            </div>
            <hr />
            <div class="row">
                <div class="col-md-4">
                <a-card title="主诉">
                    <p>{{ detail.patient_chiefcomplaint }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="寒热">
                    <p>{{ detail.patient_coldhot }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="汗出">
                    <p>{{ detail.patient_sweat }}</p>
                </a-card>
                </div>
            </div>
            <hr />
            <div class="row">
                <div class="col-md-4">
                <a-card title="疼痛">
                    <p>{{ detail.patient_pain }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="头身胸腹">
                    <p>{{ detail.patient_body }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="眼耳">
                    <p>{{ detail.patient_eareye }}</p>
                </a-card>
                </div>
            </div>
            <hr />
            <div class="row">
                <div class="col-md-4">
                <a-card title="睡眠">
                    <p>{{ detail.patient_sleep }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="性味">
                    <p>{{ detail.patient_flavor }}</p>
                </a-card>
                </div>
                <div class="col-md-4">
                <a-card title="二便">
                    <p>{{ detail.patient_excretion }}</p>
                </a-card>
                </div>
            </div>
            <hr />
            <div class="row">
                <div class="col-md-4">
                    <a-card title="面">
                        <p>{{ detail.patient_face }}</p>
                    </a-card>
                </div>
                <div class="col-md-4">
                    <a-card title="舌">
                        <p>{{ detail.patient_tongue }}</p>
                    </a-card>
                </div>
                <div class="col-md-4">
                    <a-card title="脉">
                        <p>{{ detail.patient_vein }}</p>
                    </a-card>
                </div>
            </div>
        </a-tab-pane>
        <a-tab-pane key="2" tab="你的诊断">
            <div class="row">
                <div class="col-md-4">
                    <a-card title="诊断">
                        <p>{{ detail.player_diagnosis }}</p>
                    </a-card>
                </div>
                <div class="col-md-4">
                    <a-card title="证候分析">
                        <p>{{ detail.player_syndrome }}</p>
                    </a-card> 
                </div>
                <div class="col-md-4">
                    <a-card title="治法">
                        <p>{{ detail.player_method }}</p>
                    </a-card>
                </div>
            </div>
            <hr />
            <div class="row">
                <div class="col-md-4">
                    <a-card title="方剂">
                        <p>{{ detail.player_prescription }}</p>
                    </a-card>
                </div>
                <div class="col-md-4">
                    <a-card title="穴位">
                        <p>{{ detail.player_acupoints }}</p>
                    </a-card>
                </div>
            </div>
        </a-tab-pane>
        <a-tab-pane key="3" tab="参考诊断">
            <div class="row">
                <div class="col-md-4">
                    <a-card title="诊断">
                        <p>{{ detail.ref_diagnosis }}</p>
                    </a-card>
                </div>
                <div class="col-md-4">
                    <a-card title="证候分析">
                        <p>{{ detail.ref_syndrome }}</p>
                    </a-card> 
                </div>
                <div class="col-md-4">
                    <a-card title="治法">
                        <p>{{ detail.ref_method }}</p>
                    </a-card>
                </div>
            </div>
            <hr />
            <div class="row">
                <div class="col-md-4">
                    <a-card title="方剂">
                        <p>{{ detail.ref_prescription }}</p>
                    </a-card>
                </div>
                <div class="col-md-4">
                    <a-card title="穴位">
                        <p>{{ detail.ref_acupoints }}</p>
                    </a-card>
                </div>
            </div>
        </a-tab-pane>
      </a-tabs>
    </div>
    <Footer />
  </div>
</template>

<script>
import qs from 'qs'
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

  async asyncData({ query, $axios, error }) {
    let detail = null
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
      if (userBaseInfo.id == -1) {
        error({ statusCode: 403, message: '先登录吧～' })
      }
    })

    await $axios.get('getLogDetail_VirtualDiagnosis', {
        params: {
            id: query.id
        }
    })
    .then((res) => {
      if (res.data == 1) {
        error({ statusCode: 500, message: '未知错误' })
      }
      else {
        detail = res.data
      }
    })

    return {
      userBaseInfo: userBaseInfo,
      detail: detail
    }
  },

  methods: {
  }
}
</script>

<style scoped>
p {
  font-weight: bold;
  font-size: 18px;
}

.entry {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
