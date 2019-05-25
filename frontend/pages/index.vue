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
                <router-link :to="{ path: 'profile', query: { nickname: nickname } }">个人信息</router-link>
              </a-menu-item>
              <a-menu-item @click="logout">注销</a-menu-item>
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

      <a-carousel autoplay style="height: 600px">
        <img style="height: 600px" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558497293209&di=48b70276e02fd17a558683fd8c62b0e4&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201503%2F07%2F20150307163030_aRPTy.jpeg">
        <img style="height: 600px" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558497293209&di=48b70276e02fd17a558683fd8c62b0e4&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201503%2F07%2F20150307163030_aRPTy.jpeg">
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
            infinite-scroll-disabled="busy"
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
                  <a-col :span="8">
                    <a-avatar :size="64" :src="baseUrl + item.userFrom_avatar" />
                    <div>
                      <a v-if="item.userFrom_nickname == 'Anony'">匿名</a>
                      <a v-else @click="$router.push({ path: 'profile', query: { nickname: item.userFrom_nickname } })">{{ item.userFrom_nickname }}</a>
                      <p class="bio">{{ item.userFrom_bio }}</p>
                    </div>
                  </a-col>
                  <a-col :span="8">
                    <a-avatar :size="64" src="https://s2.ax1x.com/2019/05/25/Vkx8oR.jpg" />
                  </a-col>
                  <a-col :span="8">
                    <a-avatar :size="64" :src="baseUrl + item.userTo_avatar"/>
                    <div>
                      <a v-if="item.userTo_nickname == 'Anony'">TA</a>
                      <a v-else @click="$router.push({ path: 'profile', query: { nickname: item.userTo_nickname } })">{{ item.userTo_nickname }}</a>
                      <p class="bio">{{ item.userTo_bio }}</p>
                    </div>
                  </a-col>
                </a-row>

                <p style="padding: 10px; font-size: large">{{ item.content }}</p>
                <img v-if="item.cover" style="width: 60%; margin-bottom: 10px;" :src="baseUrl + item.cover" @click="previewCover=true" />
                <a-modal v-model="previewCover" :footer="null">
                  <img style="width: 100%" :src="baseUrl + item.cover">
                </a-modal>
                <br />

                <a-row>
                  <a-col :span="8">
                    <span>
                      <a-icon type="like-o" :theme="item.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(item)" style="cursor: pointer; fontSize: 24px" /> {{ item.thumbsUp }}
                    </span>
                  </a-col>
                  <a-col :span="8">
                    <a-button style="width: 100%">戳进去</a-button>
                  </a-col>
                  <a-col :span="8">
                    <span>
                      <a-icon type="message" style="fontSize: 24px" /> {{ item.comments }}
                    </span>
                  </a-col>
                </a-row>
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
      previewCover: false,

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
      this.$axios.get('logout')
      this.nickname = null
      this.avatar = null
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
    },
    ThumbsUp(item) {
      if (item.isThumbsUp) {
        item.isThumbsUp = false
        item.thumbsUp -= 1
        this.$axios.post('thumbsUp', qs.stringify({
          id: item.id,
          isThumbsUp: false
        }))
      }
      else {
        item.isThumbsUp = true
        item.thumbsUp += 1
        this.$axios.post('thumbsUp', qs.stringify({
          id: item.id,
          isThumbsUp: true
        }))
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

.ant-carousel >>> .slick-dots {
  height: auto
}

.loading {
  position: absolute;
  bottom: 40px;
  width: 100%;
  text-align: center;
}
</style>
