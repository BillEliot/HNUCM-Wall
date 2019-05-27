<template>
  <div>
    <header>
      <!-- navbar -->
      <navbar :userBaseInfo="userBaseInfo" />

      <a-carousel autoplay class="carousel">
        <img src="https://s2.ax1x.com/2019/05/26/VV8t9s.jpg">
        <img src="https://s2.ax1x.com/2019/05/26/VV8Jhj.jpg">
        <img src="https://s2.ax1x.com/2019/05/26/VV8N3n.jpg">
      </a-carousel>

      <div class="banner-title">
        <div class="text-center">
          <h1>❤HNUCM❤</h1>
          <h1>墙墙</h1>
        </div>
      </div>

    </header>
    <div style="margin-top: 100px"></div>

    <div class="container">
      <div class="row">
        <div class="col-md-12 col-xs-12">
          <!-- Top -->
          <a-card hoverable style="width: 100%; margin-bottom: 20px">
            <template class="ant-card-actions" slot="actions">
              <a-icon type="heart" />
            </template>
            <a-card-meta
              title="Nickname"
              description="表白的话">
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
                    <a-avatar v-if="item.userFrom_uid == -1" :size="64" :src="baseUrl + item.userFrom_avatar" />
                    <a-avatar v-else :size="64" :src="baseUrl + item.userFrom_avatar" @click="$router.push({ path: 'profile', query: { uid: item.userFrom_uid } })" style="cursor: pointer;" />
                    <div>
                      <a v-if="item.userFrom_uid == -1">匿名</a>
                      <a v-else @click="$router.push({ path: 'profile', query: { uid: item.userFrom_uid } })">{{ item.userFrom_nickname }}</a>
                      <p class="bio">{{ item.userFrom_bio }}</p>
                    </div>
                  </a-col>
                  <a-col :span="8">
                    <a-avatar :size="64" src="https://s2.ax1x.com/2019/05/25/Vkx8oR.jpg" />
                  </a-col>
                  <a-col :span="8">
                    <a-avatar v-if="item.userTo_uid == -1" :size="64" :src="baseUrl + item.userTo_avatar" />
                    <a-avatar v-else :src="baseUrl + item.userTo_avatar" @click="$router.push({ path: 'profile', query: { uid: item.userTo_uid } })" style="cursor: pointer;" />
                    <div>
                      <a v-if="item.userTo_uid == -1">{{ item.nameTo }}</a>
                      <a v-else @click="$router.push({ path: 'profile', query: { uid: item.userTo_uid } })">{{ item.userTo_nickname }}</a>
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
                    <span style="fontSize: 24px">
                      <a-icon type="like-o" :theme="item.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(item)" style="cursor: pointer;" /> {{ item.thumbsUp }}
                    </span>
                  </a-col>
                  <a-col :span="8">
                    <a-button style="width: 100%" @click="$router.push({ path: 'love/detail', query: { id: item.id } })">戳进去</a-button>
                  </a-col>
                  <a-col :span="8">
                    <span style="fontSize: 24px">
                      <a-icon type="message" /> {{ item.comments }}
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
import navbar from '~/components/navbar'

export default {
  components: {
    navbar
  },
  data() {
    return {
      loading: false,
      busy: false,
      previewCover: false,

      loveList: []
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let loveList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    await $axios.post('getLoveList', qs.stringify({
      index: '0'
    }))
    .then((response) => {
      loveList = response.data.info
    })

    return {
      userBaseInfo: userBaseInfo,
      loveList: loveList
    }
  },
  methods: {
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
      if (this.userBaseInfo.uid == -1) {
        this.$message.warning('先登录吧～')
      }
      else {
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

.banner-title {
  position: absolute;
  width: 100%;
  overflow: hidden;
  display: block;
  top: 10%;
}
.banner-title h1 {
  font-size: 48px;
  color: black;
}

.carousel {
  height: 300px;
}
.carousel img {
  height: 300px;
  opacity: 0.7;
  overflow: hidden;
}

@media (min-width: 1200px) {
  .banner-title {
    top: 20%;
  }
  .banner-title h1 {
    font-size: 84px;
  }

  .carousel {
    height: 600px;
  }
  .carousel img {
    height: 600px;
  }
}
</style>
