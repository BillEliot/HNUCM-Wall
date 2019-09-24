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
                        <h1>我的消息</h1>
                        <p class="subheading">Message</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <div class="container">
      <a-list
        itemLayout="vertical"
        size="large"
        :pagination="pagination"
        :dataSource="messageList"
      >
        <div slot="footer">小伙伴们在关注你哦～</div>
        <a-list-item slot="renderItem" slot-scope="item, index" key="index">
          <a-list-item-meta :description="item.commentContent">
            <div v-if="item.messageType == 'thumbsUp'" slot="title">
              <router-link :to="{ path: '/profile', query: { uid: item.user.uid }}">{{ item.user.nickname }}</router-link> 给你点赞了 在
              <div v-if="item.messageFrom == 'love'" class="message-title"><router-link :to="{ path: '/love/detail', query: { id: item.messageID }}">表白墙</router-link></div>
              <div v-else-if="item.messageFrom == 'lose'" class="message-title"><router-link :to="{ path: '/lose/detail', query: { id: item.messageID }}">失物墙</router-link></div>
              <div v-else-if="item.messageFrom == 'deal'" class="message-title"><router-link :to="{ path: '/deal/detail', query: { id: item.messageID }}">二手交易</router-link></div>
              <div v-else-if="item.messageFrom == 'help'" class="message-title"><router-link :to="{ path: '/help/detail', query: { id: item.messageID }}">求助墙</router-link></div>
              <div v-else-if="item.messageFrom == 'article'" class="message-title"><router-link :to="{ path: '/article/detail', query: { id: item.messageID }}">大佬杂谈</router-link></div>
            </div>
            <div v-else-if="item.messageType == 'comment'" slot="title">
              <router-link :to="{ path: '/profile', query: { uid: item.user.uid }}">{{ item.user.nickname }}</router-link> 评论了你 在
              <div v-if="item.messageFrom == 'love'" class="message-title"><router-link :to="{ path: '/love/detail', query: { id: item.messageID }}">表白墙</router-link></div>
              <div v-else-if="item.messageFrom == 'lose'" class="message-title"><router-link :to="{ path: '/lose/detail', query: { id: item.messageID }}">失物墙</router-link></div>
              <div v-else-if="item.messageFrom == 'deal'" class="message-title"><router-link :to="{ path: '/deal/detail', query: { id: item.messageID }}">二手交易</router-link></div>
              <div v-else-if="item.messageFrom == 'help'" class="message-title"><router-link :to="{ path: '/help/detail', query: { id: item.messageID }}">求助墙</router-link></div>
              <div v-else-if="item.messageFrom == 'article'" class="message-title"><router-link :to="{ path: '/article/detail', query: { id: item.messageID }}">大佬杂谈</router-link></div>
            </div>
            <a-avatar slot="avatar" :src="baseUrl + item.user.avatar" class="avatar" />
          </a-list-item-meta>
        </a-list-item>
      </a-list>
    </div>
    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
      pagination: {
        pageSize: 10
      }
    }
  },
  async asyncData({ $axios, query, redirect }) {
    let userBaseInfo = null
    let messageList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
      if (query.uid != userBaseInfo.uid) {
        redirect('/')
      }
    })
    await $axios.get('getMessage')
    .then((response) => {
      messageList = response.data.info
    })

    return {
      userBaseInfo: userBaseInfo,
      messageList: messageList
    }
  },
  methods: {
  },
  computed: mapState({
    baseUrl: state => state.baseUrl,
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.avatar {
  position: relative;
  top: 10px;
}
.message-title {
  display:inline-block;
}
</style>
