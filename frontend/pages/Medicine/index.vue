<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>中药库</h1>
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
                    <a-select default-value="type" v-model="select">
                        <a-select-option value="type">按类别</a-select-option>
                        <a-select-option value="flavor">按性味</a-select-option>
                        <a-select-option value="channel">按归经</a-select-option>
                    </a-select>
                    <a-cascader
                        v-show="select == 'type'"
                        autoFocus
                        :options="medicineType"
                        placeholder="请选择中药类型"
                        @change="onChange_selectType"
                        style="width: 70%"
                    >
                    </a-cascader>
                    <a-select
                        v-show="select == 'flavor'"
                        mode="multiple"
                        placeholder="请选择性味"
                        style="width: 70%"
                        @change="onChange_selectFlavor"
                    >
                        <a-select-option value="寒">寒</a-select-option>
                        <a-select-option value="热">热</a-select-option>
                        <a-select-option value="温">温</a-select-option>
                        <a-select-option value="凉">凉</a-select-option>
                        <a-select-option value="酸">酸</a-select-option>
                        <a-select-option value="苦">苦</a-select-option>
                        <a-select-option value="甘">甘</a-select-option>
                        <a-select-option value="辛">辛</a-select-option>
                        <a-select-option value="咸">咸</a-select-option>
                    </a-select>
                    <a-select
                        v-show="select == 'channel'"
                        mode="multiple"
                        placeholder="请选择归经"
                        style="width: 70%"
                        @change="onChange_selectChannel"
                    >
                        <a-select-option value="心">心</a-select-option>
                        <a-select-option value="肝">肝</a-select-option>
                        <a-select-option value="脾">脾</a-select-option>
                        <a-select-option value="肺">肺</a-select-option>
                        <a-select-option value="肾">肾</a-select-option>
                    </a-select>
                    <a-button type="link" @click="$router.push({ path: '/medicine/search' })" style="float: right">没找到想要的？来直接搜索吧！</a-button>
                    <hr />
                    <!--------------------------------------------------------------------->
                    <div v-for="i in Math.ceil(allMedicine.length / 3)" class="row text-center" style="margin-top: 20px;">
                        <div v-if="allMedicine.length - (i-1) * 3 >= 3">
                            <div v-for="j in 3" class="col-md-4">
                                <a-card hoverable @click="medicineDetail(allMedicine[(i - 1) * 3 + j - 1].name)" class="medicine-card">
                                    <img slot="cover" :src="baseUrl + allMedicine[(i - 1) * 3 + j - 1].image" />
                                    <a-card-meta :title="allMedicine[(i - 1) * 3 + j - 1].name"></a-card-meta>
                                </a-card>
                            </div>
                        </div>
                        <div v-else>
                            <div  v-for="j in allMedicine.length - (i - 1) * 3" class="col-md-4">
                                <a-card hoverable @click="medicineDetail(allMedicine[(i - 1) * 3 + j - 1].name)" class="medicine-card">
                                    <img slot="cover" :src="baseUrl + allMedicine[(i - 1) * 3 + j - 1].image" />
                                    <a-card-meta :title="allMedicine[(i-1) * 3 + j - 1].name"></a-card-meta>
                                </a-card>
                            </div>
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
        medicineType: [{
            value: '解表药',
            label: '解表药',
            children: [{
                value: '发散风寒药',
                label: '发散风寒药'
            }, {
                value: '发散风热药',
                label: '发散风热药'
            }]
        }, {
            value: '清热药',
            label: '清热药',
            children: [{
                value: '清热泻火药',
                label: '清热泻火药'
            }, {
                value: '清热燥湿药',
                label: '清热燥湿药'
            }, {
                value: '清热解毒药',
                label: '清热解毒药'
            }, {
                value: '清热凉血药',
                label: '清热凉血药'
            }, {
                value: '清虚热药',
                label: '清虚热药'
            }]
        }, {
            value: '泻下药',
            label: '泻下药',
            children: [{
                value: '攻下药',
                label: '攻下药'
            }, {
                value: '润下药',
                label: '润下药'
            }, {
                value: '峻下逐水药',
                label: '峻下逐水药'
            }]
        }, {
            value: '祛风湿药',
            label: '祛风湿药',
            children: [{
                value: '祛风寒湿药',
                label: '祛风寒湿药'
            }, {
                value: '祛风湿热药',
                label: '祛风湿热药'
            }, {
                value: '祛风湿强筋骨药',
                label: '祛风湿强筋骨药'
            }]
        }, {
            value: '化湿药',
            label: '化湿药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '利水渗湿药',
            label: '利水渗湿药',
            children: [{
                value: '利水消肿药',
                label: '利水消肿药'
            }, {
                value: '利尿通淋药',
                label: '利尿通淋药'
            }, {
                value: '利湿退黄药',
                label: '利湿退黄药'
            }]
        }, {
            value: '温里药',
            label: '温里药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '理气药',
            label: '理气药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '消食药',
            label: '消食药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '驱虫药',
            label: '驱虫药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '止血药',
            label: '止血药',
            children: [{
                value: '凉血止血药',
                label: '凉血止血药'
            }, {
                value: '化瘀止血药',
                label: '化瘀止血药'
            }, {
                value: '收敛止血药',
                label: '收敛止血药'
            }, {
                value: '温经止血药',
                label: '温经止血药'
            }]
        }, {
            value: '活血化淤药',
            label: '活血化淤药',
            children: [{
                value: '活血止痛药',
                label: '活血止痛药'
            }, {
                value: '活血调经药',
                label: '活血调经药'
            }, {
                value: '活血疗伤药',
                label: '活血疗伤药'
            }, {
                value: '破血消癓药',
                label: '破血消癓药'
            }]
        }, {
            value: '化痰止咳平喘药',
            label: '化痰止咳平喘药',
            children: [{
                value: '温化寒痰药',
                label: '温化寒痰药'
            }, {
                value: '清化热痰药',
                label: '清化热痰药'
            }, {
                value: '止咳平喘药',
                label: '止咳平喘药'
            }]
        }, {
            value: '安神药',
            label: '安神药',
            children: [{
                value: '重镇安神药',
                label: '重镇安神药'
            }, {
                value: '养心安神药',
                label: '养心安神药'
            }]
        }, {
            value: '平肝息风药',
            label: '平肝息风药',
            children: [{
                value: '平抑肝阳药',
                label: '平抑肝阳药'
            }, {
                value: '息风止痉药',
                label: '息风止痉药'
            }]
        }, {
            value: '开窍药',
            label: '开窍药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '补虚药',
            label: '补虚药',
            children: [{
                value: '补气药',
                label: '补气药'
            }, {
                value: '补血药',
                label: '补血药'
            }, {
                value: '补阴药',
                label: '补阴药'
            }, {
                value: '补阳药',
                label: '补阳药'
            }]
        }, {
            value: '收涩药',
            label: '收涩药',
            children: [{
                value: '固表止汗药',
                label: '固表止汗药'
            }, {
                value: '敛肺涩肠药',
                label: '敛肺涩肠药'
            }, {
                value: '固精缩尿止带药',
                label: '固精缩尿止带药'
            }]
        }, {
            value: '涌吐药',
            label: '涌吐药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '攻毒杀虫止痒药',
            label: '攻毒杀虫止痒药',
            children: [{
                value: '/',
                label: '/'
            }]
        }, {
            value: '拨毒化腐生肌药',
            label: '拨毒化腐生肌药',
            children: [{
                value: '/',
                label: '/'
            }]
        }],
        select: 'type'
    }
  },
  async asyncData({ $axios }) {
    let allMedicine = []

    await $axios.get('getAllMedicine_Type', {
        params: {
            type: '解表药',
            subType: '发散风寒药'
        }
    })
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            allMedicine = response.data.data
        }
    })

    return {
        allMedicine: allMedicine
    }
  },
  methods: {
      onChange_selectType(value) {
          this.$axios.get('getAllMedicine_Type', {
              params: {
                  type: value[0],
                  subType: value[1]
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.allMedicine = response.data.data
              }
          })
      },
      onChange_selectFlavor(value) {
          this.$axios.get('getAllMedicine_Flavor', {
              params: {
                  flavors: value
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.allMedicine = response.data.data
              }
          })
      },
      onChange_selectChannel(value) {
          this.$axios.get('getAllMedicine_Channel', {
              params: {
                  channels: value
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.allMedicine = response.data.data
              }
          })
      },
      medicineDetail(name) {
          let routeData = this.$router.resolve({ path: '/medicine/detail', query: { name: name } })
          window.open(routeData.href, '_blank')
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

.medicine-card {
    width: 300px;
    height: 260px;
    margin: 0 auto
}

.description {
    color: red;
    font-style: italic;
    font-weight: bold;
}
</style>
