<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>{{ matchDetail.title }}</h1>
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
                    <a-card title="描述" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text content">
                            {{ matchDetail.description }}
                        </p>
                    </a-card>
                    <a-card title="要求" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text content">
                            {{ matchDetail.requirement }}
                        </p>
                    </a-card>
                    <a-card title="奖项" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text content">
                            {{ matchDetail.prizeDescription }}
                        </p>
                    </a-card>
                    <a-card title="时间" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <p class="card-text content">
                            {{ `${moment(matchDetail.startDate).format('lll')} ~ ${moment(matchDetail.endDate).format('lll')}` }}
                        </p>
                    </a-card>
                    <a-card title="文件" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px' }">
                        <a-list item-layout="horizontal" :data-source="matchDetail.files" class="text-left">
                            <a-list-item slot="renderItem" slot-scope="item, index">
                                <a-list-item-meta>
                                    <a slot="title" @click="download(item.url)" style="color: blue">{{ item.name }}</a>
                                    <a-avatar v-if="item.type == 'word'" slot="avatar"><a-icon slot="icon" type="file-word" theme="twoTone" /></a-avatar>
                                    <a-avatar v-else-if="item.type == 'excel'" slot="avatar"><a-icon slot="icon" type="file-excel" theme="twoTone" /></a-avatar>
                                    <a-avatar v-else-if="item.type == 'ppt'" slot="avatar"><a-icon slot="icon" type="file-ppt" theme="twoTone" /></a-avatar>
                                    <a-avatar v-else-if="item.type == 'pdf'" slot="avatar"><a-icon slot="icon" type="file-pdf" theme="twoTone" /></a-avatar>
                                </a-list-item-meta>
                            </a-list-item>
                        </a-list>
                    </a-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
        moment
    }
  },
  async asyncData({ $axios, query }) {
      let matchDetail = null

      await $axios.get('getMatchDetail', {
          params: {
              id: query.id
          }
      })
      .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
              matchDetail = response.data.data
          }
      })

      return {
          matchDetail: matchDetail
      }
  },
  methods: {
      download(url) {
          window.open(this.baseUrl + url, '_blank')
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

.content {
    font-size: 18px;
}
</style>
