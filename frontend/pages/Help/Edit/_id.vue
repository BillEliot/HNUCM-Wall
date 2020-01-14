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
                            <h1>编辑求助</h1>
                            <p class="subheading">小伙伴们会尽力帮忙的</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- container -->
        <div class="container article">
            <div class="row">
                <div class="col-md-12">
                    <a-input placeholder="输入标题" v-model="helpDetail.title">
                        <a-icon slot="prefix" type="edit" />
                    </a-input>
                    <no-ssr placeholder='Loading'>
                        <mavon-editor :toolbars="toolbars" v-model="helpDetail.content" class="editor" />
                    </no-ssr>
                    <a-button type="primary" class="submit" @click="editHelp">发布求助</a-button>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        toolbars: {
            bold: true,
            italic: true,
            header: true,
            underline: true,
            strikethrough: true,
            mark: true,
            superscript: true,
            subscript: true,
            quote: true,
            ol: true,
            ul: true,
            link: true,
            imagelink: true,
            table: true,
            help: true,
            trash: true,
            save: true,
            alignleft: true,
            aligncenter: true,
            alignright: true,
        }
    }
  },
  async asyncData({ $axios, query, error }) {
      let userBaseInfo = null

      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
          if (userBaseInfo.uid == -1) {
              error({ statusCode: 403, message: '先登录吧～' })
          }
      })
      
      let helpDetail = null
      await $axios.post('getHelpDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/article')
          }
          else {
              helpDetail = response.data
          }
      })

      return {
          userBaseInfo: userBaseInfo,
          helpDetail: helpDetail
      }
  },
  methods: {
      editHelp() {
          if (!!this.helpDetail.title && !!this.helpDetail.content) {
              this.$axios.post('editHelp', qs.stringify({
                  id: this.helpDetail.id,
                  title: this.helpDetail.title,
                  content: this.helpDetail.content,
              }))
              .then((response) => {
                  if (response.data == 0) {
                      this.$message.success('编辑成功')
                      this.$router.push({ path: '/help/detail', query:{ 'id': this.helpDetail.id } })
                  }
                  else if (response.data == 2) {
                      this.$message.error('无权修改')
                  }
                  else {
                      this.$message.error('未知错误')
                  }
              })
          }
          else {
              this.$message.warning('请填写完整的求助信息')
          }
      }
  }
}
</script>

<style scoped>
.article {
    margin-top: 50px;
}

.editor {
    margin-top: 30px;
    height: 100%;
    height: 800px;
    z-index: 1
}

.submit {
    margin-top: 30px;
    width: 100%
}

.extra {
    margin-top: 30px;
}
</style>
