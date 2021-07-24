<template>
  <div>
    <a-carousel autoplay class="carousel">
      <img v-for="banner, index in banners" :key="index" :src="banner.imageUrl" @click="imageLink(banner.linkUrl)">
    </a-carousel>
    <!---------------------------------------------------->
    <section class="section">
      <div class="container text-center">
        <a-row>
          <a-col :md="12" :sm="24">
            <a-tabs type="card" default-active-key="hot" class="card-container">
              <a-tab-pane key="hot">
                <span slot="tab">
                  最新热点
                  <a-icon type="heat-map" />
                </span>
                <a-list size="small" bordered :data-source="briefHotList" class="text-right">
                  <a-list-item slot="renderItem" slot-scope="item, index" class="text-left">
                    <nuxt-link :to="{ path: '/hot/detail', query: { id: item.id } }">
                      {{ (index + 1) + '.' + item.title }} <a-tag>{{ item._type }}</a-tag>
                    </nuxt-link>
                  </a-list-item>
                  <nuxt-link to="/hot" slot="footer">
                    更多
                  </nuxt-link>
                </a-list>
              </a-tab-pane>
              <a-tab-pane key="match">
                <span slot="tab">
                  最新比赛
                  <a-icon type="heat-map" />
                </span>
                <a-list size="small" bordered :data-source="briefMatchList" class="text-right">
                  <a-list-item slot="renderItem" slot-scope="item, index" class="text-left">
                    <nuxt-link :to="{ path: '/match/detail', query: { id: item.id } }">
                      {{ (index + 1) + '.' + item.title }} <a-tag>{{ `总奖金: ${item.totalBonus} (元)` }}</a-tag>
                    </nuxt-link>
                  </a-list-item>
                  <nuxt-link to="/match" slot="footer">
                    更多
                  </nuxt-link>
                </a-list>
              </a-tab-pane>
              <a-tab-pane key="lecture">
                <span slot="tab">
                  最新讲座
                  <a-icon type="highlight" />
                </span>
                <a-list size="small" bordered :data-source="briefLectureList" class="text-right">
                  <a-list-item slot="renderItem" slot-scope="item, index" class="text-left">
                    <nuxt-link :to="{ path: '/lecture' }">
                      {{ `${(index + 1)}. ${item.title} - ${item.lecturer}` }}
                      <a-tag v-if="item.state == '未开始'">{{ item.state }}</a-tag>
                      <a-tag v-else-if="item.state == '进行中'" color="green">{{ item.state }}</a-tag>
                      <a-tag v-else-if="item.state == '已结束'" color="red">{{ item.state }}</a-tag>
                    </nuxt-link>
                  </a-list-item>
                  <nuxt-link to="/lecture" slot="footer">
                    更多
                  </nuxt-link>
                </a-list>
              </a-tab-pane>
            </a-tabs>
          </a-col>
          <a-col :md="12" :sm="24">
            <a-tabs type="card" default-active-key="1" class="card-container">
              <a-tab-pane key="1">
                <span slot="tab">
                  最新墙墙
                  <a-icon type="appstore" />
                </span>
                <a-list size="small" bordered :data-source="briefWallList" class="text-right">
                  <a-list-item slot="renderItem" slot-scope="item, index" class="text-left">
                    <nuxt-link v-if="item.type == 'love'" :to="{ path: '/love/detail', query: { id: item.id } }">
                      {{ `${(index + 1)}. ${item.content}` }} <a-tag>表白墙</a-tag>
                    </nuxt-link>
                    <nuxt-link v-else-if="item.type == 'lose'" :to="{ path: '/lose/detail', query: { id: item.id } }">
                      {{ `${(index + 1)}. ${item.content}` }} <a-tag>失物墙</a-tag>
                    </nuxt-link>
                    <nuxt-link v-else-if="item.type == 'deal'" :to="{ path: '/deal/detail', query: { id: item.id } }">
                      {{ `${(index + 1)}. ${item.content}` }} <a-tag>交易墙</a-tag>
                    </nuxt-link>
                    <nuxt-link v-else-if="item.type == 'help'" :to="{ path: '/help/detail', query: { id: item.id } }">
                      {{ `${(index + 1)}. ${item.content}` }} <a-tag>求助墙</a-tag>
                    </nuxt-link>
                  </a-list-item>
                </a-list>
              </a-tab-pane>
              <a-tab-pane key="2">
                <span slot="tab">
                  最新文章
                  <a-icon type="book" />
                </span>
                <a-list size="small" bordered :data-source="briefArticleList" class="text-right">
                  <a-list-item slot="renderItem" slot-scope="item, index" class="text-left">
                    <nuxt-link :to="{ path: '/article/detail', query: { id: item.id } }">
                      {{ `${(index + 1)}. ${item.title}` }}
                    </nuxt-link>
                  </a-list-item>
                  <nuxt-link to="/article" slot="footer">
                    更多
                  </nuxt-link>
                </a-list>
              </a-tab-pane>
              <a-tab-pane key="3">
                <span slot="tab">
                  最新刷题
                  <a-icon type="database" />
                </span>
                <a-list size="small" bordered :data-source="briefBankStatisticsList" class="text-right">
                  <a-list-item slot="renderItem" slot-scope="item, index" class="text-left">
                    {{ `${(index + 1)}.` }}
                    <a-tag>{{ item.user.username }}</a-tag>
                    {{ item.subject }}
                    <span style="float: right">{{ `正确率: ${(item.correctQuestions/item.allQuestions*100).toFixed(2)}%` }}</span>
                  </a-list-item>
                  <nuxt-link to="/bank/statistics" slot="footer">
                    更多
                  </nuxt-link>
                </a-list>
              </a-tab-pane>
            </a-tabs>
          </a-col>
        </a-row>
        <hr />
        <a-card title="墙墙">
          <a-row>
            <a-col :md="6" :sm="24">
              <div class="section-item">
                <nuxt-link to="/love">
                  <a-icon type="heart" theme="twoTone" class="section-icon" />
                  <h4>表白墙</h4>
                </nuxt-link>
                <span class="section-admin">
                  管理员:
                  <a-tag v-for="member in permissionGroupMembers_Love" :key="member.id">
                    <nuxt-link :to="{ path: '/profile', query: { id: member.id } }">
                      {{ member.username }}
                    </nuxt-link>
                  </a-tag>
                </span>
              </div>
            </a-col>
            <a-col :md="6" :sm="24">
              <div class="section-item">
                <nuxt-link to="/lose">
                  <a-icon type="tags" theme="twoTone" class="section-icon" />
                  <h4>失物墙</h4>
                </nuxt-link>
                <span class="section-admin">
                  管理员:
                  <a-tag v-for="member in permissionGroupMembers_Lose" :key="member.id">
                    <nuxt-link :to="{ path: '/profile', query: { id: member.id } }">
                      {{ member.username }}
                    </nuxt-link>
                  </a-tag>
                </span>
              </div>
            </a-col>
            <a-col :md="6" :sm="24">
              <div class="section-item">
                <nuxt-link to="/deal">
                  <a-icon type="dollar" theme="twoTone" class="section-icon" />
                  <h4>二手墙</h4>
                </nuxt-link>
                <span class="section-admin">
                  管理员
                  <a-tag v-for="member in permissionGroupMembers_Deal" :key="member.id">
                    <nuxt-link :to="{ path: '/profile', query: { id: member.id } }">
                      {{ member.username }}
                    </nuxt-link>
                  </a-tag>
                </span>
              </div>
            </a-col>
            <a-col :md="6" :sm="24">
              <div class="section-item">
                <nuxt-link to="/help">
                  <a-icon type="switcher" theme="twoTone" class="section-icon" />
                  <h4>求助墙</h4>
                </nuxt-link>
                <span class="section-admin">
                  管理员:
                  <a-tag v-for="member in permissionGroupMembers_Help" :key="member.id">
                    <nuxt-link :to="{ path: '/profile', query: { id: member.id } }">
                      {{ member.username }}
                    </nuxt-link>
                  </a-tag>
                </span>
              </div>
            </a-col>
          </a-row>
        </a-card>
        <a-card title="学习">
          <a-row>
            <a-col :md="12" :sm="24">
              <div class="section-item">
                <nuxt-link to="/article">
                  <a-icon type="crown" theme="twoTone" class="section-icon" />
                  <h4>大佬杂谈</h4>
                </nuxt-link>
                <span class="section-admin">
                  管理员:
                  <a-tag v-for="member in permissionGroupMembers_Article" :key="member.id">
                    <nuxt-link :to="{ path: '/profile', query: { id: member.id } }">
                      {{ member.username }}
                    </nuxt-link>
                  </a-tag>
                </span>
              </div>
            </a-col>
            <a-col :md="12" :sm="24">
              <div class="section-item">
                <nuxt-link to="/bank">
                  <a-icon type="database" theme="twoTone" class="section-icon" />
                  <h4>题库</h4>
                </nuxt-link>
                <span class="section-admin">
                  管理员:
                  <a-tag v-for="member in permissionGroupMembers_Bank" :key="member.id">
                    <nuxt-link :to="{ path: '/profile', query: { id: member.id } }">
                      {{ member.username }}
                    </nuxt-link>
                  </a-tag>
                </span>
              </div>
            </a-col>
          </a-row>
        </a-card>
      </div>
    </section>
  </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
      moment
    }
  },
  async asyncData({ $axios }) {
    let banners = []

    await $axios.get('getBanners')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        banners = response.data.data
      }
    })
    // --------------------------------------------------------------------
    let briefHotList = []
    let briefMatchList = []
    let briefLectureList = []
    let briefWallList = []
    let briefArticleList = []
    let briefBankStatisticsList = []

    await $axios.get('getBriefHotList')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        briefHotList = response.data.data
      }
    })
    await $axios.get('getBriefMatchList')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        briefMatchList = response.data.data
      }
    })
    await $axios.get('getBriefLectureList')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        briefLectureList = response.data.data
      }
    })
    await $axios.get('getBriefWallList')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        briefWallList = response.data.data
      }
    })
    await $axios.get('getBriefArticleList')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        briefArticleList = response.data.data
      }
    })
    await $axios.get('getBriefBankStatistics')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        briefBankStatisticsList = response.data.data
      }
    })
    // --------------------------------------------------------------------
    let permissionGroupMembers_Love = []
    let permissionGroupMembers_Lose = []
    let permissionGroupMembers_Deal = []
    let permissionGroupMembers_Help = []
    let permissionGroupMembers_Article = []
    let permissionGroupMembers_Bank = []

    await $axios.get('getPermissionGroupMembers', {
      params: {
        group: 'group_love'
      }
    })
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        permissionGroupMembers_Love = response.data.data
      }
    })
    await $axios.get('getPermissionGroupMembers', {
      params: {
        group: 'group_lose'
      }
    })
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        permissionGroupMembers_Lose = response.data.data
      }
    })
    await $axios.get('getPermissionGroupMembers', {
      params: {
        group: 'group_deal'
      }
    })
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        permissionGroupMembers_Deal = response.data.data
      }
    })
    await $axios.get('getPermissionGroupMembers', {
      params: {
        group: 'group_help'
      }
    })
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        permissionGroupMembers_Help = response.data.data
      }
    })
    await $axios.get('getPermissionGroupMembers', {
      params: {
        group: 'group_article'
      }
    })
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        permissionGroupMembers_Article = response.data.data
      }
    })
    await $axios.get('getPermissionGroupMembers', {
      params: {
        group: 'group_bank'
      }
    })
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        permissionGroupMembers_Bank = response.data.data
      }
    })

    return {
      banners:banners,

      briefHotList: briefHotList,
      briefMatchList: briefMatchList,
      briefLectureList: briefLectureList,
      briefWallList: briefWallList,
      briefArticleList: briefArticleList,
      briefBankStatisticsList: briefBankStatisticsList,

      permissionGroupMembers_Love: permissionGroupMembers_Love,
      permissionGroupMembers_Lose: permissionGroupMembers_Lose,
      permissionGroupMembers_Deal: permissionGroupMembers_Deal,
      permissionGroupMembers_Help: permissionGroupMembers_Help,
      permissionGroupMembers_Article: permissionGroupMembers_Article,
      permissionGroupMembers_Bank: permissionGroupMembers_Bank
    }
  },
  methods: {
    imageLink(url) {
      if (url != '') {
        window.open(url, '_blank')
      }
    }
  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.card-container {
  padding: 20px;
  border: 1px solid;
  border-color: lightgray;
  border-radius: 20px;
}

.section {
  padding: 2em 0;
  position: relative;
}
.section h4 {
  color: #0099FF;
}
.section-item {
  position: relative;
  padding: 10px;
  float: left;
  width: 100%;
}
.section-icon {
  font-size: 48px;
}
.section-admin {
  color: gray;
}

.ant-carousel >>> .slick-dots {
  height: auto
}
.carousel {
  height: 300px;
  margin-top: 3em;
}
.carousel img {
  height: 300px;
  opacity: 0.7;
  overflow: hidden;
}

@media (min-width: 992px) {
  .carousel {
    height: 600px;
  }
  .carousel img {
    height: 600px;
  }
}
</style>
