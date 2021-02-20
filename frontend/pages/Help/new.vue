<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>发布求助</h1>
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
                    <a-input placeholder="输入标题" v-model="title">
                        <a-icon slot="prefix" type="edit" />
                    </a-input>
                    <client-only placeholder='Loading'>
                        <markdown_editor v-model="content" class="editor" />
                    </client-only>
                    <a-button type="primary" class="submit" @click="submitHelp">发布求助</a-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import markdown_editor from '@/components/markdown_editor.vue'

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  components: {
      markdown_editor
  },
  data() {
    return {
    }
  },
  async asyncData({ $axios, query }) {
      let helpDetail = null
      let title = ''
      let content = ''

      if (query.isEdit) {
          await $axios.get('getHelpDetail', {
              params: {
                  id: query.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  helpDetail = response.data.data
                  if (query.isEdit) {
                      title = helpDetail.title
                      content = helpDetail.content
                  }
              }
          })
      }

      return {
          isEdit: query.isEdit,
          helpDetail: helpDetail,
          title: title,
          content: content
      }
  },
  methods: {
      submitHelp() {
          if (!!this.title && !!this.content) {
              this.$axios.post('submitHelp', qs.stringify({
                  id: this.helpDetail.id,
                  isEdit: this.isEdit,
                  title: this.title,
                  content: this.content,
              }))
              .then((response) => {
                  if (response.data.code == 200 && response.data.status == 'success') {
                      this.$message.success('发布成功')
                      this.$router.push({ path: '/help' })
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
