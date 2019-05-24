<template>
  <div>
    <header>
      <!-- navbar -->
      <a-menu v-model="navbar" mode="horizontal" theme="dark" class="nav">
        <a-sub-menu>
          <span slot="title"><a-icon type="coffee" />表白墙</span>
          <a-menu-item-group title="I Love U">
            <a-menu-item key="love:1">表白墙</a-menu-item>
            <a-menu-item key="love:2">我要表白</a-menu-item>
          </a-menu-item-group>
        </a-sub-menu>

        <a-menu-item key="whisper">
          <a-icon type="star" /> 悄悄话
        </a-menu-item>
        <!-- auth -->
        <template v-if="nickname">
          <a-avatar :src="baseUrl + avatar" />
          <a-dropdown>
            <a> {{ nickname }} <a-icon type="down" /></a>
            <a-menu slot="overlay">
              <a-menu-item>
                <router-link to="/profile">个人信息</router-link>
              </a-menu-item>
              <a-menu-item @click="logout">注销</a-menu-item>
              <a-menu-item>
                <router-link to="/reserve">立即预约</router-link>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </template>
        <template v-else>
          <router-link to="/login">
            <a-button type="primary" style="margin-right: 10px">登录</a-button>
          </router-link>
          <router-link to="/register">
            <a-button>注册</a-button>
          </router-link>
        </template>
      </a-menu>

      <a-carousel autoplay>
        <img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558497293209&di=48b70276e02fd17a558683fd8c62b0e4&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201503%2F07%2F20150307163030_aRPTy.jpeg">
        <img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558497293209&di=48b70276e02fd17a558683fd8c62b0e4&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201503%2F07%2F20150307163030_aRPTy.jpeg">
      </a-carousel>
      <!--
      <div class="hero-holder" style="position: relative">
        <div class="hero-message">
          <h1 class="uppercase">优敏思</h1>
          <h2 class="hero-subtitle">竞赛教育领跑者</h2>
        </div>
      </div>
      -->
    </header>

    <div style="margin-top: 100px"></div>

    <div class="container">
      <div class="row">
        <div class="col-md-12 col-xs-12">
          <!-- Top -->
          <a-card hoverable style="width: 100%; margin-bottom: 20px">
            <template class="ant-card-actions" slot="actions">
              <a-icon type="setting" />
              <a-icon type="edit" />
              <a-icon type="ellipsis" />
            </template>
            <a-card-meta
              title="Card title"
              description="This is the description">
              <a-avatar slot="avatar" src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
            </a-card-meta>
            <img
              src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
              slot="cover"
              style="height: 200px"
            />
          </a-card>
          <!-- List -->
          <DynamicScroller
            :items="loveList"
            :min-item-size="50"
            v-infinite-scroll="infiniteLoadLoveList"
            :infinite-scroll-disabled="busy"
            :infinite-scroll-distance="20"
            style="width: 100%"
            class="text-center"
          >
            <template v-slot="{ item, index, active }">
              <DynamicScrollerItem
                :item="item"
                :active="active"
                :size-dependencies="[
                  item,
                ]"
                :data-index="index"
                slot="renderItem"
              >
                <a-row>
                  <a-col :span="12">
                    <a-avatar :src="baseUrl + item.userFrom_avatar" />
                    <div>
                      <a>{{ item.userFrom_nickname }}</a>
                      <p style="color: rgba(0, 0, 0, 0.45)">{{ item.userFrom_bio }}</p>
                    </div>
                  </a-col>
                  <a-col :span="12">
                    <a-avatar :src="baseUrl + item.userTo_avatar"/>
                    <div>
                      <a>{{ item.userTo_nickname }}</a>
                      <p style="color: rgba(0, 0, 0, 0.45)">{{ item.userTo_bio }}</p>
                    </div>
                  </a-col>
                </a-row>

                <p style="padding: 10px; font-size: large">{{ item.content }}</p>
                <img v-if="item.cover" style="width: 50%; margin-bottom: 10px;" :src="baseUrl + item.cover" />
                <br />

                <span style="margin-right: 20%">
                  <a-icon type="like-o" /> 100
                </span>
                <span style="margin-left: 20%">
                  <a-icon type="message" /> 200
                </span>
                <hr />
              </DynamicScrollerItem>
            </template>
          </DynamicScroller>
          <a-spin v-if="loading" class="loading" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      navbar: null,
      nickname: null,
      avatar: null,

      loading: false,
      busy: false,

      loveList: []
    }
  },
  async asyncData({ $axios }) {
    let nickname = null
    let avatar = null
    let loveList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      nickname = response.data.nickname,
      avatar = response.data.avatar
    })

    await $axios.post('getLoveList', qs.stringify({
      index: '0'
    }))
    .then((response) => {
      loveList = response.data.info
    })

    return {
      nickname: nickname,
      avatar: avatar,
      loveList: loveList
    }
  },
  methods: {
    logout() {

    },
    infiniteLoadLoveList() {
      this.loading = true
      this.$axios.post('getLoveList', qs.stringify({
        index: this.loveList.length
      }))
      .then((response) => {
        this.loading = false
        if (response.data == 1) {
          this.busy = true
          this.$message.warning('到底啦～')
        }
        else {
          this.loveList = this.loveList.concat(response.data.info)
        }
      })
    }
  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  })
}
</script>

<style>
.loading {
  position: absolute;
  bottom: 40px;
  width: 100%;
  text-align: center;
}
</style>
