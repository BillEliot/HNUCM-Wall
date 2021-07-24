<template>
  <div>
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
            <div v-if="item._type == 'thumbsUp'" slot="title">
              <router-link :to="{ path: '/profile', query: { id: item.user.id }}">{{ item.user.username }}</router-link> 给你点赞了 在
              <div v-if="item._from == 'love'" class="message-title"><router-link :to="{ path: '/love/detail', query: { id: item.messageID }}">表白墙</router-link></div>
              <div v-else-if="item._from == 'lose'" class="message-title"><router-link :to="{ path: '/lose/detail', query: { id: item.messageID }}">失物墙</router-link></div>
              <div v-else-if="item._from == 'deal'" class="message-title"><router-link :to="{ path: '/deal/detail', query: { id: item.messageID }}">二手交易</router-link></div>
              <div v-else-if="item._from == 'help'" class="message-title"><router-link :to="{ path: '/help/detail', query: { id: item.messageID }}">求助墙</router-link></div>
              <div v-else-if="item._from == 'article'" class="message-title"><router-link :to="{ path: '/article/detail', query: { id: item.messageID }}">大佬杂谈</router-link></div>
            </div>
            <div v-else-if="item._type == 'comment'" slot="title">
              <router-link :to="{ path: '/profile', query: { id: item.user.id }}">{{ item.user.username }}</router-link> 评论了你 在
              <div v-if="item._from == 'love'" class="message-title"><router-link :to="{ path: '/love/detail', query: { id: item.messageID }}">表白墙</router-link></div>
              <div v-else-if="item._from == 'lose'" class="message-title"><router-link :to="{ path: '/lose/detail', query: { id: item.messageID }}">失物墙</router-link></div>
              <div v-else-if="item._from == 'deal'" class="message-title"><router-link :to="{ path: '/deal/detail', query: { id: item.messageID }}">二手交易</router-link></div>
              <div v-else-if="item._from == 'help'" class="message-title"><router-link :to="{ path: '/help/detail', query: { id: item.messageID }}">求助墙</router-link></div>
              <div v-else-if="item._from == 'article'" class="message-title"><router-link :to="{ path: '/article/detail', query: { id: item.messageID }}">大佬杂谈</router-link></div>
            </div>
            <a-avatar slot="avatar" :src="baseUrl + item.user.avatar" class="avatar" />
          </a-list-item-meta>
          <span>{{ item.date }}</span>
        </a-list-item>
      </a-list>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  data() {
    return {
      pagination: {
        pageSize: 10
      }
    }
  },
  async asyncData({ $axios }) {
    let messageList = []

    await $axios.get('getMessage')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        messageList = response.data.data
      }
    })

    return {
      messageList: messageList
    }
  },
  methods: {
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

.avatar {
  position: relative;
  top: 10px;
}
.message-title {
  display:inline-block;
}
</style>
