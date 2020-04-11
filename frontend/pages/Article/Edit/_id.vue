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
                            <h1>编辑文章</h1>
                            <p class="subheading">把文章修改的更好吧～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- container -->
        <div class="container article">
            <div class="row">
                <div class="col-md-12">
                    <a-input placeholder="输入文章标题" v-model="articleDetail.title">
                        <a-icon slot="prefix" type="edit" />
                    </a-input>
                    <a-select
                        v-model="articleDetail.tags"
                        mode="tags"
                        :showArrow="false"
                        placeholder="添加标签"
                        notFoundContent="未添加标签"
                        style="width: 100%; margin-top: 10px"
                    >
                    </a-select>
                    <no-ssr placeholder='Loading'>
                        <mavon-editor :toolbars="toolbars" v-model="articleDetail.content" class="editor" />
                    </no-ssr>
                    <div class="extra">
                        <p>设置阅读本篇文章所需花费的硬币，<b>最低为0个硬币，最高为1000个硬币</b></p>
                        <a-input-number
                            v-model="articleDetail.neededCoin"
                            :min="0"
                            :max="1000"
                            :formatter="value => `${value} 硬币`"
                            :parser="value => value.replace(' 硬币', '')"
                            style="width: 150px"
                        />
                    </div>
                    <a-button type="primary" class="submit" @click="editArticle">发布文章</a-button>
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
  async asyncData({ $axios, error, query }) {
      let userBaseInfo = null

      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
          if (userBaseInfo.uid == -1) {
              error({ statusCode: 403, message: '先登录吧～' })
          }
      })

      let articleDetail = null
      await $axios.post('getArticleDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/article')
          }
          else {
              articleDetail = response.data
          }
      })

      return {
          userBaseInfo: userBaseInfo,
          articleDetail: articleDetail
      }
  },
  methods: {
      editArticle() {
          if (!!this.articleDetail.title && !!this.articleDetail.content) {
              this.$axios.post('editArticle', qs.stringify({
                  id: this.articleDetail.id,
                  title: this.articleDetail.title,
                  tags: this.articleDetail.tags,
                  content: this.articleDetail.content,
                  neededCoin: this.articleDetail.neededCoin
              }, { arrayFormat: 'brackets' }))
              .then((response) => {
                  if (response.data == 0) {
                      this.$message.success('编辑成功')
                      this.$router.push({ path: '/article/detail', query: { 'id': this.articleDetail.id } })
                  }
                  else if (response.data == 2) {
                      this.$message.warning('无权修改')
                  }
                  else {
                      this.$message.error('未知错误')
                  }
              })
          }
          else {
              this.$message.warning('请填写完整的文章信息')
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
