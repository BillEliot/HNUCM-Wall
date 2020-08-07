<template>
  <div>
    <!-- navbar -->
    <navbar :userBaseInfo="userBaseInfo" />
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title-zy">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>金匮打卡</h1>
                        <a-button type="primary" size="large" @click="$router.push({ path: '/activity/jingui/statistics' })">打卡统计</a-button>
                        <a-button size="large" @click="$router.push({ path: '/activity/jingui/log', query: { uid: userBaseInfo.uid } })">我的打卡</a-button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div style="margin-top: 50px"></div>
    <div class="container">
        <div class="row">
            <div class="col-md-12 col-xs-12 text-center">
                <a-tabs type="card">
                    <a-tab-pane tab="图文打卡" key="1">
                        <no-ssr placeholder='Loading'>
                            <mavon-editor v-model="content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel" class="editor" />
                        </no-ssr>
                        <a-button type="primary" @click="sign" class="sign">打卡</a-button>
                    </a-tab-pane>
                    <a-tab-pane tab="语音打卡" key="2">
                        <span class="attention">录音后，点击“Record 1”，点击“下载图标”即可下载录音，点击“保存图标”即可上传打卡</span>
                        <audio-recorder
                            upload-url="uploadAudio_JinGui"
                            filename="JinGui"
                            format="mp3"
                            :attempts="1"
                            :time="2"
                            :successful-upload="audio_successful"
                            :failed-upload="audio_failed"
                        />
                    </a-tab-pane>
                </a-tabs>
            </div>
        </div>
    </div>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'
import { mapState } from 'vuex'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
        cover: null,
        isRecording: false
    }
  },
  async asyncData({ $axios, error }) {
    let userBaseInfo = null
    let content = ''

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    await $axios.get('IsFirstSignToday_JinGui')
    .then((response) => {
        if (response.data == 1) {
            error({ statusCode: 500, message: '请登录后打卡' })
        }
        else if (response.data == 2) {
            error({ statusCode: 500, message: '未知错误' })
        }
        else {
            content = response.data
        }
    })

    return {
      userBaseInfo: userBaseInfo,
      content: content
    }
  },
  methods: {
      sign () {
          if (!!this.content) {
              this.$axios.post('sign_JinGui', qs.stringify({
                  content: this.content,
                  cover: this.cover
              }))
              .then((response) => {
                  if (response.data == 0) {
                      this.$message.success('打卡成功')
                  }
                  else if (response.data == 1) {
                      this.$message.warning('说点什么吧~')
                  }
                  else {
                      this.$message.error('未知错误')
                  }
              })
          }
          else {
              this.$message.warning('说点什么吧~')
          }
      },
      audio_successful(msg) {
          if (msg.data == 1) {
              this.$message.error('未知错误')
          }
          else {
              this.$message.success('打卡成功')
          }
      },
      audio_failed(msg) {
          this.$message.error('未知错误')
      },
      $imgAdd(pos, $file) {
           var formdata = new FormData()
           formdata.append('image', $file)
           this.$axios({
               url: 'uploadImg_JinGui',
               method: 'post',
               data: formdata,
               headers: { 'Content-Type': 'multipart/form-data' },
           })
           .then((response) => {
               this.$refs.md.$img2Url(pos, this.baseUrl + '/media/img/JinGui/' + response.data)
               this.cover = response.data
           })
      },
      $imgDel(url) {
          this.$axios.post('removeImg_JinGui', qs.stringify({
              url: url[0]
          }))
          .then((response) => {
              if (response.data == 0) {
                  this.$message.success('删除成功')
              }
              else {
                  this.$message.error('未知错误')
              }
          })
      },
      record() {
          if (this.isRecording) {
              this.isRecording = false
              rc.pause()
              .then(() => {
                  this.$message.success('暂停录音')
              })
              .catch((error) => {
                  this.$message.error(error)
              })
          }
          else {
              this.isRecording = true
              rc.start()
              .then(() => {
                  this.$message.success('开始录音')
              })
              .catch((error) => {
                  this.$message.error(error)
              })
          }
      },
    },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
.editor {
    margin-top: 30px;
    height: 100%;
    height: 300px;
    z-index: 1
}
.attention {
    font-weight: bold;
    color: red;
}
.sign {
    margin-top: 20px;
    width: 100%;
}
.ar {
    width: 100%;
}
</style>
