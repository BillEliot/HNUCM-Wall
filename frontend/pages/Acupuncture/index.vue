<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>经络库</h1>
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
                    <a-select default-value="channel" v-model="select">
                        <a-select-option value="channel">按经脉</a-select-option>
                        <a-select-option value="type">按类型</a-select-option>
                    </a-select>
                    <a-select v-show="select == 'channel'" placeholder="请选择经脉" style="width: 20%" @change="getAllAcupoint_Channel">
                        <a-select-option value='手太阴肺经'>手太阴肺经</a-select-option>
                        <a-select-option value='手阳明大肠经'>手阳明大肠经</a-select-option>
                        <a-select-option value='足阳明胃经'>足阳明胃经</a-select-option>
                        <a-select-option value='足太阴脾经'>足太阴脾经</a-select-option>
                        <a-select-option value='手少阴心经'>手少阴心经</a-select-option>
                        <a-select-option value='手太阳小肠经'>手太阳小肠经</a-select-option>
                        <a-select-option value='足太阳膀胱经'>足太阳膀胱经</a-select-option>
                        <a-select-option value='足少阴肾经'>足少阴肾经</a-select-option>
                        <a-select-option value='手厥阴心包经'>手厥阴心包经</a-select-option>
                        <a-select-option value='手少阳三焦经'>手少阳三焦经</a-select-option>
                        <a-select-option value='足少阳胆经'>足少阳胆经</a-select-option>
                        <a-select-option value='足厥阴肝经'>足厥阴肝经</a-select-option>
                        <a-select-option value='任脉'>任脉</a-select-option>
                        <a-select-option value='督脉'>督脉</a-select-option>
                    </a-select>
                    <a-select v-show="select == 'type'" placeholder="请选择穴位类型" style="width: 20%" @change="getAllAcupoint_Type">
                        <a-select-option value='井穴'>井穴</a-select-option>
                        <a-select-option value='荥穴'>荥穴</a-select-option>
                        <a-select-option value='输穴'>输穴</a-select-option>
                        <a-select-option value='经穴'>经穴</a-select-option>
                        <a-select-option value='合穴'>合穴</a-select-option>
                        <a-select-option value='原穴'>原穴</a-select-option>
                        <a-select-option value='络穴'>络穴</a-select-option>
                        <a-select-option value='郄穴'>郄穴</a-select-option>
                        <a-select-option value='下合穴'>下合穴</a-select-option>
                        <a-select-option value='背俞穴'>背俞穴</a-select-option>
                        <a-select-option value='募穴'>募穴</a-select-option>
                        <a-select-option value='八会穴'>八会穴</a-select-option>
                        <a-select-option value='八脉交会穴'>八脉交会穴</a-select-option>
                        <a-select-option value='交会穴'>交会穴</a-select-option>
                    </a-select>
                    <a-button type="link" @click="$router.push({ path: '/acupuncture/search' })">没找到想要的？来直接搜索吧！</a-button>
                    <hr />
                    <!--------------------------------------------------------------------->
                    <div v-for="i in Math.ceil(allAcupoint.length / 3)" :key="i" class="row text-center" style="margin-top: 20px;">
                        <div v-if="allAcupoint.length - (i-1)*3 >= 3">
                            <div v-for="j in 3" :key="j" class="col-md-4">
                                <a-card hoverable :title="allAcupoint[(i-1)*3+j-1].name" @click="acupointDetail(allAcupoint[(i-1)*3+j-1].name)" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                                    <a-card title="位置" :headStyle="{ 'font-weight': 'bold' }">
                                        <p>{{ allAcupoint[(i-1)*3+j-1].location }}</p>
                                    </a-card>
                                    <a-card title="类型" :headStyle="{ 'font-weight': 'bold' }">
                                        <a-tag v-for="(type, index) in allAcupoint[(i-1)*3+j-1]._type.split(';')" :key="index" :color="randomColor()">
                                            {{ type }}
                                        </a-tag>
                                    </a-card>
                                </a-card>
                            </div>
                        </div>
                        <div v-else>
                            <div  v-for="j in allAcupoint.length - (i-1)*3" :key="j" class="col-md-4">
                                <a-card hoverable :title="allAcupoint[(i-1)*3+j-1].name" @click="acupointDetail(allAcupoint[(i-1)*3+j-1].name)" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                                    <a-card title="位置" :headStyle="{ 'font-weight': 'bold' }">
                                        <p>{{ allAcupoint[(i-1)*3+j-1].location }}</p>
                                    </a-card>
                                    <a-card title="类型" :headStyle="{ 'font-weight': 'bold' }">
                                        <a-tag v-for="(type, index) in allAcupoint[(i-1)*3+j-1]._type.split(';')" :key="index" :color="randomColor()">
                                            {{ type }}
                                        </a-tag>
                                    </a-card>
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
        select: 'channel'
    }
  },
  async asyncData({ $axios }) {
    let allAcupoint = []

    await $axios.get('getAllAcupoint_Channel', {
        params: {
            channel: '手太阴肺经'
        }
    })
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            allAcupoint = response.data.data
        }
    })

    return {
        allAcupoint: allAcupoint
    }
  },
  methods: {
      randomColor() {
          let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
          return color[Math.round(Math.random() * (color.length - 1))]
      },
      getAllAcupoint_Channel(channel) {
          this.$axios.get('getAllAcupoint_Channel', {
              params: {
                  channel: channel
              }
          })
          .then((response) => {
            if (response.data.code == 200 && response.data.status == 'success') {
                this.allAcupoint = response.data.data
            }
          })
      },
      getAllAcupoint_Type(type) {
          this.$axios.get('getAllAcupoint_Type', {
              params: {
                  type: type
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.allAcupoint = response.data.data
              }
          })
      },
      acupointDetail(name) {
          let routeData = this.$router.resolve({ path: '/acupuncture/detail', query: { name: name } });
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
